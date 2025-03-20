use crate::ast::*;
use crate::base::{PysparkTranspileContext, ToSparkExpr};
use crate::functions::eval_fns::eval_fn;
use crate::transpiler::ilike::AsLikeString;
use crate::transpiler::utils::join_as_binaries;
use anyhow::{anyhow, bail};
use phf::phf_map;
use regex::Regex;
use spl_transpiler_common::aliasable::Aliasable;
use spl_transpiler_spl::ast;

static SIMPLE_OP_MAP: phf::Map<&'static str, &'static str> = phf_map! {
    "=" => "==",
    "AND" => "&",
    "OR" => "|",
    "NOT" => "~",
};

impl ToSparkExpr for ast::Expr {
    fn to_spark_expr(&self, ctx: &PysparkTranspileContext) -> anyhow::Result<Expr> {
        match self.clone() {
            // Binary operation -> Binary op
            ast::Expr::Binary(ast::Binary {
                left,
                symbol,
                right,
            }) => match (
                *left,
                SIMPLE_OP_MAP
                    .get(symbol.as_str())
                    .cloned()
                    .unwrap_or(symbol.as_str()),
                *right,
            ) {
                // src_ip = 10.0.0.0/16 -> F.expr("cidr_match('10.0.0.0/16', src_ip)")
                (
                    ast::Expr::Leaf(ast::LeafExpr::Constant(ast::Constant::Field(ast::Field(col)))),
                    "==",
                    ast::Expr::Leaf(ast::LeafExpr::Constant(ast::Constant::IPv4CIDR(
                        ast::IPv4CIDR(cidr),
                    ))),
                ) => Ok(column_like!(expr("cidr_match('{}', {})", cidr, col)).into()),
                // src_ip = "x*" -> F.like(F.col("src_ip"), "x%"),
                (
                    lhs,
                    op,
                    ast::Expr::Leaf(ast::LeafExpr::Constant(ast::Constant::Wildcard(
                        wildcard @ ast::Wildcard(..),
                    ))),
                ) => {
                    let lhs: Expr = lhs.with_context(ctx).try_into()?;
                    let match_wildcard =
                        column_like!([lhs].ilike([py_lit(wildcard.as_like_string())]));
                    match op {
                        "=" => Ok(match_wildcard.into()),
                        "==" => Ok(match_wildcard.into()),
                        "!=" => Ok(column_like!(~[match_wildcard]).into()),
                        _ => bail!("Unsupported comparison operator for wildcard rhs: {}", op),
                    }
                }
                // a [op] b -> a [op] b
                (left, op, right) => Ok(ColumnLike::try_binary_op(
                    left.with_context(ctx),
                    op,
                    right.with_context(ctx),
                )?
                .into()),
            },

            // Unary operation -> Unary op
            ast::Expr::Unary(ast::Unary { symbol, right }) if symbol == "NOT" => {
                Ok(ColumnLike::try_unary_not((*right).with_context(ctx))?.into())
            }

            // Field -> Named column
            ast::Expr::Leaf(ast::LeafExpr::Constant(ast::Constant::Field(ast::Field(name)))) => {
                Ok(ColumnLike::named(name.clone()).into())
            }

            // Int constant -> Int literal column
            ast::Expr::Leaf(ast::LeafExpr::Constant(ast::Constant::Int(ast::IntValue(val)))) => {
                Ok(ColumnLike::literal(val).into())
            }

            // Double constant -> Double literal column
            ast::Expr::Leaf(ast::LeafExpr::Constant(ast::Constant::Double(ast::DoubleValue(
                val,
            )))) => Ok(ColumnLike::literal(val).into()),

            // String constant -> String literal column
            ast::Expr::Leaf(ast::LeafExpr::Constant(ast::Constant::Str(ast::StrValue(val)))) => {
                Ok(ColumnLike::string_literal(val).into())
            }

            // Boolean constant -> Boolean literal column
            ast::Expr::Leaf(ast::LeafExpr::Constant(ast::Constant::Bool(ast::BoolValue(val)))) => {
                Ok(ColumnLike::from(val).into())
            }

            // IPv4 cidr -> String literal column
            ast::Expr::Leaf(ast::LeafExpr::Constant(ast::Constant::IPv4CIDR(ast::IPv4CIDR(
                val,
            )))) => Ok(ColumnLike::string_literal(val).into()),

            // 'x in ("a", "b*", c)' -> Binary op tree of OR's of individual checks
            // "a" -> { col("x") == "a" }
            // "b*" -> { col("x").like("b%") }
            // ...
            ast::Expr::FieldIn(ast::FieldIn { field, exprs }) => {
                let c: Expr = column_like!(col(field.clone())).into();
                let checks: anyhow::Result<Vec<ColumnLike>> = exprs
                    .iter()
                    .map(|expr| match expr {
                        ast::Expr::Leaf(ast::LeafExpr::Constant(ast::Constant::Wildcard(
                            val @ ast::Wildcard(..),
                        ))) => Ok(column_like!(
                            [c.clone()].ilike([py_lit(val.as_like_string())])
                        )),
                        _ => {
                            let pyspark_expr = expr.clone().with_context(ctx).try_into()?;
                            match pyspark_expr {
                                Expr::Column(rhs) => Ok(column_like!([c.clone()] == [rhs])),
                                _ => Err(anyhow!(
                                    "Non column-like expression found in FieldIn rhs: {:?}",
                                    expr
                                )),
                            }
                        }
                    })
                    .collect();
                let checks = checks?;
                Ok(join_as_binaries("|", checks)
                    .unwrap_or(column_like!(lit(true)))
                    .into())
                // Ok(match checks.len() {
                //     0 => column_like!(lit(true)).into(),
                //     1 => checks[0].clone().into(),
                //     2 => column_like!([checks[0].clone()] | [checks[1].clone()]).into(),
                //     _ => {
                //         let mut left = checks[0].clone();
                //         for check in &checks[1..] {
                //             left = column_like!([left] | [check.clone()]).into();
                //         }
                //         left
                //     }
                // }.into())
            }

            ast::Expr::Call(call @ ast::Call { .. }) => Ok(eval_fn(call, ctx)?.into()),

            _ => Err(anyhow!("Unsupported expression: {:?}", self)),
        }
    }
}

