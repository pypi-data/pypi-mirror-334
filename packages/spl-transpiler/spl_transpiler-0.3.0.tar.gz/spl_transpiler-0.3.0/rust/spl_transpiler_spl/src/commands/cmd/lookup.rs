use crate::ast::{FieldLike, ParsedCommandOptions};
use crate::commands::base::{SplCommand, SplCommandOptions};
use crate::parser::{aliased_field, comma_or_space_separated_list1, field, token, ws};
use crate::python::*;
use nom::branch::alt;
use nom::bytes::complete::tag_no_case;
use nom::character::complete::multispace1;
use nom::combinator::{into, map, opt, verify};
use nom::sequence::separated_pair;
use nom::{IResult, Parser};
use pyo3::prelude::*;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct LookupOutput {
    #[pyo3(get)]
    pub kv: String,
    #[pyo3(get)]
    pub fields: Vec<FieldLike>,
}

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct LookupCommand {
    #[pyo3(get)]
    pub dataset: String,
    #[pyo3(get)]
    pub fields: Vec<FieldLike>,
    #[pyo3(get)]
    pub output: Option<LookupOutput>,
}
impl_pyclass!(LookupOutput { kv: String, fields: Vec<FieldLike> });
impl_pyclass!(LookupCommand { dataset: String, fields: Vec<FieldLike>, output: Option<LookupOutput> });

//   def fieldRep[_: P]: P[Seq[FieldLike]] = (aliasedField | field).filter {
//     case Alias(Field(field), _) => field.toLowerCase() != "output"
//     case Field(v) => v.toLowerCase(Locale.ROOT) != "output"
//     case _ => false
//   }.rep(1)
pub fn field_rep(input: &str) -> IResult<&str, Vec<FieldLike>> {
    comma_or_space_separated_list1(alt((
        into(verify(aliased_field, |v| {
            !(v.alias.eq_ignore_ascii_case("output") || v.field.0.eq_ignore_ascii_case("output"))
        })),
        into(verify(field, |v| !v.0.eq_ignore_ascii_case("output"))),
    )))
    .parse(input)
}

//
//   def lookupOutput[_: P]: P[LookupOutput] =
//     (W("OUTPUT")|W("OUTPUTNEW")).! ~ fieldRep map LookupOutput.tupled
fn lookup_output(input: &str) -> IResult<&str, LookupOutput> {
    map(
        separated_pair(
            alt((tag_no_case("OUTPUT"), tag_no_case("OUTPUTNEW"))),
            multispace1,
            field_rep,
        ),
        |(kv, fields)| LookupOutput {
            kv: kv.to_string().to_ascii_lowercase(),
            fields,
        },
    )
    .parse(input)
}

//
//   def lookup[_: P]: P[LookupCommand] =
//     "lookup" ~ token ~ fieldRep ~ lookupOutput.? map LookupCommand.tupled

#[derive(Debug, Default)]
pub struct LookupParser {}
pub struct LookupCommandOptions {}

impl SplCommandOptions for LookupCommandOptions {}

impl TryFrom<ParsedCommandOptions> for LookupCommandOptions {
    type Error = anyhow::Error;

    fn try_from(_value: ParsedCommandOptions) -> Result<Self, Self::Error> {
        Ok(Self {})
    }
}

impl SplCommand<LookupCommand> for LookupParser {
    type RootCommand = crate::commands::LookupCommandRoot;
    type Options = LookupCommandOptions;

    fn parse_body(input: &str) -> IResult<&str, LookupCommand> {
        map(
            (ws(token), ws(field_rep), ws(opt(lookup_output))),
            |(token, fields, output)| LookupCommand {
                dataset: token.to_string(),
                fields,
                output,
            },
        )
        .parse(input)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::ast;
    use crate::parser::pipeline;
    use rstest::rstest;

    //
    //   test("lookup process_create_whitelist a b output reason") {
    //     p(pipeline(_), Pipeline(Seq(
    //       LookupCommand(
    //         "process_create_whitelist",
    //         Seq(
    //           Field("a"),
    //           Field("b")
    //         ),
    //         Some(
    //           LookupOutput(
    //             "output",
    //             Seq(
    //               Field("reason")
    //             )
    //           )
    //         )
    //       )
    //     )))
    //   }
    #[rstest]
    fn test_pipeline_lookup_5() {
        let _lookup_cmd = LookupCommand {
            dataset: "process_create_whitelist".to_string(),
            fields: vec![ast::Field::from("a").into(), ast::Field::from("b").into()],
            output: Some(LookupOutput {
                kv: "output".to_string(),
                fields: vec![ast::Field::from("reason").into()],
            }),
        };
        assert_eq!(
            LookupParser::parse("lookup process_create_whitelist a b output reason"),
            Ok(("", _lookup_cmd.clone()))
        );
        assert_eq!(
            pipeline("lookup process_create_whitelist a b output reason"),
            Ok((
                "",
                ast::Pipeline {
                    commands: vec![_lookup_cmd.clone().into()],
                }
            ))
        )
    }

    #[rstest]
    fn test_pipeline_lookup_6_field_rep() {
        assert_eq!(
            field_rep("group as user_group"),
            Ok((
                "",
                vec![ast::AliasedField {
                    field: ast::Field::from("group"),
                    alias: "user_group".to_string(),
                }
                .into()]
            ))
        );
    }

    #[rstest]
    fn test_pipeline_lookup_6_lookup_output() {
        assert_eq!(
            lookup_output("OUTPUT group as user_group"),
            Ok((
                "",
                LookupOutput {
                    kv: "output".to_string(),
                    fields: vec![ast::AliasedField {
                        field: ast::Field::from("group"),
                        alias: "user_group".to_string(),
                    }
                    .into()],
                }
            ))
        );
    }

    #[rstest]
    fn test_pipeline_lookup_6() {
        assert_eq!(
            LookupParser::parse("lookup usertogroup user as local_user OUTPUT group as user_group"),
            Ok((
                "",
                LookupCommand {
                    dataset: "usertogroup".to_string(),
                    fields: vec![ast::AliasedField {
                        field: ast::Field::from("user"),
                        alias: "local_user".to_string(),
                    }
                    .into()],
                    output: Some(LookupOutput {
                        kv: "output".to_string(),
                        fields: vec![ast::AliasedField {
                            field: ast::Field::from("group"),
                            alias: "user_group".to_string(),
                        }
                        .into(),],
                    }),
                }
            ))
        );
    }
}
