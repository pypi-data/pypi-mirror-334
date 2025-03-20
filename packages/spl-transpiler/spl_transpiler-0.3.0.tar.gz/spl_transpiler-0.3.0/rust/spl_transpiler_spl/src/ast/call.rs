use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct Call {
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub args: Vec<Expr>,
}
