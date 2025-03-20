use crate::ast::ParsedCommandOptions;
use crate::commands::CommandBase;
use crate::parser::{command_options, unwrapped};
use nom::branch::alt;
use nom::bytes::complete::tag_no_case;
use nom::character::complete::multispace1;
use nom::combinator::{eof, map};
use nom::sequence::preceded;
use nom::{IResult, Parser};

pub trait SplCommandOptions: TryFrom<ParsedCommandOptions, Error = anyhow::Error> {
    fn match_options(input: &str) -> IResult<&str, Self> {
        unwrapped(map(command_options, |opts| Self::try_from(opts.into()))).parse(input)
    }
}

pub struct NoOptions {}

impl TryFrom<ParsedCommandOptions> for NoOptions {
    type Error = anyhow::Error;

    fn try_from(_: ParsedCommandOptions) -> Result<Self, Self::Error> {
        Ok(NoOptions {})
    }
}

pub trait SplCommand<T> {
    type RootCommand: CommandBase;
    type Options: SplCommandOptions;

    fn parse_body(input: &str) -> IResult<&str, T>;

    fn parse(input: &str) -> IResult<&str, T> {
        preceded(Self::match_name, Self::parse_body).parse(input)
    }

    fn match_name_raw(input: &str) -> IResult<&str, ()> {
        match Self::RootCommand::ALIAS {
            Some(alias) => map(
                alt((tag_no_case(Self::RootCommand::NAME), tag_no_case(alias))),
                |_| (),
            )
            .parse(input),
            None => map(tag_no_case(Self::RootCommand::NAME), |_| ()).parse(input),
        }
    }

    fn match_name(input: &str) -> IResult<&str, ()> {
        map((Self::match_name_raw, alt((multispace1, eof))), |_| ()).parse(input)
    }
}
