from pyspark.sql import DataFrame

from pyspark_spl_tools.base import enforce_types, Expr


@enforce_types
def spath(
    df: DataFrame, path: str, *, input_: Expr = "raw", output: Expr | None = None
) -> DataFrame:
    pass
