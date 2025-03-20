use crate::ast::column_like;
use crate::ast::ColumnLike;
use crate::ast::ColumnOrName;
use crate::ast::PyDict;
use crate::ast::PyList;
use crate::ast::PyLiteral;
use crate::ast::RuntimeExpr;
use crate::singletons::{CodeTransformer, CodeTransformerType};
use crate::utils::escape_maybe_dotted;
use crate::{PysparkTranspileContext, PythonCode, ToSparkQuery};
use anyhow::{bail, Context};
use spl_transpiler_common::aliasable::Aliasable;
use std::sync::atomic::{AtomicUsize, Ordering};

#[derive(Debug, PartialEq, Clone, Hash)]
pub enum SourceKey {
    Index,
    Lookup,
    DataModel,
}

impl SourceKey {
    pub fn to_table_source_kwarg(&self) -> String {
        match self {
            SourceKey::Index => "index".to_string(),
            SourceKey::Lookup => "lookup".to_string(),
            SourceKey::DataModel => "datamodel".to_string(),
        }
    }
}

#[allow(dead_code)]
#[derive(Debug, PartialEq, Clone, Hash)]
pub enum DataFrame {
    Source {
        source_keys: Vec<(SourceKey, String)>,
    },
    Transformed {
        source: Box<DataFrame>,
        transformer: CodeTransformerType,
    },
    Runtime {
        name: String,
        source: Option<Box<DataFrame>>,
        runtime_func: String,
        args: Vec<RuntimeExpr>,
        kwargs: Vec<(String, RuntimeExpr)>,
    },
    Raw {
        source: Option<Box<DataFrame>>,
        code: Option<String>,
        prefix: Option<Vec<String>>,
    },
    Named {
        source: Box<DataFrame>,
        name: String,
    },
    DataframeMethod {
        source: Box<DataFrame>,
        method: String,
        args: Vec<RuntimeExpr>,
        kwargs: Vec<(String, RuntimeExpr)>,
    },
}

#[allow(dead_code)]
impl DataFrame {
    fn generate_unique_name(counter: &AtomicUsize) -> String {
        let uid = counter.fetch_add(1, Ordering::Relaxed);
        format!("df_{uid}")
    }

