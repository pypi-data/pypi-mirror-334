use crate::functions::convert_fns::convert_fn;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use spl_transpiler_spl::ast;
use spl_transpiler_spl::commands::cmd::convert::*;

impl PipelineTransformer for ConvertCommand {
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let mut df = state.df.clone().unwrap_or_default();

        for conv in self.convs.iter().cloned() {
            let (result, input_field) = convert_fn(self, &conv)?;
            let FieldConversion {
                field: ast::Field(name),
                alias,
                ..
            } = conv;
            let name = alias.map(|f| f.0).unwrap_or(name);
            df = df.with_column_maybe(name, result, input_field)
        }
        Ok(state.with_df(df))
    }
}

#[cfg(test)]
mod tests {
    use crate::utils::test::generates;
    use rstest::rstest;

    #[rstest]
    fn test_convert_command() {
        generates(
            r#"convert timeformat="%Y-%m-%dT%H:%M:%S" ctime(firstTime)"#,
            r#"
from pyspark_spl_tools.monkeypatches import install_monkeypatches
install_monkeypatches()

table_source(spark, index="main")._spltranspiler__withColumnMaybe(
    'firstTime',
    F.date_format(F.col("firstTime"), "yyyy-MM-dd'T'HH:mm:ss"),
    'firstTime'
)
            "#,
        )
    }
}
