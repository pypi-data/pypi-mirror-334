use crate::ast::*;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use spl_transpiler_spl::ast;
use spl_transpiler_spl::ast::FieldOrAlias;
use spl_transpiler_spl::commands::cmd::bin::*;

impl PipelineTransformer for BinCommand {
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let mut df = state.df.clone().unwrap_or_default();
        let col_name = match self.field.clone() {
            FieldOrAlias::Field(ast::Field(name)) => name,
            FieldOrAlias::Alias(ast::Alias { name, .. }) => name,
        };
        if let Some(ast::TimeSpan { value, scale }) = self.span.clone() {
            let span = format!("{} {}", value, scale);
            df = df.with_column(
                col_name.clone(),
                column_like!(window([col(col_name.clone())], [py_lit(span)])),
            );
        }
        let subfield = "start";
        df = df.with_column(
            col_name.clone(),
            column_like!(col(format!("`{}`.`{}`", col_name, subfield))),
        );
        Ok(state.with_df(df))
    }
}

#[cfg(test)]
mod tests {
    use crate::utils::test::generates;

    #[test]
    fn test_bin_command_transform_standalone() {
        generates(
            r#"index=main | bucket span=10m _time"#,
            r#"
table_source(spark, index="main").withColumn(
    "_time",
    F.window(F.col("_time"), "10 minutes")
).withColumn(
    "_time",
    F.col("`_time`.`start`")
)
            "#,
        );
    }
}
