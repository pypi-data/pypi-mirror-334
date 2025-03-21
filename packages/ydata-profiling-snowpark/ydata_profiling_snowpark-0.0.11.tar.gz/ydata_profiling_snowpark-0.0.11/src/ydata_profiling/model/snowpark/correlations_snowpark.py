"""Correlations between variables."""
from typing import Optional
from typing import Tuple, List

import pandas as pd
import phik

from packaging import version
import snowflake.snowpark as sp
from snowflake.snowpark import Session, DataFrame
from snowflake.snowpark import functions as F
from snowflake.snowpark.types import (
    StructType,
    StructField,
    DoubleType,
    StringType, 
    ArrayType
)

from requests.structures import CaseInsensitiveDict as cidict

from ydata_profiling.config import Settings
from ydata_profiling.model.correlations import Cramers, Kendall, Pearson, PhiK, Spearman

SPARK_CORRELATION_PEARSON = "pearson"
SPARK_CORRELATION_SPEARMAN = "spearman"


@Spearman.compute.register(Settings, DataFrame, dict)
def snowpark_spearman_compute(
    config: Settings, df: DataFrame, summary: dict
) -> Optional[pd.DataFrame]:

    raise NotImplementedError("Spearman correlation is not supported in Snowpark")


@Pearson.compute.register(Settings, DataFrame, dict)
def snowpark_pearson_compute(
    config: Settings, df: DataFrame, summary: dict
) -> Optional[pd.DataFrame]:

    # Get the numerical cols for index and column names
    # Spark only computes Pearson natively for the above dtypes
    matrix, num_cols = _compute_snowpark_corr_natively(
        df, summary, corr_type=SPARK_CORRELATION_PEARSON
    )
    return pd.DataFrame(matrix, index=num_cols, columns=num_cols)

def _compute_snowpark_corr_natively(
    df, summary: dict, corr_type: str
):
    if corr_type.lower() != "pearson":
        raise NotImplementedError(
            f"Snowpark only provides a built-in Pearson correlation. '{corr_type}' is not supported."
        )

    variables = {column: description["type"] for column, description in summary.items()}
    interval_columns = [
        column for column, type_name in variables.items() if type_name == "Numeric"
    ]

    # If you have zero or one numeric column, correlation matrix is trivial
    if len(interval_columns) <= 1:
        # Return a 0x0 or 1x1 matrix (depending on your preference)
        return [], interval_columns

    n = len(interval_columns)
    # Build an n x n matrix initialized to None (or 1.0 for diagonal if you want)
    corr_matrix = [[None for _ in range(n)] for _ in range(n)]

    # Fill the diagonal with 1.0
    for i in range(n):
        corr_matrix[i][i] = 1.0

    # For each pair of columns, compute correlation
    for i in range(n):
        for j in range(i + 1, n):
            col_i = interval_columns[i]
            col_j = interval_columns[j]

            # Snowpark corr usage: df.agg(corr(col("a"), col("b")))
            # .collect() returns a list of Row objects; pick first row and first column
            result = df.agg(F.corr(F.col(col_i), F.col(col_j))).collect()
            # result looks like [Row(CORR(A,B)=0.813...), ...]

            corr_value = result[0][0] if result and result[0] else None

            # Place the value symmetrically in the matrix
            corr_matrix[i][j] = corr_value
            corr_matrix[j][i] = corr_value

    return corr_matrix, interval_columns

