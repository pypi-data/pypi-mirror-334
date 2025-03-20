use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct Wildcard(pub String);

impl<S: ToString> From<S> for Wildcard {
    fn from(value: S) -> Wildcard {
        Wildcard(value.to_string())
    }
}
