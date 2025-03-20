use crate::ast::column_like;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use anyhow::ensure;
use spl_transpiler_spl::commands::cmd::mv_expand::MvExpandCommand;

impl PipelineTransformer for MvExpandCommand {
    #[allow(unused_variables, unreachable_code)]
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let df = state.df.clone().unwrap_or_default();

        ensure!(self.limit.is_none(), "Cannot limit `F.explode`");

        let df = df.with_column(
            self.field.0.clone(),
            column_like!(explode([col(self.field.0.clone())])),
        );

        Ok(state.with_df(df))
    }
}

#[cfg(test)]
mod tests {
    use crate::utils::test::generates;
    use rstest::rstest;

    #[rstest]
    fn test_mv_expand_1() {
        generates(
            r#"index=main | mvexpand key_policy_statements"#,
            r#"
table_source(spark, index="main").withColumn(
    "key_policy_statements",
    F.explode(F.col("key_policy_statements"))
)"#,
        )
    }
}
