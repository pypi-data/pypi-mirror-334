use crate::ast::*;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use spl_transpiler_spl::ast;
use spl_transpiler_spl::commands::cmd::fields::*;

impl PipelineTransformer for FieldsCommand {
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let mut df = state.df.clone().unwrap_or_default();

        let cols: Vec<_> = self
            .fields
            .iter()
            .map(|ast::Field(name)| column_like!(col(name)))
            .collect();

        df = df.select(cols);

        Ok(state.with_df(df))
    }
}
