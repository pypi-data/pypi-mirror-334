mod column_like;
mod column_or_name;
mod dataframe;
mod expr;
mod py_dict;
mod py_list;
mod py_literal;
mod py_runtime_func;
mod runtime_expr;
mod transformed_pipeline;

pub use column_like::*;
pub use column_or_name::*;
pub use dataframe::*;
pub use expr::*;
pub use py_dict::*;
pub use py_list::*;
pub use py_literal::*;
pub use py_runtime_func::*;
pub use runtime_expr::*;
pub use transformed_pipeline::*;

#[cfg(test)]
mod tests {
    use super::*;
    use crate::base::test::test_pyspark_transpile_context;
    use crate::base::RuntimeSelection;
    use crate::utils::test::assert_python_code_eq;
    use crate::{PysparkTranspileContext, ToSparkExpr, ToSparkQuery};
    use rstest::rstest;
    use spl_transpiler_python_formatter::format_python_code;

    fn generates(ast: impl ToSparkQuery, code: impl ToString) {
        let ctx = test_pyspark_transpile_context(RuntimeSelection::Disallow);
        let generated = ast.to_spark_query(&ctx).expect("Failed to generate code");
        let formatted_generated = format_python_code(generated.to_string().replace(",)", ")"))
            .expect("Failed to format rendered Spark query");
        let formatted_code = format_python_code(code.to_string().replace(",)", ")"))
            .expect("Failed to format target code");
        assert_eq!(formatted_generated, formatted_code);
    }

