use crate::ast::{ColumnLike, Expr, RuntimeExpr};
use spl_transpiler_common::aliasable::Aliasable;

impl Aliasable for ColumnLike {
    fn unaliased_with_name(&self) -> (Self, Option<String>) {
        match self {
            ColumnLike::Aliased { col, name } => match *col.clone() {
                Expr::Column(col) => (col.unaliased(), Some(name.clone())),
                _ => (self.clone(), Some(name.clone())),
            },
            _ => (self.clone(), None),
        }
    }
}

impl Aliasable for Expr {
    fn unaliased_with_name(&self) -> (Self, Option<String>) {
        match self {
            Expr::Column(col) => {
                let (c, name) = col.unaliased_with_name();
                (c.into(), name)
            }
            _ => (self.clone(), None),
        }
    }
}

impl Aliasable for RuntimeExpr {
    fn unaliased_with_name(&self) -> (Self, Option<String>) {
        match self {
            RuntimeExpr::Expr(expr) => {
                let (expr, name) = expr.unaliased_with_name();
                (expr.into(), name)
            }
            _ => (self.clone(), None),
        }
    }
}

impl ColumnLike {
    pub fn with_alias(&self, name: String) -> Self {
        ColumnLike::aliased(self.unaliased(), name)
    }

    pub fn maybe_with_alias(&self, name: Option<String>) -> Self {
        match name {
            Some(n) => self.with_alias(n),
            None => self.clone(),
        }
    }
}

impl Expr {
    pub fn with_alias(&self, name: String) -> Self {
        ColumnLike::aliased(self.clone(), name).into()
    }

    pub fn maybe_with_alias(&self, name: Option<String>) -> Self {
        match name {
            Some(n) => self.with_alias(n),
            None => self.clone(),
        }
    }
}
