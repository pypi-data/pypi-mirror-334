use crate::ast::ColumnLike;
use crate::ast::ColumnOrName;
use crate::ast::DataFrame;
use crate::ast::Expr;
use crate::ast::PyDict;
use crate::ast::PyList;
use crate::ast::PyLiteral;
use crate::ast::PyRuntimeFunc;
use crate::{ContextualizedExpr, PysparkTranspileContext, PythonCode, ToSparkExpr, ToSparkQuery};

#[derive(Debug, PartialEq, Clone, Hash)]
pub enum RuntimeExpr {
    DataFrame(Box<DataFrame>),
    Expr(Expr),
    PyDict(PyDict),
    PyList(PyList),
    PyRuntimeFunc(PyRuntimeFunc),
}

impl From<DataFrame> for RuntimeExpr {
    fn from(val: DataFrame) -> Self {
        RuntimeExpr::DataFrame(Box::new(val))
    }
}

impl<E: Into<Expr>> From<E> for RuntimeExpr {
    fn from(val: E) -> Self {
        RuntimeExpr::Expr(val.into())
    }
}

impl<E: ToSparkExpr> TryFrom<ContextualizedExpr<E>> for RuntimeExpr {
    type Error = anyhow::Error;
    fn try_from(val: ContextualizedExpr<E>) -> anyhow::Result<Self, Self::Error> {
        let expr: Expr = val.try_into()?;
        Ok(expr.into())
    }
}

impl From<ColumnOrName> for RuntimeExpr {
    fn from(val: ColumnOrName) -> Self {
        match val {
            ColumnOrName::Column(col) => RuntimeExpr::from(col),
            ColumnOrName::Name(name) => RuntimeExpr::Expr(Expr::Column(ColumnLike::Named { name })),
        }
    }
}

impl From<PyDict> for RuntimeExpr {
    fn from(val: PyDict) -> Self {
        RuntimeExpr::PyDict(val)
    }
}

impl From<PyList> for RuntimeExpr {
    fn from(val: PyList) -> Self {
        RuntimeExpr::PyList(val)
    }
}

impl From<PyRuntimeFunc> for RuntimeExpr {
    fn from(val: PyRuntimeFunc) -> Self {
        RuntimeExpr::PyRuntimeFunc(val)
    }
}

impl<T: Into<RuntimeExpr>> From<Option<T>> for RuntimeExpr {
    fn from(val: Option<T>) -> Self {
        match val {
            Some(val) => val.into(),
            None => RuntimeExpr::Expr(PyLiteral("None".into()).into()),
        }
    }
}

impl ToSparkQuery for RuntimeExpr {
    fn to_spark_query(&self, ctx: &PysparkTranspileContext) -> anyhow::Result<PythonCode> {
        match self {
            RuntimeExpr::DataFrame(val) => val.to_spark_query(ctx),
            RuntimeExpr::Expr(val) => val.to_spark_query(ctx),
            RuntimeExpr::PyDict(val) => val.to_spark_query(ctx),
            RuntimeExpr::PyList(val) => val.to_spark_query(ctx),
            RuntimeExpr::PyRuntimeFunc(val) => val.to_spark_query(ctx),
        }
    }
}