    pub fn source(source_keys: impl IntoIterator<Item = (SourceKey, impl ToString)>) -> DataFrame {
        let source_keys = source_keys
            .into_iter()
            .map(|(k, v)| (k, v.to_string()))
            .collect();
        DataFrame::Source { source_keys }
    }
    pub fn source_index(index: impl ToString) -> DataFrame {
        DataFrame::source(vec![(SourceKey::Index, index)])
    }
    pub fn source_lookup(lookup: impl ToString) -> DataFrame {
        DataFrame::source(vec![(SourceKey::Lookup, lookup)])
    }
    pub fn source_datamodel(datamodel: impl ToString) -> DataFrame {
        DataFrame::source(vec![(SourceKey::DataModel, datamodel)])
    }
    pub fn runtime(
        source: Option<DataFrame>,
        runtime_func: impl ToString,
        args: Vec<RuntimeExpr>,
        kwargs: Vec<(String, RuntimeExpr)>,
        ctx: &PysparkTranspileContext,
    ) -> Self {
        let source = match source {
            Some(df @ DataFrame::Runtime { .. }) => Some(Box::new(df)),
            Some(df) => Some(Box::new(
                df.named(Some(Self::generate_unique_name(&ctx.df_num)), ctx),
            )),
            None => None,
        };
        Self::Runtime {
            name: Self::generate_unique_name(&ctx.df_num),
            source,
            runtime_func: runtime_func.to_string(),
            args,
            kwargs,
        }
    }
    pub fn raw_source(code: impl ToString) -> DataFrame {
        DataFrame::Raw {
            source: None,
            code: Some(code.to_string()),
            prefix: None,
        }
    }
    pub fn raw_transform(&self, code: impl ToString, prefix: Option<Vec<String>>) -> DataFrame {
        DataFrame::Raw {
            source: Some(Box::new(self.clone())),
            code: Some(code.to_string()),
            prefix,
        }
    }
    pub fn requires(&self, transformer: CodeTransformerType) -> DataFrame {
        DataFrame::Transformed {
            source: Box::new(self.clone()),
            transformer,
        }
    }
    // pub fn comment(&self, comment: impl ToString) -> DataFrame {
    //     DataFrame::Raw {
    //         source: Some(Box::new(self.clone())),
    //         code: None,
    //         prefix: Some(vec!(format!("# {}", comment.to_string()))),
    //     }
    // }
    // pub fn prefixed(&self, prefix: impl IntoIterator<Item=String>) -> DataFrame {
    //     DataFrame::Raw {
    //         source: Some(Box::new(self.clone())),
    //         code: None,
    //         prefix: Some(Vec::from(prefix)),
    //     }
    // }
    pub fn named(&self, name: Option<String>, ctx: &PysparkTranspileContext) -> DataFrame {
        DataFrame::Named {
            source: Box::new(self.clone()),
            name: name.unwrap_or_else(|| Self::generate_unique_name(&ctx.df_num)),
        }
    }
    pub fn select(&self, columns: Vec<ColumnLike>) -> DataFrame {
        self.dataframe_method(
            "select",
            columns.into_iter().map(Into::into).collect(),
            vec![],
        )
    }
    pub fn select_with_wildcard(&self, columns: Vec<ColumnOrName>) -> DataFrame {
        self.dataframe_method(
            "_spltranspiler__selectWithWildcards",
            columns
                .into_iter()
                .map(|c| match c {
                    ColumnOrName::Column(col) => col.into(),
                    ColumnOrName::Name(name) => column_like!(py_lit(name)).into(),
                })
                .collect(),
            vec![],
        )
        .requires(CodeTransformerType::MonkeyPatch)
    }
    pub fn where_(&self, condition: impl Into<RuntimeExpr>) -> DataFrame {
        self.dataframe_method("where", vec![condition.into().unaliased()], vec![])
    }
    pub fn group_by(&self, columns: Vec<impl Into<ColumnOrName>>) -> DataFrame {
        self.dataframe_method(
            "groupBy",
            vec![PyList(
                columns
                    .into_iter()
                    .map(|col| match col.into() {
                        ColumnOrName::Column(col) => col.unaliased().into(),
                        ColumnOrName::Name(name) => {
                            column_like!(py_lit(escape_maybe_dotted(name))).into()
                        }
                    })
                    .collect::<Vec<_>>(),
            )
            .into()],
            vec![],
        )
    }
    pub fn agg(&self, columns: Vec<ColumnLike>) -> DataFrame {
        self.dataframe_method(
            "agg",
            columns.into_iter().map(|c| c.into()).collect(),
            vec![],
        )
    }
    pub fn with_column(&self, name: impl ToString, column: ColumnLike) -> DataFrame {
        self.dataframe_method(
            "withColumn",
            vec![
                column_like!(py_lit(name.to_string())).into(),
                column.unaliased().into(),
            ],
            vec![],
        )
    }
    pub fn with_columns(
        &self,
        columns: impl IntoIterator<Item = (impl ToString, ColumnLike)>,
    ) -> DataFrame {
        self.dataframe_method(
            "withColumns",
            vec![PyDict(
                columns
                    .into_iter()
                    .map(|(k, v)| (k.to_string(), v.into()))
                    .collect::<Vec<_>>(),
            )
            .into()],
            vec![],
        )
    }
    pub fn with_column_maybe(
        &self,
        name: impl ToString,
        column: ColumnLike,
        requires_col: String,
    ) -> DataFrame {
        self.dataframe_method(
            "_spltranspiler__withColumnMaybe",
            vec![
                column_like!(py_lit(name.to_string())).into(),
                column.unaliased().into(),
                PyLiteral::from(requires_col).into(),
            ],
            vec![],
        )
        .requires(CodeTransformerType::MonkeyPatch)
    }
    pub fn with_column_renamed(
        &self,
        old_name: impl ToString,
        new_name: impl ToString,
    ) -> DataFrame {
        self.dataframe_method(
            "withColumnRenamed",
            vec![
                column_like!(py_lit(old_name.to_string())).into(),
                column_like!(py_lit(new_name.to_string())).into(),
            ],
            vec![],
        )
    }
    pub fn with_columns_renamed<OLD: ToString, NEW: ToString>(
        &self,
        renames: impl IntoIterator<Item = (OLD, NEW)>,
    ) -> DataFrame {
        let renames: Vec<_> = renames
            .into_iter()
            .map(|(old, new)| (old.to_string(), new.to_string()))
            .collect();
        let use_custom_rename = renames
            .iter()
            .any(|(old, new)| old.contains("*") || new.contains("*"));
        let df = self.dataframe_method(
            if use_custom_rename {
                "_spltranspiler__withColumnsRenamedWithWildcards"
            } else {
                "withColumnsRenamed"
            },
            vec![PyDict(
                renames
                    .into_iter()
                    .map(|(old, new)| (old, column_like!(py_lit(new)).into()))
                    .collect(),
            )
            .into()],
            vec![],
        );

        if use_custom_rename {
            df.requires(CodeTransformerType::MonkeyPatch)
        } else {
            df
        }
    }
    pub fn order_by(&self, columns: Vec<ColumnLike>) -> DataFrame {
        self.dataframe_method(
            "orderBy",
            columns.into_iter().map(|c| c.unaliased().into()).collect(),
            vec![],
        )
    }
    pub fn union_by_name(&self, other: DataFrame) -> DataFrame {
        self.dataframe_method(
            "unionByName",
            vec![RuntimeExpr::DataFrame(Box::new(other))],
            vec![(
                "allowMissingColumns".into(),
                column_like!(py_lit(true)).into(),
            )],
        )
    }
    pub fn limit(&self, limit: impl Into<u64>) -> DataFrame {
        self.dataframe_method(
            "limit",
            vec![column_like!(py_lit(limit.into())).into()],
            vec![],
        )
    }
    pub fn tail(&self, limit: impl Into<u64>) -> DataFrame {
        self.dataframe_method(
            "tail",
            vec![column_like!(py_lit(limit.into())).into()],
            vec![],
        )
    }
    pub fn join(
        &self,
        other: DataFrame,
        condition: impl Into<RuntimeExpr>,
        join_type: impl ToString,
    ) -> DataFrame {
        self.dataframe_method(
            "join",
            vec![RuntimeExpr::DataFrame(Box::new(other))],
            vec![
                ("on".into(), condition.into()),
                (
                    "how".into(),
                    column_like!(py_lit(join_type.to_string())).into(),
                ),
            ],
        )
    }
    pub fn alias(&self, name: impl ToString) -> DataFrame {
        self.dataframe_method(
            "alias",
            vec![RuntimeExpr::from(column_like!(py_lit(name.to_string()))).unaliased()],
            vec![],
        )
    }
    pub fn dataframe_method(
        &self,
        method: impl ToString,
        args: Vec<RuntimeExpr>,
        kwargs: Vec<(String, RuntimeExpr)>,
    ) -> DataFrame {
        Self::DataframeMethod {
            source: Box::new(self.clone()),
            method: method.to_string(),
            args,
            kwargs,
        }
    }
}

