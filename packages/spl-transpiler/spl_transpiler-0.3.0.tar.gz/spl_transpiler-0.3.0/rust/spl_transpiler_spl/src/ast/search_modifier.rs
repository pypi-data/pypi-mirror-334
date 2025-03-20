use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub enum SearchModifier {
    SourceType(String),
    Host(String),
    HostTag(String),
    EventType(String),
    EventTypeTag(String),
    SavedSplunk(String),
    Source(String),
    SplunkServer(String),
}
