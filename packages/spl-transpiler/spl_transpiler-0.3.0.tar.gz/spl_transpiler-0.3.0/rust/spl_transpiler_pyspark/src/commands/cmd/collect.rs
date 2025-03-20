use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use anyhow::bail;
use spl_transpiler_spl::commands::cmd::collect::*;

impl PipelineTransformer for CollectCommand {
    #[allow(unused_variables, unreachable_code)]
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        bail!("UNIMPLEMENTED")
    }
}
