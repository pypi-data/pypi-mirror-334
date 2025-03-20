use crate::ast::ColumnLike;
use crate::{PysparkTranspileContext, PythonCode, ToSparkQuery};

#[derive(Debug, PartialEq, Clone, Hash)]
pub enum ColumnOrName {
    Column(ColumnLike),
    Name(String),
}

impl From<String> for ColumnOrName {
    fn from(val: String) -> Self {
        ColumnOrName::Name(val)
    }
}

impl From<ColumnLike> for ColumnOrName {
    fn from(val: ColumnLike) -> Self {
        ColumnOrName::Column(val)
    }
}

impl ToSparkQuery for ColumnOrName {
    fn to_spark_query(&self, ctx: &PysparkTranspileContext) -> anyhow::Result<PythonCode> {
        match self {
            ColumnOrName::Column(col) => col.to_spark_query(ctx),
            ColumnOrName::Name(name) => Ok(format!("\"{}\"", name).into()),
        }
    }
}
