use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct Binary {
    // #[pyo3(get)]
    pub left: Box<Expr>,
    #[pyo3(get)]
    pub symbol: String,
    // #[pyo3(get)]
    pub right: Box<Expr>,
}

impl Binary {
    pub fn new(left: impl Into<Expr>, symbol: impl ToString, right: impl Into<Expr>) -> Self {
        Self {
            left: Box::new(left.into()),
            symbol: symbol.to_string(),
            right: Box::new(right.into()),
        }
    }
}
