use crate::ast::column_like;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use spl_transpiler_spl::commands::cmd::mv_combine::MvCombineCommand;

impl PipelineTransformer for MvCombineCommand {
    #[allow(unused_variables, unreachable_code)]
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let df = state.df.clone().unwrap_or_default();

        let delimiter = self.delim.clone().unwrap_or(" ".into());
        let df = df.with_column(
            self.field.0.clone(),
            column_like!(array_join([col(self.field.0.clone())], [py_lit(delimiter)])),
        );

        Ok(state.with_df(df))
    }
}

#[cfg(test)]
mod tests {
    use crate::utils::test::generates;
    use rstest::rstest;

    #[rstest]
    fn test_mv_combine_1() {
        generates(
            r#"index=main | mvcombine foo"#,
            r#"
table_source(spark, index="main").withColumn(
    "foo",
    F.array_join(F.col("foo"), " ")
)"#,
        )
    }

    #[rstest]
    fn test_mv_combine_2() {
        generates(
            r#"index=main | mvcombine delim=":" foo"#,
            r#"
table_source(spark, index="main").withColumn(
    "foo",
    F.array_join(F.col("foo"), ":")
)"#,
        )
    }
}
