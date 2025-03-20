//noinspection RsDetachedFile
use crate::ast::*;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use anyhow::{bail, ensure};
use log::warn;
use spl_transpiler_spl::commands::cmd::data_model::*;

impl PipelineTransformer for DataModelCommand {
    fn transform_for_runtime(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        let df = state.df.clone();
        let mut kwargs = py_dict! {};

        kwargs.push(
            "data_model_name",
            PyLiteral::from(self.data_model_name.clone()),
        );
        kwargs.push("dataset_name", PyLiteral::from(self.dataset_name.clone()));
        kwargs.push("search_mode", PyLiteral::from(self.search_mode.clone()));
        kwargs.push("strict_fields", PyLiteral::from(self.strict_fields));
        kwargs.push(
            "allow_old_summaries",
            PyLiteral::from(self.allow_old_summaries),
        );
        kwargs.push("summaries_only", PyLiteral::from(self.summaries_only));

        let df = DataFrame::runtime(df, "data_model", vec![], kwargs.0, &state.ctx);

        Ok(state.with_df(df))
    }

    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> anyhow::Result<PipelineTransformState> {
        if !self.summaries_only {
            warn!("`datamodel` `summariesonly` argument has no effect in PySpark")
        }
        if !self.allow_old_summaries {
            warn!("`datamodel` `allow_old_summaries` argument has no effect in PySpark")
        }
        if !self.strict_fields {
            warn!("`datamodel` `strict_fields` argument has no effect in PySpark")
        }
        ensure!(
            self.search_mode == Some("search".to_string()),
            "UNIMPLEMENTED: `datamodel` command does not support search_mode other than 'search'"
        );

        let df = match (state.df.clone(), self.data_model_name.clone(), self.dataset_name.clone()) {
            (Some(src), None, None) => src,
            (None, data_model, node_name) => DataFrame::source_datamodel(match (data_model, node_name) {
                (Some(data_model), None) => format!("`{}`", data_model),
                (Some(data_model), Some(node_name)) => {
                    // data_model = <data_model_name>.<root_dataset_name>
                    // node_name = <root_dataset_name>.<...>.<target_dataset_name>
                    // return <data_model_name>.<root_dataset_name>.<...>.<target_dataset_name>
                    // let truncated_node_name = node_name.split(".").skip(1).collect::<Vec<_>>().join(".");
                    let data_model_parts = data_model.split('.').collect::<Vec<_>>();
                    let mut node_name_parts = node_name.split('.').collect::<Vec<_>>();
                    if data_model_parts.last().expect("No data model parts found") == node_name_parts.first().expect("No node name parts found") {
                        node_name_parts.remove(0);
                    }
                    format!("`{}.{}`", data_model_parts.join("."), node_name_parts.join("."))
                }
                _ => bail!("I think we received a dataset ({:?}) with no data model ({:?}) in `datamodel`?", self.dataset_name, self.data_model_name),
            }),
            _ => bail!("UNIMPLEMENTED: `tstats` command requires a source DataFrame and either a data model or a node name"),
        };

        Ok(state.with_df(df))
    }
}

#[cfg(test)]
mod tests {
    use crate::utils::test::{generates, generates_runtime};
    use rstest::rstest;

    #[rstest]
    fn test_datamodel_1() {
        generates_runtime(
            r#"datamodel Model search"#,
            r#"
df_1 = commands.data_model(None, data_model_name="Model", dataset_name=None, search_mode="search", strict_fields=False, allow_old_summaries=False, summaries_only=True)
df_1
            "#,
        )
    }

    #[rstest]
    fn test_datamodel_2() {
        generates(
            r#"datamodel Endpoint Processes search"#,
            r#"table_source(spark, datamodel="`Endpoint.Processes`")"#,
        )
    }
}
