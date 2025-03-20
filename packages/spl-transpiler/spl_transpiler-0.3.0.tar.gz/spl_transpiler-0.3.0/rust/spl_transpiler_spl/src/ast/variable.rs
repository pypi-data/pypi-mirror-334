use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct Variable(pub String);

impl<S: ToString> From<S> for Variable {
    fn from(value: S) -> Variable {
        Variable(value.to_string())
    }
}
