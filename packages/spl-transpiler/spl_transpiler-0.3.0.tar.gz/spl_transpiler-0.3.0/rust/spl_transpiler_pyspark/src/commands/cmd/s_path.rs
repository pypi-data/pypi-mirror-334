use crate::ast::*;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use spl_transpiler_spl::commands::cmd::s_path::*;

impl PipelineTransformer for SPathCommand {
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let mut df = state.df.clone().unwrap_or_default();

        let output_name = self.output.clone().unwrap_or(self.path.clone());

        df = df.with_column(
            output_name,
            column_like!(get_json_object(
                [col(self.input.clone())],
                [py_lit(format!("$.{}", self.path.clone()))]
            )),
        );

        Ok(state.with_df(df))
    }
}

#[cfg(test)]
mod tests {
    use crate::utils::test::generates;
    use rstest::rstest;

    #[rstest]
    fn test_spath_1() {
        generates(
            r#"spath input=x output=y key.subkey"#,
            r#"table_source(spark, index="main").withColumn(
                "y",
                F.get_json_object(F.col("x"), "$.key.subkey")
            )"#,
        );
    }
}
