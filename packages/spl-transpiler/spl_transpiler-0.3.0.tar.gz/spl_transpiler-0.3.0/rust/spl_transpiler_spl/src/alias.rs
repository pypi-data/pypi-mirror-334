use crate::ast;

use spl_transpiler_common::aliasable::Aliasable;

impl Aliasable for ast::Expr {
    fn unaliased_with_name(&self) -> (Self, Option<String>) {
        match self {
            ast::Expr::Alias(ast::Alias { expr, name }) => {
                let (expr, _) = (*expr).unaliased_with_name();
                (expr, Some(name.clone()))
            }
            ast::Expr::AliasedField(ast::AliasedField { field, alias }) => {
                (field.clone().into(), Some(alias.clone()))
            }
            _ => (self.clone(), None),
        }
    }
}

impl ast::Expr {
    pub fn with_alias(&self, name: String) -> Self {
        ast::Expr::Alias(ast::Alias {
            expr: Box::new(self.clone()),
            name,
        })
    }

    pub fn maybe_with_alias(&self, name: Option<String>) -> Self {
        match name {
            Some(n) => self.with_alias(n),
            None => self.clone(),
        }
    }
}
