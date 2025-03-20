use super::*;
use anyhow::anyhow;
use pyo3::pyclass;
use std::collections::HashMap;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct CommandOptions {
    #[pyo3(get)]
    pub options: Vec<FC>,
}

pub struct ParsedCommandOptions {
    inner: HashMap<String, Constant>,
}

impl From<CommandOptions> for ParsedCommandOptions {
    fn from(value: CommandOptions) -> Self {
        Self {
            inner: value
                .options
                .iter()
                .cloned()
                .map(|option| (option.field, option.value))
                .collect(),
        }
    }
}

impl ParsedCommandOptions {
    pub fn get_int_option(&self, key: &str) -> Result<Option<i64>, anyhow::Error> {
        match self.inner.get(key) {
            Some(Constant::Int(IntValue(value))) => Ok(Some(*value)),
            Some(_) => Err(anyhow!("not an int")),
            None => Ok(None),
        }
    }

    pub fn get_int(&self, key: &str, default: i64) -> Result<i64, anyhow::Error> {
        self.get_int_option(key).map(|v| v.unwrap_or(default))
    }

    pub fn get_string_option(&self, key: &str) -> Result<Option<String>, anyhow::Error> {
        match self.inner.get(key) {
            Some(Constant::Field(Field(value))) => Ok(Some(value.clone())),
            Some(Constant::Str(StrValue(value))) => Ok(Some(value.clone())),
            Some(_) => Err(anyhow!("not a string")),
            None => Ok(None),
        }
    }

    pub fn get_string(&self, key: &str, default: impl ToString) -> Result<String, anyhow::Error> {
        self.get_string_option(key)
            .map(|v| v.unwrap_or(default.to_string()))
    }

    pub fn get_span_option(&self, key: &str) -> Result<Option<TimeSpan>, anyhow::Error> {
        match self.inner.get(key) {
            Some(Constant::TimeSpan(span)) => Ok(Some(span.clone())),
            Some(_) => Err(anyhow!("not a span")),
            None => Ok(None),
        }
    }

    pub fn get_boolean(&self, key: &str, default: bool) -> Result<bool, anyhow::Error> {
        match self.inner.get(key) {
            Some(Constant::Bool(BoolValue(value))) => Ok(*value),
            Some(Constant::Field(Field(v))) if v == "true" => Ok(true),
            Some(Constant::Field(Field(v))) if v == "t" => Ok(true),
            Some(Constant::Field(Field(v))) if v == "false" => Ok(false),
            Some(Constant::Field(Field(v))) if v == "f" => Ok(false),
            Some(_) => Err(anyhow!("not a bool")),
            None => Ok(default),
        }
    }
}
