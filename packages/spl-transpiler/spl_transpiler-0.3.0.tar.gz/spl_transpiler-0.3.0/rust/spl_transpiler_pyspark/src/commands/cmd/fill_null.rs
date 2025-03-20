use crate::ast::*;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use spl_transpiler_spl::commands::cmd::fill_null::FillNullCommand;

impl PipelineTransformer for FillNullCommand {
    fn transform_for_runtime(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let df = DataFrame::runtime(
            state.df.clone(),
            "fill_null",
            vec![],
            py_dict! {
                value=PyLiteral::from(self.value.clone()),
                fields=self.fields.clone().map(|fs| PyList(fs.into_iter().map(|f| PyLiteral::from(f.0).into()).collect()))
            }.0,
            &state.ctx,
        );

        Ok(state.with_df(df))
    }

    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let df = state.df.clone().unwrap_or_default();

        let df = df.dataframe_method(
            "fillna",
            vec![column_like!(py_lit(self.value.clone())).into()],
            vec![],
        );

        Ok(state.with_df(df))
    }
}

#[cfg(test)]
mod tests {
    use crate::utils::test::{generates, generates_runtime};
    use rstest::rstest;

    #[rstest]
    fn test_fill_null_1() {
        generates(
            r#"fillnull value=NULL"#,
            r#"table_source(spark, index="main").fillna("NULL")"#,
        )
    }

    #[rstest]
    fn test_fill_null_2() {
        generates_runtime(
            r#"fillnull value=NULL"#,
            r#"
df_1 = commands.fill_null(None, value='NULL', fields=None)
df_1
            "#,
        )
    }
}