impl Default for DataFrame {
    fn default() -> Self {
        DataFrame::source_index("main")
    }
}

impl ToSparkQuery for DataFrame {
    fn to_spark_query(&self, ctx: &PysparkTranspileContext) -> anyhow::Result<PythonCode> {
        match self {
            DataFrame::Source { source_keys } => {
                let args = source_keys
                    .iter()
                    .map(|(k, v)| format!("{}='{}'", k.to_table_source_kwarg(), v))
                    .collect::<Vec<_>>()
                    .join(", ");
                Ok(format!("table_source(spark, {})", args).into())
            }
            DataFrame::Transformed {
                source,
                transformer,
            } => {
                let code = source.to_spark_query(ctx)?;
                let code = transformer.update_code(code, ctx)?;
                Ok(code)
            }
            DataFrame::Raw {
                source,
                code,
                prefix,
            } => {
                let source_code = match source {
                    Some(ref source) => Some(source.to_spark_query(ctx)?),
                    None => None,
                };
                let primary_code = match code {
                    Some(ref code) => code.clone(),
                    None => match &source_code {
                        Some(PythonCode {
                            primary_df_code, ..
                        }) => primary_df_code.clone(),
                        None => {
                            bail!("Cannot generate raw code with neither a source nor raw code")
                        }
                    },
                };
                Ok(PythonCode::new(
                    primary_code,
                    prefix.clone().unwrap_or_default(),
                    source_code,
                ))
            }
            DataFrame::Runtime {
                name,
                source,
                runtime_func,
                args,
                kwargs,
            } => {
                let primary_source_code = match source {
                    Some(ref source) => source.to_spark_query(ctx)?,
                    None => PythonCode::from("None".to_string()),
                };
                let mut all_preface = vec![];
                let mut all_args = vec![primary_source_code.primary_df_code.clone()];
                for arg in args.iter() {
                    let PythonCode {
                        preface,
                        primary_df_code,
                    } = arg.to_spark_query(ctx)?;
                    all_preface.extend(preface);
                    all_args.push(primary_df_code);
                }
                for (name, kwarg) in kwargs.iter() {
                    let PythonCode {
                        preface,
                        primary_df_code,
                    } = kwarg.to_spark_query(ctx)?;
                    all_preface.extend(preface);
                    all_args.push(format!("{name}={primary_df_code}"));
                }
                let all_args_str = all_args.join(", ");
                let full_command =
                    format!("{} = commands.{}({})", name, runtime_func, all_args_str);
                all_preface.push(full_command);

                Ok(PythonCode::new(
                    name.clone(),
                    all_preface,
                    Some(primary_source_code),
                ))
            }
            DataFrame::Named { source, name } => {
                let source_code = source.to_spark_query(ctx)?;
                Ok(PythonCode::new(
                    name.clone(),
                    vec![format!("{} = {}", name, source_code.primary_df_code)],
                    Some(source_code),
                ))
            }
            DataFrame::DataframeMethod {
                source,
                method,
                args,
                kwargs,
            } => {
                let args = args
                    .iter()
                    .map(|col| Ok((None, col.to_spark_query(ctx)?)))
                    .collect::<anyhow::Result<Vec<_>>>()
                    .context("Rendering function args failed")?;
                let kwargs = kwargs
                    .iter()
                    .map(|(name, col)| Ok((Some(name.clone()), col.to_spark_query(ctx)?)))
                    .collect::<anyhow::Result<Vec<_>>>()
                    .context("Rendering function kwargs failed")?;
                let mut param_strings = Vec::new();
                let mut source_code = source.to_spark_query(ctx)?;
                args.into_iter().chain(kwargs).for_each(
                    |(
                        name,
                        PythonCode {
                            primary_df_code,
                            preface,
                        },
                    )| {
                        source_code = PythonCode::new(
                            source_code.primary_df_code.clone(),
                            preface,
                            Some(source_code.clone()),
                        );
                        let param_str = match name {
                            Some(ref name) => format!("{}={}", name, primary_df_code),
                            None => primary_df_code,
                        };
                        param_strings.push(param_str);
                    },
                );
                let code = format!(
                    "{}.{}({},)",
                    source_code.primary_df_code,
                    method,
                    param_strings.join(",")
                );
                Ok(PythonCode::new(code, vec![], Some(source_code)))
            }
        }
    }
}
