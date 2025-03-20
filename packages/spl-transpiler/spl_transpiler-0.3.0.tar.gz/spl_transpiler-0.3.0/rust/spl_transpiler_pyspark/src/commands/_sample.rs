//noinspection RsDetachedFile
use super::spl::*;
use crate::ast::*;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use anyhow::bail;
use spl_transpiler_spl::ast;

impl PipelineTransformer for SAMPLECommand {
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let mut df = state.df.clone().unwrap_or_default();

        bail!("UNIMPLEMENTED");

        Ok(state.with_df(df))
    }
}
