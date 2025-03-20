use crate::ast::Expr;
use crate::base::ToSparkExpr;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use spl_transpiler_spl::commands::cmd::where_::WhereCommand;

impl PipelineTransformer for WhereCommand {
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let mut df = state.df.clone().unwrap_or_default();

        let condition: Expr = self.expr.clone().with_context(&state.ctx).try_into()?;
        df = df.where_(condition);

        Ok(state.with_df(df))
    }
}
