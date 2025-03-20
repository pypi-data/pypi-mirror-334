use super::*;
use pyo3::pyclass;

#[derive(Debug, PartialEq, Clone, Hash)]
#[pyclass(frozen, eq, hash)]
pub enum FieldOrAlias {
    Field(Field),
    Alias(Alias),
}

impl From<Field> for FieldOrAlias {
    fn from(val: Field) -> Self {
        FieldOrAlias::Field(val)
    }
}

impl From<Alias> for FieldOrAlias {
    fn from(val: Alias) -> Self {
        FieldOrAlias::Alias(val)
    }
}

impl From<AliasedField> for FieldOrAlias {
    fn from(val: AliasedField) -> Self {
        FieldOrAlias::Alias(val.into())
    }
}
