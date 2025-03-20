use crate::ast::ColumnLike::FunctionCall;
use crate::ast::*;
use crate::base::{PysparkTranspileContext, ToSparkExpr};
use crate::commands::stats_utils;
use crate::singletons::CodeTransformerType;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use anyhow::bail;
use anyhow::Result;
use log::warn;
use spl_transpiler_common::aliasable::Aliasable;
use spl_transpiler_spl::ast;
use spl_transpiler_spl::commands::cmd::stats::*;

fn transform_stats_runtime_expr(
    expr: &ast::Expr,
    ctx: &PysparkTranspileContext,
) -> Result<(String, RuntimeExpr)> {
    let (e, maybe_name) = expr.clone().unaliased_with_name();
    let (name, args) = match e {
        ast::Expr::Call(ast::Call { name, args }) => (name.to_string(), args),
        _ => bail!(
            "All `stats` aggregations must be function calls, got {:?}",
            expr
        ),
    };
    let alias = maybe_name.unwrap_or(name.clone());
    let args: Result<Vec<Expr>> = args
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

impl PipelineTransformer for StatsCommand {
    fn transform_for_runtime(
        &self,
        state: PipelineTransformState,
    ) -> Result<PipelineTransformState> {
        if self.partitions != 0 && self.partitions != 1 {
            warn!("`stats` `partitions` argument has no effect in PySpark")
        }
        if self.all_num {
            warn!("`stats` `all_num` argument has no effect in PySpark")
        }
        if self.dedup_split_vals {
            warn!("`stats` `dedup_split_vals` argument has no effect in PySpark")
        }
        if self.delim != " " {
            warn!("`stats` `delim` argument has no effect in PySpark")
        }

        let mut all_kwargs = py_dict! {};

        // By statement
        if let Some(by_fields) = &self.by {
            let by_fields: Vec<RuntimeExpr> = by_fields
                .iter()
                .cloned()
                .map(stats_utils::transform_by_field)
                .map(Into::into)
                .collect();
            all_kwargs.push("by", PyList(by_fields));
        }

        for e in self.funcs.iter() {
            let (name, e) = transform_stats_runtime_expr(e, &state.ctx)?;
            all_kwargs.push(name, e);
        }

        let df = DataFrame::runtime(state.df.clone(), "stats", vec![], all_kwargs.0, &state.ctx);

        Ok(state.with_df(df))
    }

    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> Result<PipelineTransformState> {
        if self.partitions != 0 && self.partitions != 1 {
            warn!("`stats` `partitions` argument has no effect in PySpark")
        }
        if self.all_num {
            warn!("`stats` `all_num` argument has no effect in PySpark")
        }
        if self.dedup_split_vals {
            warn!("`stats` `dedup_split_vals` argument has no effect in PySpark")
        }
        if self.delim != " " {
            warn!("`stats` `delim` argument has no effect in PySpark")
        }

        let mut df = state.df.clone().unwrap_or_default();

        let mut aggs: Vec<ColumnLike> = vec![];
        for e in self.funcs.iter() {
            let (df_, e) = stats_utils::transform_stats_expr(df, e, &state.ctx)?;
            df = df_;
            aggs.push(e);
        }
        let by_columns: Vec<_> = self
            .by
            .clone()
            .unwrap_or_default()
            .into_iter()
            .map(stats_utils::transform_by_field)
            .map(|col| match col {
                ColumnOrName::Column(col) => RuntimeExpr::from(col.unaliased()),
                ColumnOrName::Name(name) => {
                    let formatted_name = if name.contains('.') {
                        format!("`{}`", name)
                    } else {
                        name.to_string()
                    };
                    RuntimeExpr::from(column_like!(py_lit(formatted_name)))
                }
            })
            .collect();

        let df = df
            .dataframe_method(
                "_spltranspiler__groupByMaybeExploded",
                vec![PyList(by_columns).into()],
                Vec::new(),
            )
            .requires(CodeTransformerType::MonkeyPatch);

        let df = df.agg(aggs);

        Ok(state.with_df(df))
    }
}

#[cfg(test)]
mod tests {
    use crate::utils::test::{generates, generates_runtime};
    use rstest::rstest;

    #[rstest]
    fn test_xsl_script_execution_with_wmic_1() {
        generates(
            r#"stats
            count min(_time) as firstTime max(_time) as lastTime
            by Processes.parent_process_name Processes.parent_process Processes.process_name Processes.process_id Processes.process Processes.dest Processes.user"#,
            r#"
from pyspark_spl_tools.monkeypatches import install_monkeypatches
install_monkeypatches()

table_source(spark, index="main")._spltranspiler__groupByMaybeExploded([
                "`Processes.parent_process_name`",
                "`Processes.parent_process`",
                "`Processes.process_name`",
                "`Processes.process_id`",
                "`Processes.process`",
                "`Processes.dest`",
                "`Processes.user`",
            ]).agg(
                F.count(F.lit(1)).alias("count"),
                F.min(F.col("_time")).alias("firstTime"),
                F.max(F.col("_time")).alias("lastTime"),
            )"#,
        )
    }

    #[rstest]
    fn test_stats_2() {
        generates(
            r#"stats
            count min(_time) as firstTime max(_time) as lastTime
            by Web.http_user_agent, Web.status Web.http_method, Web.url, Web.url_length, Web.src, Web.dest, sourcetype"#,
            r#"
from pyspark_spl_tools.monkeypatches import install_monkeypatches
install_monkeypatches()

table_source(spark, index="main")._spltranspiler__groupByMaybeExploded([
                "`Web.http_user_agent`",
                "`Web.status`",
                "`Web.http_method`",
                "`Web.url`",
                "`Web.url_length`",
                "`Web.src`",
                "`Web.dest`",
                "sourcetype",
            ]).agg(
                F.count(F.lit(1)).alias("count"),
                F.min(F.col("_time")).alias("firstTime"),
                F.max(F.col("_time")).alias("lastTime"),
            )
            "#,
        )
    }

    #[rstest]
    fn test_stats_3() {
        let query = r#"stats
        count min(_time) AS firstTime max(_time) AS lastTime
        BY _time span=1h Processes.user Processes.process_id Processes.process_name Processes.process Processes.process_path Processes.dest Processes.parent_process_name Processes.parent_process Processes.process_guid"#;

        generates(
            query,
            r#"
from pyspark_spl_tools.monkeypatches import install_monkeypatches
install_monkeypatches()

table_source(spark, index="main")._spltranspiler__groupByMaybeExploded([
                F.window("_time", "1 hours"),
                "`Processes.user`",
                "`Processes.process_id`",
                "`Processes.process_name`",
                "`Processes.process`",
                "`Processes.process_path`",
                "`Processes.dest`",
                "`Processes.parent_process_name`",
                "`Processes.parent_process`",
                "`Processes.process_guid`",
            ]).agg(
                F.count(F.lit(1)).alias("count"),
                F.min(F.col("_time")).alias("firstTime"),
                F.max(F.col("_time")).alias("lastTime"),
            )
            "#,
        )
    }

    #[rstest]
    fn test_stats_4() {
        let query = r#"stats
        count min(_time) as firstTime max(_time) as lastTime
        by Processes.original_file_name Processes.parent_process_name Processes.parent_process Processes.process_name Processes.process Processes.parent_process_id Processes.process_id  Processes.dest Processes.user"#;

        // TODO: The `like` strings should be r strings or escaped
        generates(
            query,
            r#"
from pyspark_spl_tools.monkeypatches import install_monkeypatches
install_monkeypatches()

table_source(spark, index="main")._spltranspiler__groupByMaybeExploded([
                "`Processes.original_file_name`",
                "`Processes.parent_process_name`",
                "`Processes.parent_process`",
                "`Processes.process_name`",
                "`Processes.process`",
                "`Processes.parent_process_id`",
                "`Processes.process_id`",
                "`Processes.dest`",
                "`Processes.user`",
            ]).agg(
                F.count(F.lit(1)).alias("count"),
                F.min(F.col("_time")).alias("firstTime"),
                F.max(F.col("_time")).alias("lastTime"),
            )
            "#,
        )
    }

    #[rstest]
    fn test_stats_5() {
        let query = r#"stats
        count min(_time) as firstTime max(_time) as lastTime
        by _time span=1h Processes.original_file_name Processes.parent_process_name Processes.parent_process Processes.process_name Processes.process Processes.parent_process_id Processes.process_id  Processes.dest Processes.user"#;

        generates_runtime(
            query,
            r#"
df_1 = commands.stats(
    None,
    by=[
        F.window("_time", "1 hours"),
        F.col("`Processes.original_file_name`"),
        F.col("`Processes.parent_process_name`"),
        F.col("`Processes.parent_process`"),
        F.col("`Processes.process_name`"),
        F.col("`Processes.process`"),
        F.col("`Processes.parent_process_id`"),
        F.col("`Processes.process_id`"),
        F.col("`Processes.dest`"),
        F.col("`Processes.user`"),
    ],
    count=functions.stats.count(),
    firstTime=functions.stats.min(F.col("_time")),
    lastTime=functions.stats.max(F.col("_time")),
)
df_1
            "#,
        )
    }

    #[rstest]
    fn test_stats_6() {
        let query = r#"stats
        count
        by _time"#;

        generates(
            query,
            r#"
from pyspark_spl_tools.monkeypatches import install_monkeypatches
install_monkeypatches()

table_source(spark, index="main")._spltranspiler__groupByMaybeExploded(["_time"]).agg(F.count(F.lit(1)).alias("count"))
            "#,
        )
    }

    #[rstest]
    fn test_stats_7() {
        let query = r#"
    sourcetype=aws:cloudtrail eventName=ModifyImageAttribute (requestParameters.launchPermission.add.items{}.userId
    = * OR requestParameters.launchPermission.add.items{}.group = all)

    | rename requestParameters.launchPermission.add.items{}.group as group_added

    | rename requestParameters.launchPermission.add.items{}.userId as accounts_added

    | eval ami_status=if(match(group_added,"all") ,"Public AMI", "Not Public")

    | stats count min(_time) as firstTime max(_time) as lastTime  values(group_added)
    values(accounts_added) as accounts_added values(ami_status) by  src_ip region
    eventName userAgent user_arn aws_account_id userIdentity.principalId

    |  convert timeformat="%Y-%m-%dT%H:%M:%S" ctime(firstTime)| convert timeformat="%Y-%m-%dT%H:%M:%S"
    ctime(lastTime)
    "#;

        generates(
            query,
            r#"
from pyspark_spl_tools.monkeypatches import install_monkeypatches

install_monkeypatches()
table_source(spark, index="main").where(
    (
        (
            (F.col("sourcetype") == F.lit("aws:cloudtrail"))
            & (F.col("eventName") == F.lit("ModifyImageAttribute"))
        )
        & (
            F.col("`requestParameters.launchPermission.add.items{}.userId`").ilike("%") |
            (
                F.col("`requestParameters.launchPermission.add.items{}.group`")
                == F.lit("all")
            )
        )
    )
).withColumnsRenamed(
    {"requestParameters.launchPermission.add.items{}.group": "group_added"}
).withColumnsRenamed(
    {"requestParameters.launchPermission.add.items{}.userId"    : "accounts_added"}
).withColumn(
    "ami_status",
    F.when(
        F.regexp_like(F.col("group_added"), F.lit("all")), F.lit("Public AMI"    )
    ).otherwise(F.lit("Not Public"))
)._spltranspiler__groupByMaybeExploded(
    [
        "src_ip",
        "region",
        "eventName",
        "userAgent",
        "user_arn",
        "aws_account_id",
        "`userIdentity.principalId`"
    ]
).agg(
    F.count(F.lit(1)).alias("count"),
    F.min(F.col("_time")).alias("firstTime"),
    F.max(F.col("_time")).alias("lastTime"),
    F.collect_set(F.col("group_added")).alias("values"),
    F.collect_set(F.col("accounts_added")).alias("accounts_added"),
    F.collect_set(F.col("ami_status")).alias("values")
)._spltranspiler__withColumnMaybe(
    "firstTime",
    F.date_format(F.col("firstTime"), "yyyy-MM-dd'T'HH:mm:ss"),
    "firstTime"
)._spltranspiler__withColumnMaybe(
    "lastTime",
    F.date_format(F.col("lastTime"), "yyyy-MM-dd'T'HH:mm:ss"),
    "lastTime"
)
"#,
        )
    }
}
