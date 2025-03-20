use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct AliasedField {
    #[pyo3(get)]
    pub field: Field,
    #[pyo3(get)]
    pub alias: String,
}
