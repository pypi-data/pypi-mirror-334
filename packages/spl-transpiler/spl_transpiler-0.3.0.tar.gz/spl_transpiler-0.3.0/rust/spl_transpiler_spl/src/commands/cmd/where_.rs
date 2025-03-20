use crate::ast::{Expr, ParsedCommandOptions};
use crate::commands::base::{SplCommand, SplCommandOptions};
use crate::parser::logical_expression;
use crate::python::*;
use nom::combinator::map;
use nom::{IResult, Parser};
use pyo3::prelude::*;
//   // where <predicate-expression>
//   def where[_: P]: P[WhereCommand] = "where" ~ expr map WhereCommand

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct WhereCommand {
    #[pyo3(get)]
    pub expr: Expr,
}
impl_pyclass!(WhereCommand { expr: Expr });

#[derive(Debug, Default)]
pub struct WhereParser {}
pub struct WhereCommandOptions {}

impl SplCommandOptions for WhereCommandOptions {}

impl TryFrom<ParsedCommandOptions> for WhereCommandOptions {
    type Error = anyhow::Error;

    fn try_from(_value: ParsedCommandOptions) -> Result<Self, Self::Error> {
        Ok(Self {})
    }
}

impl SplCommand<WhereCommand> for WhereParser {
    type RootCommand = crate::commands::WhereCommandRoot;
    type Options = WhereCommandOptions;

    fn parse_body(input: &str) -> IResult<&str, WhereCommand> {
        map(logical_expression, |v| WhereCommand { expr: v }).parse(input)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::ast;
    use crate::parser::pipeline;
    use crate::utils::test::*;
    use rstest::rstest;

    //
    //   test("where isnull(reason)") {
    //     p(pipeline(_), Pipeline(Seq(
    //       WhereCommand(
    //         Call(
    //           "isnull",Seq(
    //             Field("reason")
    //           )
    //         )
    //       )
    //     )))
    //   }
    #[rstest]
    fn test_pipeline_where_6() {
        assert_eq!(
            pipeline("where isnull(reason)"),
            Ok((
                "",
                ast::Pipeline {
                    commands: vec![WhereCommand {
                        expr: _call!(isnull(ast::Field::from("reason"))).into()
                    }
                    .into()],
                }
            ))
        )
    }
}
