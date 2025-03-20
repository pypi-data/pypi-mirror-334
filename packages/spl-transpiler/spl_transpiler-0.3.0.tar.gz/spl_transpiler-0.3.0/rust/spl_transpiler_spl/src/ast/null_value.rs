use pyo3::pyclass;

/// Syntax tree element representing a null literal value.
#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct NullValue();
