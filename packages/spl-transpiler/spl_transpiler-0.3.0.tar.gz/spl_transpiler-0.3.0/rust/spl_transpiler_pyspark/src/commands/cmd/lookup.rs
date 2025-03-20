use crate::ast::DataFrame;
use crate::ast::*;
use crate::transpiler::utils::join_as_binaries;
use crate::transpiler::{PipelineTransformState, PipelineTransformer};
use anyhow::{bail, Result};
use spl_transpiler_spl::ast;
use spl_transpiler_spl::ast::FieldLike;
use spl_transpiler_spl::commands::cmd::lookup::{LookupCommand, LookupOutput};

impl PipelineTransformer for LookupCommand {
    #[allow(unused_variables, unreachable_code)]
    fn transform_standalone(
        &self,
        state: PipelineTransformState,
    ) -> Result<PipelineTransformState> {
        let df = state.df.clone().unwrap_or_default();

        let df = df.alias("main");
        let lookup_df = DataFrame::source_lookup(self.dataset.clone()).alias("lookup");

        let join_columns: Result<Vec<_>> = self
            .fields
            .iter()
            .map(|f| match f.clone() {
                FieldLike::AliasedField(ast::AliasedField { field, alias }) => Ok(column_like!(
                    [col(format!("`main`.`{}`", alias))]
                        == [col(format!("`lookup`.`{}`", field.0))]
                )),
                FieldLike::Field(ast::Field(name)) => Ok(column_like!(
                    [col(format!("`main`.`{}`", name))] == [col(format!("`lookup`.`{}`", name))]
                )),
                _ => bail!(
                    "UNIMPLEMENTED: Unsupported lookup field definition: {:?}",
                    f
                ),
            })
            .collect();
        let join_condition = join_as_binaries("&", join_columns?).unwrap_or(column_like!(lit(1)));

        let df = df.join(lookup_df, join_condition, "left");

        let df = df.select_with_wildcard(match self.output.clone() {
            None => {
                vec![
                    "`main`.*".to_string().into(),
                    column_like!(col("`lookup`.*")).into(),
                ]
            }
            Some(LookupOutput { kv, fields }) if kv.eq_ignore_ascii_case("OUTPUT") => {
                let mut cols: Vec<ColumnOrName> = vec!["`main`.*".to_string().into()];
                for field in fields {
                    cols.push(match field {
                        FieldLike::Field(ast::Field(name)) => {
                            column_like!([col(format!("`lookup`.`{}`", name))].alias(name)).into()
                        }
                        FieldLike::AliasedField(ast::AliasedField { field, alias }) => {
                            column_like!([col(format!("`lookup`.`{}`", field.0))].alias(alias))
                                .into()
                        }
                        // FieldLike::Alias(_) => {}
                        _ => bail!(
                            "UNIMPLEMENTED: Unsupported lookup output definition: {:?}",
                            field
                        ),
                    });
                }
                cols
            }
            Some(LookupOutput { kv, fields }) if kv.eq_ignore_ascii_case("OUTPUTNEW") => {
                bail!("UNIMPLEMENTED: `lookup` command with `OUTPUTNEW` not supported")
            }
            output => bail!("Unsupported output definition for `lookup`: {:?}", output),
        });

        Ok(state.with_df(df))
    }
}

#[cfg(test)]
mod tests {
    use crate::utils::test::generates;
    use rstest::rstest;

    #[rstest]
    fn test_lookup_1() {
        generates(
            r#"index=main
                        | lookup usertogroup user as local_user OUTPUT group as user_group"#,
            r#"
from pyspark_spl_tools.monkeypatches import install_monkeypatches
install_monkeypatches()

table_source(spark, index="main").alias("main").join(
    table_source(spark, lookup="usertogroup").alias("lookup"),
    on=(F.col("`main`.`local_user`") == F.col("`lookup`.`user`")),
    how="left"
)._spltranspiler__selectWithWildcards(
    "`main`.*",
    F.col("`lookup`.`group`").alias("user_group")
)
            "#,
        )
    }
}
