use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct FV {
    #[pyo3(get)]
    pub field: String,
    #[pyo3(get)]
    pub value: String,
}
