use pyo3::pyclass;

/// Syntax tree element representing a duration with a value and a scale.
///
/// # Fields
///
/// * `value` - An integer representing the duration of the time span.
/// * `scale` - A string representing the unit of the time span (e.g., "seconds", "minutes").
#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct TimeSpan {
    #[pyo3(get)]
    pub value: i64,
    #[pyo3(get)]
    pub scale: String,
}
