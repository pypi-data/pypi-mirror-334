use crate::ast::{Field, TimeSpan};
use crate::parser::{comma_or_space_separated_list1, field, time_span, ws};
use nom::branch::alt;
use nom::bytes::complete::tag_no_case;
use nom::character::complete::multispace1;
use nom::combinator::map;
use nom::sequence::{preceded, separated_pair};
use nom::{IResult, Parser};
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct MaybeSpannedField {
    pub field: Field,
    pub span: Option<TimeSpan>,
}

impl From<Field> for MaybeSpannedField {
    fn from(field: Field) -> Self {
        MaybeSpannedField { field, span: None }
    }
}

pub fn maybe_spanned_field(input: &str) -> IResult<&str, MaybeSpannedField> {
    alt((
        map(
            separated_pair(
                field,
                multispace1,
                preceded(ws(tag_no_case("span=")), time_span),
            ),
            |(field, span)| MaybeSpannedField {
                field,
                span: Some(span),
            },
        ),
        map(field, |field| MaybeSpannedField { field, span: None }),
    ))
    .parse(input)
}

pub fn maybe_spanned_field_list1(input: &str) -> IResult<&str, Vec<MaybeSpannedField>> {
    comma_or_space_separated_list1(maybe_spanned_field).parse(input)
}
