use super::*;
use pyo3::pyclass;

/// A pipeline is a chain of commands where data is passed and processed by each command in turn.
#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct Pipeline {
    #[pyo3(get)]
    pub commands: Vec<Command>,
}
