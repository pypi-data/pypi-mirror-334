use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub enum LeafExpr {
    Constant(Constant),
    FV(FV),
    FB(FB),
    FC(FC),
}
