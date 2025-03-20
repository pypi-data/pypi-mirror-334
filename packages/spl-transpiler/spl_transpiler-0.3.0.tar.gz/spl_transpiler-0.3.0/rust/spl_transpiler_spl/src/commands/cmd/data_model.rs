//noinspection RsDetachedFile
use crate::ast;
use crate::ast::ParsedCommandOptions;
use crate::commands::base::{SplCommand, SplCommandOptions};
use crate::parser::{field, ws};
use crate::python::*;
use nom::branch::alt;
use nom::bytes::complete::tag_no_case;
use nom::combinator::{map, opt, verify};
use nom::{IResult, Parser};
use pyo3::prelude::*;
/*
| datamodel [<data model name>] [<dataset name>] [<data model search mode>] [strict_fields=<bool>] [allow_old_summaries=<bool>] [summariesonly=<bool>]
 */

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct DataModelCommand {
    #[pyo3(get)]
    pub data_model_name: Option<String>,
    #[pyo3(get)]
    pub dataset_name: Option<String>,
    #[pyo3(get)]
    pub search_mode: Option<String>,
    #[pyo3(get)]
    pub strict_fields: bool,
    #[pyo3(get)]
    pub allow_old_summaries: bool,
    #[pyo3(get)]
    pub summaries_only: bool,
}
impl_pyclass!(DataModelCommand {
    strict_fields: bool,
    allow_old_summaries: bool,
    summaries_only: bool,
    data_model_name: Option<String>,
    dataset_name: Option<String>,
    search_mode: Option<String>
});

#[derive(Debug, Default)]
pub struct DataModelParser {}
pub struct DataModelCommandOptions {
    strict_fields: bool,
    allow_old_summaries: bool,
    summaries_only: bool,
}

impl SplCommandOptions for DataModelCommandOptions {}

impl TryFrom<ParsedCommandOptions> for DataModelCommandOptions {
    type Error = anyhow::Error;

    fn try_from(value: ParsedCommandOptions) -> Result<Self, Self::Error> {
        Ok(Self {
            strict_fields: value.get_boolean("strict_fields", false)?,
            allow_old_summaries: value.get_boolean("allow_old_summaries", false)?,
            summaries_only: value.get_boolean("summariesonly", true)?,
        })
    }
}

fn field_not_keyword(input: &str) -> IResult<&str, ast::Field> {
    verify(field, |v| {
        !matches!(v.0.as_str(), "search" | "flat" | "acceleration_search")
    })
    .parse(input)
}

impl SplCommand<DataModelCommand> for DataModelParser {
    type RootCommand = crate::commands::DataModelCommandRoot;
    type Options = DataModelCommandOptions;

    fn parse_body(input: &str) -> IResult<&str, DataModelCommand> {
        map(
            (
                Self::Options::match_options,
                opt(ws(field_not_keyword)),
                opt(ws(field_not_keyword)),
                opt(alt((
                    tag_no_case("search"),
                    tag_no_case("flat"),
                    tag_no_case("acceleration_search"),
                ))),
            ),
            |(options, data_model_name, dataset_name, search_mode)| DataModelCommand {
                data_model_name: data_model_name.map(|s| s.0),
                dataset_name: dataset_name.map(|s| s.0),
                search_mode: search_mode.map(|s| s.to_string()),
                strict_fields: options.strict_fields,
                allow_old_summaries: options.allow_old_summaries,
                summaries_only: options.summaries_only,
            },
        )
        .parse(input)
    }
}
