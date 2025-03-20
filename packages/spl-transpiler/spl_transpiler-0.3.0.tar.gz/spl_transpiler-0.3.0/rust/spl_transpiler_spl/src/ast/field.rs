use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct Field(pub String);

impl<S: ToString> From<S> for Field {
    fn from(value: S) -> Field {
        Field(value.to_string())
    }
}
