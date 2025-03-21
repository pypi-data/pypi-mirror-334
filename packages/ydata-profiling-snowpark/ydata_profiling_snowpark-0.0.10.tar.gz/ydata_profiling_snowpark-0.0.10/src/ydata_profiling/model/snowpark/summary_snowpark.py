"""Compute statistical description of datasets."""
import multiprocessing
from typing import Tuple

import numpy as np
from snowflake.snowpark import DataFrame
from snowflake.snowpark.types import ArrayType
from tqdm import tqdm
from visions import VisionsTypeset


from ydata_profiling.config import Settings
from ydata_profiling.model.summarizer import BaseSummarizer
from ydata_profiling.model.summary import describe_1d, get_series_descriptions
from ydata_profiling.utils.dataframe import sort_column_names


@describe_1d.register
def spark_describe_1d(
    config: Settings,
    series: DataFrame,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
) -> dict:
    """Describe a series (infer the variable type, then calculate type-specific values).

    Args:
        config: report Settings object
        series: The Series to describe.
        summarizer: Summarizer object
        typeset: Typeset

    Returns:
        A Series containing calculated series description values.
    """

    # Make sure pd.NA is not in the series
    series = series.fillna(np.nan)

    # get `infer_dtypes` (bool) from config
    if config.infer_dtypes:
        # Infer variable types
        vtype = typeset.infer_type(series)
        series = typeset.cast_to_inferred(series)
    else:
        # Detect variable types from pandas dataframe (df.dtypes).
        # [new dtypes, changed using `astype` function are now considered]

        if isinstance(series.schema.fields[0].datatype, ArrayType):
            dtype = "ArrayType"
        else:
            dtype =  type(series.schema.fields[0].datatype).__name__

        vtype = {
            "float": "Numeric",
            "int": "Numeric",
            "bigint": "Numeric",
            "LongType": "Numeric",
            "double": "Numeric",
            "DoubleType": "Numeric",
            "DecimalType": "Numeric",
            "string": "Categorical",
            "StringType": "Categorical",
            "ArrayType": "Categorical",
            "boolean": "Boolean",
            "BooleanType": "Boolean",
            "date": "DateTime",
            "DateType": "DateTime",
            "timestamp": "DateTime",
            "TimestampType": "DateTime"
        }[dtype]

    return summarizer.summarize(config, series, dtype=vtype)


@get_series_descriptions.register
def spark_get_series_descriptions(
    config: Settings,
    df: DataFrame,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    pbar: tqdm,
) -> dict:
    series_description = {}

    def multiprocess_1d(args: tuple) -> Tuple[str, dict]:
        """Wrapper to process series in parallel.

        Args:
            column: The name of the column.
            series: The series values.

        Returns:
            A tuple with column and the series description.
        """
        column, df = args
        return column, describe_1d(config, df.select(column), summarizer, typeset)

    # Rename the df column names to prevent potential conflicts
    for col in df.columns:
        df = df.withColumnRenamed(col, f"{col}_CUSTOMER")

    columns = df.limit(1).toPandas().columns

    args = [(name, df) for name in columns]
    with multiprocessing.pool.ThreadPool(12) as executor:
        for i, (column, description) in enumerate(
            executor.imap_unordered(multiprocess_1d, args)
        ):
            if column.endswith("_CUSTOMER"):
                column = column[:-9]
            pbar.set_postfix_str(f"Describe variable:{column}")

            # summary clean up for spark
            description.pop("value_counts")

            series_description[column] = description
            pbar.update()
        series_description = {k[:-9]: series_description[k[:-9]] for k in columns}

    # Mapping from column name to variable type
    series_description = sort_column_names(series_description, config.sort)

    return series_description
