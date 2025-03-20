use crate::ast::ColumnLike;
use crate::ast::PyLiteral;
use crate::{PysparkTranspileContext, PythonCode, ToSparkQuery};

#[derive(Debug, PartialEq, Clone, Hash)]
// #[pyclass(frozen,eq,hash)]
pub enum Expr {
    Column(ColumnLike),
    PyLiteral(PyLiteral),
}

impl ToSparkQuery for Expr {
    fn to_spark_query(&self, ctx: &PysparkTranspileContext) -> anyhow::Result<PythonCode> {
        match self {
            Expr::Column(col @ ColumnLike::BinaryOp { .. }) => {
                Ok(format!("({})", col.to_spark_query(ctx)?,).into())
            }
            Expr::Column(col) => col.to_spark_query(ctx),
            Expr::PyLiteral(literal) => literal.to_spark_query(ctx),
        }
    }
}

impl From<ColumnLike> for Expr {
    fn from(val: ColumnLike) -> Self {
        Expr::Column(val)
    }
}

impl From<PyLiteral> for Expr {
    fn from(val: PyLiteral) -> Self {
        Expr::PyLiteral(val)
    }
}

impl TryInto<ColumnLike> for Expr {
    type Error = anyhow::Error;
    fn try_into(self) -> anyhow::Result<ColumnLike, Self::Error> {
        match self {
            Expr::Column(col) => Ok(col),
            _ => Err(anyhow::anyhow!("Expected ColumnLike, got {:?}", self)),
        }
    }
}
