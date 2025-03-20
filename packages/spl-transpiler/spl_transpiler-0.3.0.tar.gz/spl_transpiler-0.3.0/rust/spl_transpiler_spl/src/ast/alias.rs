use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct Alias {
    // #[pyo3(get)]
    pub expr: Box<Expr>,
    #[pyo3(get)]
    pub name: String,
}

impl Alias {
    pub fn new(name: impl ToString, expr: impl Into<Expr>) -> Self {
        Self {
            name: name.to_string(),
            expr: Box::new(expr.into()),
        }
    }
}

impl From<AliasedField> for Alias {
    fn from(value: AliasedField) -> Self {
        Alias {
            expr: Box::new(value.field.into()),
            name: value.alias,
        }
    }
}
