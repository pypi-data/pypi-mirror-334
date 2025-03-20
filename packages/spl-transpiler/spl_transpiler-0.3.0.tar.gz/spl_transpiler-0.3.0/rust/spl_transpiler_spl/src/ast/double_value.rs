use float_derive::FloatHash;
use pyo3::pyclass;

/// Syntax tree element representing a floating-point literal value.
#[derive(Debug, PartialEq, Clone, FloatHash)]
#[pyclass(frozen, eq, hash)]
pub struct DoubleValue(pub f64);

impl<T: Into<f64>> From<T> for DoubleValue {
    fn from(value: T) -> Self {
        DoubleValue(value.into())
    }
}
