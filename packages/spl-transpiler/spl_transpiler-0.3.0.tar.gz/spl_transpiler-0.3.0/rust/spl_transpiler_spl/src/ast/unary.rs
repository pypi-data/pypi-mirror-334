use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct Unary {
    #[pyo3(get)]
    pub symbol: String,
    // #[pyo3(get)]
    pub right: Box<Expr>,
}

impl Unary {
    pub fn new(symbol: impl ToString, right: impl Into<Expr>) -> Self {
        Self {
            symbol: symbol.to_string(),
            right: Box::new(right.into()),
        }
    }
}
