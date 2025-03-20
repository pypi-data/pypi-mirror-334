use pyo3::pyclass;

/// Syntax tree element representing a boolean literal value.
#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct BoolValue(pub bool);

impl<T: Into<bool>> From<T> for BoolValue {
    fn from(value: T) -> Self {
        BoolValue(value.into())
    }
}
