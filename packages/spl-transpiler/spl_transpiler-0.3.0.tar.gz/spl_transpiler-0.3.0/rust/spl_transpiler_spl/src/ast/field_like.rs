use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub enum FieldLike {
    Field(Field),
    Wildcard(Wildcard),
    AliasedField(AliasedField),
    Alias(Alias),
}

impl From<Field> for FieldLike {
    fn from(val: Field) -> Self {
        FieldLike::Field(val)
    }
}

impl From<Wildcard> for FieldLike {
    fn from(val: Wildcard) -> Self {
        FieldLike::Wildcard(val)
    }
}

impl From<AliasedField> for FieldLike {
    fn from(val: AliasedField) -> Self {
        FieldLike::AliasedField(val)
    }
}

impl From<Alias> for FieldLike {
    fn from(val: Alias) -> Self {
        FieldLike::Alias(val)
    }
}
