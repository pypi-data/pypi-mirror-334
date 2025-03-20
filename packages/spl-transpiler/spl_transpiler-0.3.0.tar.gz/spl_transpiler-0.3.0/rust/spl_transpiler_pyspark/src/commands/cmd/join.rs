use crate::ast::*;
use crate::transpiler::utils::join_as_binaries;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use anyhow::{bail, ensure, Context};
use spl_transpiler_spl::ast;
use spl_transpiler_spl::commands::cmd::join::JoinCommand;

impl PipelineTransformer for JoinCommand {
    #[allow(unused_variables, unreachable_code)]
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let df = state.df.clone().unwrap_or_default().alias("LEFT");

        ensure!(
            self.max == 1,
            "UNIMPLEMENTED: Join with max != 1 not yet supported"
        );

        let right_df: TransformedPipeline =
            TransformedPipeline::transform(self.sub_search.clone(), state.ctx.clone())?;
        let right_df = right_df
            .dataframes
            .first()
            .context("No dataframe found for sub_search")?
            .named(None, &state.ctx)
            .alias("RIGHT");

        let join_type = match self.join_type.clone().as_str() {
            "inner" => "inner",
            "left" => "left",
            "outer" => "outer",
            _ => bail!("Unsupported join type: {}", self.join_type),
        };

        let condition = join_as_binaries(
            "&",
            self.fields
                .clone()
                .into_iter()
                .map(|ast::Field(name)| {
                    column_like!(
                        [col(format!("`LEFT`.`{}`", name))] == [col(format!("`RIGHT`.`{}`", name))]
                    )
                })
                .collect(),
        )
        .unwrap();

        let condition = match (self.use_time, self.earlier) {
            (true, true) => {
                column_like!([condition] & [[col("`LEFT`.`_time`")] >= [col("`RIGHT`.`_time`")]])
            }
            (true, false) => {
                column_like!([condition] & [[col("`LEFT`.`_time`")] <= [col("`RIGHT`.`_time`")]])
            }
            (false, _) => condition,
        };

        let df = df.join(right_df, condition, join_type);

        Ok(state.with_df(df))
    }
}

#[cfg(test)]
mod tests {
    use crate::utils::test::*;
    use rstest::rstest;

    #[rstest]
    fn test_join_1() {
        generates(
            r#"join product_id [search vendors]"#,
            r#"
df_1 = table_source(spark, index="main").where(F.col("_raw").ilike("%vendors%"))
table_source(spark, index="main").alias("LEFT").join(
    df_1.alias("RIGHT"),
    on=(F.col("`LEFT`.`product_id`") == F.col("`RIGHT`.`product_id`")),
    how="inner"
)"#,
        )
    }

    #[rstest]
    fn test_join_2() {
        generates(
            r#"
index=main
| join  process_id [
    | tstats summariesonly=false allow_old_summaries=true fillnull_value=null count
      FROM datamodel=Network_Traffic.All_Traffic
      by All_Traffic.process_id All_Traffic.dest All_Traffic.dest_port
]"#,
            r#"
df_1 = (
    table_source(spark, datamodel="`Network_Traffic.All_Traffic`")
        .groupBy(["`All_Traffic.process_id`","`All_Traffic.dest`","`All_Traffic.dest_port`"])
        .agg(F.count(F.lit(1)).alias("count"))
)
table_source(spark, index="main").alias("LEFT").join(
    df_1.alias("RIGHT"),
    on=(F.col("`LEFT`.`process_id`") == F.col("`RIGHT`.`process_id`")),
    how="inner"
)
"#,
        )
    }
}
