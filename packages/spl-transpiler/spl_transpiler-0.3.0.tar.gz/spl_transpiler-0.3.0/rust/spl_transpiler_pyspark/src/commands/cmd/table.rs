use crate::ast::*;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use spl_transpiler_spl::commands::cmd::table::TableCommand;

impl PipelineTransformer for TableCommand {
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let mut df = state.df.clone().unwrap_or_default();

        df = df.select(
            self.fields
                .iter()
                .map(|field| column_like!(col(field.0.clone())))
                .collect(),
        );

        Ok(state.with_df(df))
    }
}