impl Expr {
    fn _into_search_expr(self) -> Self {
        match self {
            Expr::Column(ref c) => c.clone().into_search_expr().into(),
            Expr::PyLiteral(_) => self,
        }
    }

    pub fn into_search_expr(self) -> Self {
        let (expr, name) = self.unaliased_with_name();
        let transformed_expr = expr._into_search_expr();
        transformed_expr.maybe_with_alias(name)
    }
}

impl ColumnLike {
    fn _into_search_expr(self) -> Self {
        match self {
            ColumnLike::Named { name } => {
                column_like!([col("_raw")].ilike([py_lit(format!("%{}%", name))]))
            }
            ColumnLike::Literal { code } => {
                column_like!([col("_raw")]
                    .ilike([py_lit(format!("%{}%", Self::_strip_quotes(code.as_str())))]))
            }

            ColumnLike::UnaryNot { right } => ColumnLike::UnaryNot {
                right: Box::new(right._into_search_expr()),
            },
            ColumnLike::BinaryOp { left, op, right } if matches!(op.as_str(), "&" | "|") => {
                ColumnLike::binary_op(left._into_search_expr(), op, right._into_search_expr())
            }
            _ => self,
        }
    }

    fn _strip_quotes(code: &str) -> &str {
        let re_double: Regex = Regex::new(r#"^".+"$"#).unwrap();
        let re_single: Regex = Regex::new(r#"^'.+'$"#).unwrap();
        if re_double.is_match(code) | re_single.is_match(code) {
            &code[1..code.len() - 1]
        } else {
            code
        }
    }

    pub fn into_search_expr(self) -> Self {
        let (expr, name) = self.unaliased_with_name();
        let transformed_expr = expr._into_search_expr();
        transformed_expr.maybe_with_alias(name)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    #[rstest]
    fn test_expr_into_search_expr() {
        assert_eq!(
            column_like!([col("A")] == [py_lit(5)]).into_search_expr(),
            column_like!([col("A")] == [py_lit(5)]),
        );
        assert_eq!(
            column_like!(col("A")).into_search_expr(),
            column_like!([col("_raw")].ilike([py_lit("%A%")])),
        );
        assert_eq!(
            column_like!(lit("A")).into_search_expr(),
            column_like!([col("_raw")].ilike([py_lit("%A%")])),
        );
        assert_eq!(
            column_like!([col("A")] & [lit("B")]).into_search_expr(),
            column_like!(
                [[col("_raw")].ilike([py_lit("%A%")])] & [[col("_raw")].ilike([py_lit("%B%")])]
            ),
        );
    }
}
