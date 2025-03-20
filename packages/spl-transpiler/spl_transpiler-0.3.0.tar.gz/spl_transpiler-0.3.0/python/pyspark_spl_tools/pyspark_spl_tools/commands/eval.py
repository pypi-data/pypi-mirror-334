from pyspark.sql import DataFrame

from pyspark_spl_tools.base import enforce_types, Expr


@enforce_types
def eval(df: DataFrame, **exprs: Expr) -> DataFrame:
    return df.withColumns(
        {name: expr.to_pyspark_expr() for name, expr in exprs.items()}
    )