    #[rstest]
    fn test_column_like() {
        generates(column_like!(col("x")), r#"F.col("x")"#);
        generates(column_like!(lit(42)), r#"F.lit(42)"#);
        generates(column_like!([lit(42)].sqrt()), r#"F.lit(42).sqrt()"#);
        generates(column_like!(lit("xyz")), r#"F.lit("xyz")"#);
        generates(column_like!(sqrt([lit(42)])), r#"F.sqrt(F.lit(42))"#);
        generates(
            column_like!([col("x")].alias("y")),
            r#"F.col("x").alias("y")"#,
        );
        generates(
            column_like!([col("x")] + [lit(42)]),
            r#"F.col("x") + F.lit(42)"#,
        );
        generates(
            ColumnLike::unary_not(ColumnLike::named("x")),
            r#"~F.col("x")"#,
        )
    }

    #[rstest]
    fn test_dataframe() {
        generates(
            DataFrame::source_index("main").where_(column_like!(col("x"))),
            r#"table_source(spark, index="main").where(F.col("x"))"#,
        )
    }

    #[rstest]
    fn test_with_aliased_column() {
        generates(
            DataFrame::source_index("main").with_column(
                "final_name",
                column_like!([col("orig_name")].alias("alias_name")),
            ),
            r#"table_source(spark, index="main").withColumn("final_name", F.col("orig_name"))"#,
        )
    }

    #[rstest]
    fn test_named() {
        let ctx = test_pyspark_transpile_context(RuntimeSelection::Disallow);
        generates(
            DataFrame::source_index("main")
                .with_column(
                    "final_name",
                    column_like!([col("orig_name")].alias("alias_name")),
                )
                .named(Some("prev".to_string()), &ctx),
            r#"
prev = table_source(spark, index="main").withColumn("final_name", F.col("orig_name"))
prev
            "#,
        )
    }

    #[rstest]
    fn test_unique_ids() {
        let ctx = test_pyspark_transpile_context(RuntimeSelection::Disallow);
        let df_1 = DataFrame::runtime(
            // None,
            None,
            "search".to_string(),
            vec![column_like!([col("x")] == [lit(3)]).into()],
            vec![],
            &ctx,
        );
        let df_2 = DataFrame::runtime(
            Some(df_1),
            "eval".to_string(),
            vec![],
            vec![("y".to_string(), column_like!(length([col("x")])).into())],
            &ctx,
        );
        assert_python_code_eq(
            df_2.to_spark_query(&ctx).unwrap().to_string(),
            r#"
df_1 = commands.search(None, (F.col('x') == F.lit(3)))
df_2 = commands.eval(df_1, y=F.length(F.col('x')))
df_2
            "#
            .trim(),
            false,
        );
    }

    #[rstest]
    fn test_raw_with_prefix(#[from(crate::base::test::ctx_bare)] ctx: PysparkTranspileContext) {
        let df = DataFrame::source_index("main").named(Some("df_pre".to_string()), &ctx);
        let df = df.raw_transform("df_pre.something_new()", None);

        assert_python_code_eq(
            df.to_spark_query(&ctx).unwrap().to_string(),
            r#"
df_pre = table_source(spark, index="main")
df_pre.something_new()
            "#,
            false,
        );
    }

    #[rstest]
    fn test_col_with_dots(#[from(crate::base::test::ctx_bare)] ctx: PysparkTranspileContext) {
        let col_with_dots = column_like!(col("a.b"));
        let col_without_dots = column_like!(col("a"));

        assert_python_code_eq(
            col_with_dots.to_spark_query(&ctx).unwrap().to_string(),
            r#"F.col("`a.b`")"#,
            false,
        );

        assert_python_code_eq(
            col_without_dots.to_spark_query(&ctx).unwrap().to_string(),
            r#"F.col("a")"#,
            false,
        );
    }

    #[rstest]
    fn test_group_by_col_with_dots(
        #[from(crate::base::test::ctx_bare)] ctx: PysparkTranspileContext,
    ) {
        let df = DataFrame::source_index("main");
        let grouped_with_dots = df.clone().group_by(vec!["a.b".to_string()]);
        let grouped_without_dots = df.clone().group_by(vec!["a".to_string()]);

        assert_python_code_eq(
            grouped_with_dots.to_spark_query(&ctx).unwrap().to_string(),
            r#"table_source(spark, index="main").groupBy(["`a.b`"])"#,
            false,
        );

        assert_python_code_eq(
            grouped_without_dots
                .to_spark_query(&ctx)
                .unwrap()
                .to_string(),
            r#"table_source(spark, index="main").groupBy(["a"])"#,
            false,
        );
    }

    #[rstest]
    fn test_rename_with_wildcard(
        #[from(crate::base::test::ctx_bare)] ctx: PysparkTranspileContext,
    ) {
        let df = DataFrame::source_index("main");
        let renamed_with_wildcard = df.clone().with_columns_renamed(vec![("a.*", "new_a")]);
        let renamed_without_wildcard = df.clone().with_columns_renamed(vec![("a", "new_a")]);

        assert_python_code_eq(
            renamed_with_wildcard
                .to_spark_query(&ctx)
                .unwrap()
                .to_string(),
            r#"
from pyspark_spl_tools.monkeypatches import install_monkeypatches

install_monkeypatches()
table_source(spark, index="main")._spltranspiler__withColumnsRenamedWithWildcards({"a.*": "new_a"})
            "#,
            false,
        );

        assert_python_code_eq(
            renamed_without_wildcard
                .to_spark_query(&ctx)
                .unwrap()
                .to_string(),
            r#"table_source(spark, index="main").withColumnsRenamed({"a": "new_a"})"#,
            false,
        );
    }

    #[rstest]
    fn test_lit_str() {
        assert_eq!(
            column_like!(lit("abc")),
            ColumnLike::Literal {
                code: "\"abc\"".into()
            }
        );
        let abc_var = "abc";
        assert_eq!(
            column_like!(lit(abc_var)),
            ColumnLike::Literal {
                code: "\"abc\"".into()
            }
        );
        let abc_var = "abc".to_string();
        assert_eq!(
            column_like!(lit(abc_var)),
            ColumnLike::Literal {
                code: "\"abc\"".into()
            }
        );
    }

    #[rstest]
    fn test_pylit_str() {
        assert_eq!(column_like!(py_lit("abc")), PyLiteral("\"abc\"".into()),);
        assert_eq!(
            column_like!(py_lit("a\\bc")),
            PyLiteral("r\"a\\bc\"".into()),
        );
    }

    #[rstest]
    fn test_boolean(#[from(crate::base::test::ctx_bare)] ctx: PysparkTranspileContext) {
        assert_eq!(
            column_like!([col("x")] == [lit(true)])
                .to_spark_query(&ctx)
                .unwrap()
                .to_string(),
            "F.col('x') == F.lit(True)"
        );
        assert_eq!(
            column_like!([col("x")] == [lit(1 == 1)])
                .to_spark_query(&ctx)
                .unwrap()
                .to_string(),
            "F.col('x') == F.lit(True)"
        );
        assert_eq!(
            column_like!([col("x")] == [lit(1 == 1)])
                .into_search_expr()
                .to_spark_query(&ctx)
                .unwrap()
                .to_string(),
            "F.col('x') == F.lit(True)"
        );
        let spl_expr = spl_transpiler_spl::ast::Expr::from(spl_transpiler_spl::ast::Binary {
            left: Box::new(spl_transpiler_spl::ast::Field::from("x").into()),
            symbol: "=".to_string(),
            right: Box::new(spl_transpiler_spl::ast::BoolValue(true).into()),
        });
        let pyspark_expr: Expr = spl_expr
            .with_context(&ctx)
            .try_into()
            .expect("Failed to convert");
        assert_eq!(
            pyspark_expr
                .into_search_expr()
                .to_spark_query(&ctx)
                .unwrap()
                .to_string(),
            "(F.col('x') == F.lit(True))"
        )
    }
}
