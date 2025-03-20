use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub struct IPv4CIDR(pub String);

impl<S: ToString> From<S> for IPv4CIDR {
    fn from(value: S) -> IPv4CIDR {
        IPv4CIDR(value.to_string())
    }
}
