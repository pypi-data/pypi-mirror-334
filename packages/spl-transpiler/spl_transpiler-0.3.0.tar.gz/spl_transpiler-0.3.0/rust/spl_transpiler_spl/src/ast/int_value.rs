use pyo3::pyclass;

/// Syntax tree element representing an integer literal value.
#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct IntValue(pub i64);

impl<T: Into<i64>> From<T> for IntValue {
    fn from(value: T) -> Self {
        IntValue(value.into())
    }
}
