from typing import Tuple

import numpy as np
import snowflake.snowpark.functions as F

from snowflake.snowpark import DataFrame
import logging

from ydata_profiling.config import Settings
from ydata_profiling.model.summary_algorithms import (
    describe_numeric_1d,
    histogram_compute,
)


from numpy import array



def numeric_stats_spark(df: DataFrame, summary: dict) -> dict:
    column = df.columns[0]

    print("Column:"+str(column))

    expr = [

        F.min(F.col(column)).alias("min"),
        F.max(F.col(column)).alias("max")
    ]

    expr_overflow = [
        F.mean(F.col(column)).alias("mean"),
        F.stddev(F.col(column)).alias("std"),
        F.variance(F.col(column)).alias("variance"),
        F.kurtosis(F.col(column)).alias("kurtosis"),
        F.skew(F.col(column)).alias("skewness"),
        F.sum(F.col(column)).alias("sum")
    ]

    try:
        #try all
        ret= df.agg(*(expr+expr_overflow) ).first().asDict()
    except Exception as exc:
        print(f"Error calculating: {exc}")
        print("trying one by one....")

    ret={
        "MEAN":None,
        "STD":None,
        "VARIANCE":None,
        "KURTOSIS":None,
        "SKEWNESS":None,
        "SUM":None
    }
    for e in expr_overflow:
        try:
            ret=ret | df.agg(e).first().asDict() 
        except Exception as exc:
            print(f"Error calculating {e}: {exc}")
            
    
    ret= df.agg(*expr).first().asDict() | ret
    print(ret)
    return ret


@describe_numeric_1d.register
def describe_numeric_1d_spark(
    config: Settings, df: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, dict]:
    """Describe a boolean series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    df = df.dropna()
    stats = numeric_stats_spark(df, summary)
    summary["min"] = stats["MIN"]
    summary["max"] = stats["MAX"]
    summary["mean"] = stats["MEAN"]
    summary["std"] = stats["STD"]
    summary["variance"] = stats["VARIANCE"]
    summary["skewness"] = stats["SKEWNESS"]
    summary["kurtosis"] = stats["KURTOSIS"]
    summary["sum"] = stats["SUM"]

    value_counts = summary["value_counts"]

    n_infinite = (
        value_counts.where(F.col(df.columns[0]).isin([np.inf, -np.inf]))
        .agg(F.sum(F.col("count")).alias("count"))
        .first()
    )
    if n_infinite is None or n_infinite["COUNT"] is None:
        n_infinite = 0
    else:
        n_infinite = n_infinite["COUNT"]
    summary["n_infinite"] = n_infinite

    n_zeros = value_counts.where(F.col(df.columns[0]) == 0).first()
    if n_zeros is None:
        n_zeros = 0
    else:
        n_zeros = n_zeros["COUNT"]
    summary["n_zeros"] = n_zeros

    n_negative = (
        value_counts.where(f"{df.columns[0]} < 0")
        .agg(F.sum(F.col("count")).alias("count"))
        .first()
    )
    if n_negative is None or n_negative["COUNT"] is None:
        n_negative = 0
    else:
        n_negative = n_negative["COUNT"]
    summary["n_negative"] = n_negative

    quantiles = config.vars.num.quantiles

    summary.update(
        {
            f"{percentile:.0%}": value
            for percentile, value in zip(
                quantiles,
                df.stat.approxQuantile(
                    f"{df.columns[0]}",
                    quantiles
                ),
            )
        }
    )

    median = summary["50%"]

    print("Columns"+str(df.columns))

    # handle nulls in the column

    summary["mad"] = df.select(
        (F.abs(F.col(f"{df.columns[0]}").cast("int") - median)).alias("abs_dev")
    ).stat.approxQuantile("abs_dev", [0.5])[0]

    # FIXME: move to fmt
    summary["p_negative"] = summary["n_negative"] / summary["n"]
    summary["range"] = summary["max"] - summary["min"]
    summary["iqr"] = summary["75%"] - summary["25%"]
    summary["cv"] = float(summary["std"]) / float(summary["mean"]) if summary["mean"] and summary["std"] else np.nan
    summary["p_zeros"] = summary["n_zeros"] / summary["n"]
    summary["p_infinite"] = summary["n_infinite"] / summary["n"]

    # TODO - enable this feature
    # because spark doesn't have an indexing system, there isn't really the idea of monotonic increase/decrease
    # [feature enhancement] we could implement this if the user provides an ordinal column to use for ordering
    # ... https://stackoverflow.com/questions/60221841/how-to-detect-monotonic-decrease-in-pyspark
    summary["monotonic"] = 0

    # this function only displays the top N (see config) values for a histogram.
    # This might be confusing if there are a lot of values of equal magnitude, but we cannot bring all the values to
    # display in pandas display
    # the alternative is to do this in spark natively, but it is not trivial
    # infinity_values = [np.inf, -np.inf]
    # infinity_index = summary["value_counts_without_nan"].index.isin(infinity_values)

    # summary.update(
    #     histogram_compute(
    #         config,
    #         summary["value_counts_without_nan"][~infinity_index].index.values,
    #         summary["n_distinct"],
    #         weights=summary["value_counts_without_nan"][~infinity_index].values,
    #     )
    # )


    # Get the number of bins
    col_name = df.columns[0]
    bins = config.plot.histogram.bins
    bins_arg = 10 if bins == 0 else min(bins, summary["n_distinct"])

    print("Bins"+str(bins_arg))


    df_hist = (
            df.withColumn("hist_bin", F.sql_expr(f"""
                        width_bucket( {col_name}, min({col_name}) over (partition by null), max({col_name}) over (partition by null)+0.01,{bins_arg}) """))
            .group_by("hist_bin")
            .count()
            .sort("hist_bin")
        )
    rows = df_hist.collect()
    print("Rows"+str(rows))
    hist_counts = [0] * bins_arg
    for idx, r in enumerate(rows):
        if r["HIST_BIN"] and r["HIST_BIN"] <= bins_arg:
            hist_counts[r["HIST_BIN"]-1] = r["COUNT"]

    if summary["max"]:
        step = (summary["max"] - summary["min"]) / bins_arg
        bin_edges = [summary["min"] + i * step for i in range(bins_arg + 1)]
    else:
        bin_edges=[0] * bins_arg

    summary["histogram"] = (array(hist_counts), array(bin_edges))

    print(f"Summary histogram:"+str(summary["histogram"]))

    return config, df, summary
