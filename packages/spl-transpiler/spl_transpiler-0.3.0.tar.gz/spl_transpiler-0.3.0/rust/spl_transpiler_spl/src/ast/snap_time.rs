use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct SnapTime {
    #[pyo3(get)]
    pub span: Option<TimeSpan>,
    #[pyo3(get)]
    pub snap: String,
    #[pyo3(get)]
    pub snap_offset: Option<TimeSpan>,
}
