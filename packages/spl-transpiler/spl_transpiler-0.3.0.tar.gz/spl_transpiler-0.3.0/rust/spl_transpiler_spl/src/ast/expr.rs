use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub enum Expr {
    Leaf(LeafExpr),
    AliasedField(AliasedField),
    Binary(Binary),
    Unary(Unary),
    Call(Call),
    FieldIn(FieldIn),
    Alias(Alias),
    TimeModifier(FormattedTimeModifier),
    SearchModifier(SearchModifier),
    SubSearch(Pipeline),
}

impl From<Constant> for Expr {
    fn from(val: Constant) -> Self {
        Expr::Leaf(LeafExpr::Constant(val))
    }
}

impl From<TimeSpan> for Expr {
    fn from(val: TimeSpan) -> Self {
        <TimeSpan as Into<Constant>>::into(val).into()
    }
}

impl From<BoolValue> for Expr {
    fn from(val: BoolValue) -> Self {
        <BoolValue as Into<Constant>>::into(val).into()
    }
}

impl From<IntValue> for Expr {
    fn from(val: IntValue) -> Self {
        Expr::Leaf(LeafExpr::Constant(val.into()))
    }
}

impl From<DoubleValue> for Expr {
    fn from(val: DoubleValue) -> Self {
        Expr::Leaf(LeafExpr::Constant(val.into()))
    }
}

impl From<StrValue> for Expr {
    fn from(val: StrValue) -> Self {
        Expr::Leaf(LeafExpr::Constant(val.into()))
    }
}

impl From<SnapTime> for Expr {
    fn from(val: SnapTime) -> Self {
        Expr::Leaf(LeafExpr::Constant(val.into()))
    }
}

impl From<Field> for Expr {
    fn from(val: Field) -> Self {
        Expr::Leaf(LeafExpr::Constant(val.into()))
    }
}

impl From<Wildcard> for Expr {
    fn from(val: Wildcard) -> Self {
        Expr::Leaf(LeafExpr::Constant(val.into()))
    }
}

impl From<Variable> for Expr {
    fn from(val: Variable) -> Self {
        Expr::Leaf(LeafExpr::Constant(val.into()))
    }
}

impl From<IPv4CIDR> for Expr {
    fn from(val: IPv4CIDR) -> Self {
        Expr::Leaf(LeafExpr::Constant(val.into()))
    }
}

impl From<FV> for Expr {
    fn from(val: FV) -> Self {
        Expr::Leaf(LeafExpr::FV(val))
    }
}

impl From<FB> for Expr {
    fn from(val: FB) -> Self {
        Expr::Leaf(LeafExpr::FB(val))
    }
}

impl From<FC> for Expr {
    fn from(val: FC) -> Self {
        Expr::Leaf(LeafExpr::FC(val))
    }
}

impl From<AliasedField> for Expr {
    fn from(val: AliasedField) -> Self {
        Expr::AliasedField(val)
    }
}

impl From<Binary> for Expr {
    fn from(val: Binary) -> Self {
        Expr::Binary(val)
    }
}

impl From<Unary> for Expr {
    fn from(val: Unary) -> Self {
        Expr::Unary(val)
    }
}

impl From<Call> for Expr {
    fn from(val: Call) -> Self {
        Expr::Call(val)
    }
}

impl From<FieldIn> for Expr {
    fn from(val: FieldIn) -> Self {
        Expr::FieldIn(val)
    }
}

impl From<Alias> for Expr {
    fn from(val: Alias) -> Self {
        Expr::Alias(val)
    }
}

impl From<FormattedTimeModifier> for Expr {
    fn from(val: FormattedTimeModifier) -> Self {
        Expr::TimeModifier(val)
    }
}

impl From<SearchModifier> for Expr {
    fn from(val: SearchModifier) -> Self {
        Expr::SearchModifier(val)
    }
}

impl From<Pipeline> for Expr {
    fn from(val: Pipeline) -> Self {
        Expr::SubSearch(val)
    }
}
