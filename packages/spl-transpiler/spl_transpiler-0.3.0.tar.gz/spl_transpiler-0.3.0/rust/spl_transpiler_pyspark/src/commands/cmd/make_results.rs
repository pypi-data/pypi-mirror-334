use crate::ast::*;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};

impl PipelineTransformer for spl_transpiler_spl::commands::cmd::make_results::MakeResultsCommand {
    #[allow(unused_variables, unreachable_code)]
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        // let df = state.df.clone().unwrap_or_default();

        /*
            spark.range(0, 10, 1)
        //         |.withColumn('_raw', F.lit(None))
        //         |.withColumn('_time', F.current_timestamp())
        //         |.withColumn('host', F.lit(None))
        //         |.withColumn('source', F.lit(None))
        //         |.withColumn('sourcetype', F.lit(None))
        //         |.withColumn('splunk_server', F.lit('local'))
        //         |.withColumn('splunk_server_group', F.lit(None))
             */
        let df = DataFrame::raw_source(format!("spark.range(0, {}, 1)", self.count));
        let mut columns = vec![("_time", column_like!(current_timestamp()))];
        if self.annotate {
            columns.push(("_raw", column_like!(lit(None))));
            columns.push(("host", column_like!(lit(None))));
            columns.push(("source", column_like!(lit(None))));
            columns.push(("sourcetype", column_like!(lit(None))));
            columns.push(("splunk_server", column_like!(lit(self.server.clone()))));
            columns.push((
                "splunk_server_group",
                match self.server_group.clone() {
                    Some(group) => column_like!(lit(group)),
                    None => column_like!(lit(None)),
                },
            ));
        }
        let df = df.with_columns(columns);

        Ok(state.with_df(df))
    }
}
