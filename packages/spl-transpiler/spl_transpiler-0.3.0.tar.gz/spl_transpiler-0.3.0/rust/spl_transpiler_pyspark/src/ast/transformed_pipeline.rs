use crate::ast::DataFrame;
use crate::{PysparkTranspileContext, PythonCode, ToSparkQuery};
use anyhow::ensure;

#[derive(Debug, PartialEq, Clone, Hash)]
pub struct TransformedPipeline {
    pub dataframes: Vec<DataFrame>,
}

impl ToSparkQuery for TransformedPipeline {
    fn to_spark_query(&self, ctx: &PysparkTranspileContext) -> anyhow::Result<PythonCode> {
        let dfs: anyhow::Result<Vec<String>> = self
            .dataframes
            .iter()
            .map(|df| df.to_spark_query(ctx).map(|code| code.to_string()))
            .collect();
        Ok(dfs?.join("\n\n").into())
    }
}

impl TryInto<DataFrame> for TransformedPipeline {
    type Error = anyhow::Error;
    fn try_into(self) -> anyhow::Result<DataFrame, Self::Error> {
        ensure!(
            self.dataframes.len() == 1,
            "Unable to map over multi-dataframe pipelines"
        );
        Ok(self.dataframes.first().unwrap().clone())
    }
}
