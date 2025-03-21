from typing import Tuple

import snowflake.snowpark.functions as F
from numpy import array
from snowflake.snowpark import DataFrame
import datetime

from ydata_profiling.config import Settings
from ydata_profiling.model.summary_algorithms import describe_date_1d


def date_stats_spark(df: DataFrame, summary: dict) -> dict:
    column = df.columns[0]

    expr = [
        F.min(F.col(column)).alias("min"),
        F.max(F.col(column)).alias("max"),
    ]

    return df.agg(*expr).first().asDict()


@describe_date_1d.register
def describe_date_1d_spark(
    config: Settings, df: DataFrame, summary: dict
) -> Tuple[Settings, DataFrame, dict]:
    """Describe a date series.

    Args:
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """
    col_name = df.columns[0]
    stats = date_stats_spark(df, summary)

   

    summary.update({"min": stats["MIN"], "max": stats["MAX"]})

    if summary["max"] and summary["min"]:
        summary["range"] = summary["max"] - summary["min"]
    else:
        summary["range"]=-1

    # Convert date to numeric so we can compute the histogram
    df = df.withColumn(col_name, F.unix_timestamp(df[col_name]))

    # Get the number of bins
    bins = config.plot.histogram.bins
    bins_arg = 10 if bins == 0 else min(bins, summary["n_distinct"])

    print("Bins"+str(bins_arg))


    def get_timestamp(d):
        if isinstance(d, datetime.datetime):
            return d.timestamp()
        else:
            return int(datetime.datetime.combine(d, datetime.time()).timestamp())

    df_hist = (
            df.withColumn("hist_bin", F.sql_expr(f"""
                        width_bucket( {col_name}, min({col_name}) over (partition by null), max({col_name}+1) over (partition by null),{bins_arg}) """))
            .group_by("hist_bin")
            .count()
            .sort("hist_bin")
        )
    rows = df_hist.collect()
    print("Rows"+str(rows))
    hist_counts = [0] * bins_arg
    for idx, r in enumerate(rows):
        if r["HIST_BIN"]:
            hist_counts[r["HIST_BIN"]-1] = r["COUNT"]

    if summary["max"]:
        step = (summary["max"] - summary["min"]) / bins_arg
        bin_edges = [get_timestamp(summary["min"] + i * step) for i in range(bins_arg + 1)]
    else:
        bin_edges=[0] * bins_arg

    summary["histogram"] = (array(hist_counts), array(bin_edges))

    print(f"Summary histogram:"+str(summary["histogram"]))

    return config, df, summary
