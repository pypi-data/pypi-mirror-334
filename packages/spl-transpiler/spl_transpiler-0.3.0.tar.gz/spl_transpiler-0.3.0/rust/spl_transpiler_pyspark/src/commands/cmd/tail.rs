use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use spl_transpiler_spl::commands::cmd::tail::TailCommand;

impl PipelineTransformer for TailCommand {
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let mut df = state.df.clone().unwrap_or_default();

        df = df.tail(self.n);

        Ok(state.with_df(df))
    }
}
