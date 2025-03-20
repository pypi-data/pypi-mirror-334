use crate::ast::ColumnLike::FunctionCall;
use crate::ast::*;
use crate::base::{PysparkTranspileContext, ToSparkExpr};
use crate::functions::stat_fns::stats_fn;
use anyhow::{bail, ensure};
use spl_transpiler_common::aliasable::Aliasable;
use spl_transpiler_spl::ast;
use spl_transpiler_spl::commands::stats_utils::MaybeSpannedField;

pub fn transform_by_field(f: MaybeSpannedField) -> ColumnOrName {
    match f.clone() {
        MaybeSpannedField {
            field: ast::Field(field),
            span: None,
        } => ColumnOrName::Name(field),
        MaybeSpannedField {
            field: ast::Field(field),
            span: Some(span),
        } => {
            let span_text = format!("{} {}", span.value, span.scale);
            column_like!(window([py_lit(field)], [py_lit(span_text)])).into()
        }
    }
}

pub fn transform_stats_expr(
    df: DataFrame,
    expr: &ast::Expr,
    ctx: &PysparkTranspileContext,
) -> anyhow::Result<(DataFrame, ColumnLike)> {
    let (e, maybe_name) = expr.clone().unaliased_with_name();
    ensure!(
        matches!(e, ast::Expr::Call(_)),
        "All `stats` aggregations must be function calls"
    );
    let (df_, e) = stats_fn(e, df, ctx)?;
    Ok((df_, e.maybe_with_alias(maybe_name)))
}

pub fn transform_stats_runtime_expr(
    expr: &ast::Expr,
    ctx: &PysparkTranspileContext,
) -> anyhow::Result<(String, RuntimeExpr)> {
    let (e, maybe_name) = expr.clone().unaliased_with_name();
    let (name, args) = match e {
        ast::Expr::Call(ast::Call { name, args }) => (name.to_string(), args),
        _ => bail!(
            "All `stats` aggregations must be function calls, got {:?}",
            expr
        ),
    };
    let alias = maybe_name.unwrap_or(name.clone());
    let args: anyhow::Result<Vec<Expr>> = args
        .into_iter()
        .map(|e| e.with_context(ctx).try_into())
        .collect();
    let expr: Expr = FunctionCall {
        func: format!("functions.stats.{}", name).to_string(),
        args: args?,
    }
    .into();
    Ok((alias, RuntimeExpr::from(expr)))
}
