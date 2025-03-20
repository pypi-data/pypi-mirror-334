from pyspark.sql import DataFrame

from pyspark_spl_tools.base import enforce_types, Expr
from pyspark_spl_tools.functions.stats import StatsFunction
from pyspark_spl_tools.monkeypatches import groupByMaybeExploded


@enforce_types
def stats(
    df: DataFrame,
    *,
    by: list[Expr] = (),
    **stat_exprs: StatsFunction,
) -> DataFrame:
    aggs = []
    for label, expr in stat_exprs.items():
        df, agg_expr = expr.to_pyspark_expr(df)
        aggs.append(agg_expr.alias(label))

    df = groupByMaybeExploded(df, [v.to_pyspark_expr() for v in by])
    df = df.agg(*aggs)

    return df
