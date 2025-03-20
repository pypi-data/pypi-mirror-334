use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct FB {
    #[pyo3(get)]
    pub field: String,
    #[pyo3(get)]
    pub value: bool,
}
