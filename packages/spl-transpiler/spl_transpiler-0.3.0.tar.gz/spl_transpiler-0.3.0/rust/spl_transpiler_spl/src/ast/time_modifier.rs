use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub enum TimeModifier {
    StartTime(String),
    EndTime(String),
    Earliest(SnapTime),
    Latest(SnapTime),
}

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct FormattedTimeModifier {
    pub format: String,
    pub time_modifier: TimeModifier,
}
