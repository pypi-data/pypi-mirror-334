use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub enum Constant {
    Null(NullValue),
    Bool(BoolValue),
    Int(IntValue),
    Double(DoubleValue),
    Str(StrValue),
    SnapTime(SnapTime),
    TimeSpan(TimeSpan),
    Field(Field),
    Wildcard(Wildcard),
    Variable(Variable),
    IPv4CIDR(IPv4CIDR),
}

impl From<TimeSpan> for Constant {
    fn from(val: TimeSpan) -> Self {
        Constant::TimeSpan(val)
    }
}

impl From<BoolValue> for Constant {
    fn from(val: BoolValue) -> Self {
        Constant::Bool(val)
    }
}

impl From<IntValue> for Constant {
    fn from(val: IntValue) -> Self {
        Constant::Int(val)
    }
}

impl From<DoubleValue> for Constant {
    fn from(val: DoubleValue) -> Self {
        Constant::Double(val)
    }
}

impl From<StrValue> for Constant {
    fn from(val: StrValue) -> Self {
        Constant::Str(val)
    }
}

impl From<SnapTime> for Constant {
    fn from(val: SnapTime) -> Self {
        Constant::SnapTime(val)
    }
}

impl From<Field> for Constant {
    fn from(val: Field) -> Self {
        Constant::Field(val)
    }
}

impl From<Wildcard> for Constant {
    fn from(val: Wildcard) -> Self {
        Constant::Wildcard(val)
    }
}

impl From<Variable> for Constant {
    fn from(val: Variable) -> Self {
        Constant::Variable(val)
    }
}

impl From<IPv4CIDR> for Constant {
    fn from(val: IPv4CIDR) -> Self {
        Constant::IPv4CIDR(val)
    }
}
