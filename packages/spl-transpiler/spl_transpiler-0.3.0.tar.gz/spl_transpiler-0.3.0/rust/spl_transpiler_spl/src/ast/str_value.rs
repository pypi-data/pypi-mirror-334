use pyo3::pyclass;

/// Syntax tree element representing a string literal value.
#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct StrValue(pub String);

impl<T: ToString> From<T> for StrValue {
    fn from(value: T) -> Self {
        StrValue(value.to_string())
    }
}
