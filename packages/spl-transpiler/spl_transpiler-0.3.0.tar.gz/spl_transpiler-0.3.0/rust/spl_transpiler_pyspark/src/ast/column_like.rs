use crate::ast::Expr;
use crate::utils::escape_maybe_dotted;
use crate::{PysparkTranspileContext, PythonCode, ToSparkQuery};
use spl_transpiler_common::aliasable::Aliasable;

#[derive(Debug, PartialEq, Clone, Hash)]
// #[pyclass(frozen,eq,hash)]
pub enum ColumnLike {
    Named {
        name: String,
    },
    Literal {
        code: String,
    },
    MethodCall {
        col: Box<Expr>,
        func: String,
        args: Vec<Expr>,
    },
    GetAttribute {
        col: Box<Expr>,
        attribute: String,
    },
    FunctionCall {
        func: String,
        args: Vec<Expr>,
    },
    Aliased {
        col: Box<Expr>,
        name: String,
    },
    BinaryOp {
        op: String,
        left: Box<Expr>,
        right: Box<Expr>,
    },
    UnaryNot {
        right: Box<Expr>,
    },
}

impl ColumnLike {
    pub fn named(name: impl ToString) -> Self {
        ColumnLike::Named {
            name: name.to_string(),
        }
    }

    pub fn literal(code: impl ToString) -> Self {
        ColumnLike::Literal {
            code: code.to_string(),
        }
    }

    pub fn string_literal(code: impl ToString) -> Self {
        ColumnLike::Literal {
            code: format!("\"{}\"", code.to_string()),
        }
    }

    pub fn method_call(col: impl Into<Expr>, func: impl ToString, args: Vec<Expr>) -> Self {
        Self::try_method_call(col, func, args).unwrap()
    }

    pub fn get_attribute(col: impl Into<Expr>, attribute: impl ToString) -> Self {
        let col: Expr = col.into();
        ColumnLike::GetAttribute {
            col: Box::new(col.unaliased()),
            attribute: attribute.to_string(),
        }
    }

    pub fn try_method_call(
        col: impl TryInto<Expr, Error = impl Into<anyhow::Error> + Send>,
        func: impl ToString,
        args: Vec<Expr>,
    ) -> anyhow::Result<Self> {
        let col: Expr = col.try_into().map_err(|e| e.into())?;
        Ok(ColumnLike::MethodCall {
            col: Box::new(col.unaliased()),
            func: func.to_string(),
            args,
        })
    }

    pub fn function_call(func: impl ToString, args: Vec<Expr>) -> Self {
        ColumnLike::FunctionCall {
            func: func.to_string(),
            args,
        }
    }

    pub fn aliased(col: impl Into<Expr>, name: impl ToString) -> Self {
        Self::try_aliased(col, name).unwrap()
    }

    pub fn try_aliased(
        col: impl TryInto<Expr, Error = impl Into<anyhow::Error> + Send>,
        name: impl ToString,
    ) -> anyhow::Result<Self> {
        let col: Expr = col.try_into().map_err(|e| e.into())?;
        Ok(ColumnLike::Aliased {
            col: Box::new(col.unaliased()),
            name: name.to_string(),
        })
    }

    pub fn binary_op(left: impl Into<Expr>, op: impl ToString, right: impl Into<Expr>) -> Self {
        Self::try_binary_op(left, op, right).unwrap()
    }

    pub fn try_binary_op(
        left: impl TryInto<Expr, Error = impl Into<anyhow::Error> + Send>,
        op: impl ToString,
        right: impl TryInto<Expr, Error = impl Into<anyhow::Error> + Send>,
    ) -> anyhow::Result<Self> {
        let left: Expr = left.try_into().map_err(|e| e.into())?;
        let right: Expr = right.try_into().map_err(|e| e.into())?;
        Ok(ColumnLike::BinaryOp {
            left: Box::new(left.unaliased()),
            op: op.to_string(),
            right: Box::new(right.unaliased()),
        })
    }

    pub fn unary_not(right: impl Into<Expr>) -> Self {
        Self::try_unary_not(right).unwrap()
    }

    pub fn try_unary_not(
        right: impl TryInto<Expr, Error = impl Into<anyhow::Error> + Send>,
    ) -> anyhow::Result<Self> {
        let right: Expr = right.try_into().map_err(|e| e.into())?;
        Ok(ColumnLike::UnaryNot {
            right: Box::new(right.unaliased()),
        })
    }
}

impl ToSparkQuery for ColumnLike {
    fn to_spark_query(&self, ctx: &PysparkTranspileContext) -> anyhow::Result<PythonCode> {
        match self {
            ColumnLike::Named { name } => Ok(format!("F.col('{}')", escape_maybe_dotted(name))),
            ColumnLike::Literal { code } => Ok(format!("F.lit({})", code)),
            ColumnLike::MethodCall { col, func, args } => {
                let args: anyhow::Result<Vec<String>> = args
                    .iter()
                    .map(|e| e.to_spark_query(ctx).map(|code| code.to_string()))
                    .collect();
                Ok(format!(
                    "{}.{}({})",
                    col.to_spark_query(ctx)?,
                    func,
                    args?.join(", ")
                ))
            }
            ColumnLike::FunctionCall { func, args } => {
                let args: anyhow::Result<Vec<String>> = args
                    .iter()
                    .map(|e| e.to_spark_query(ctx).map(|code| code.to_string()))
                    .collect();
                let func = if func.contains(".") {
                    func.clone()
                } else {
                    format!("F.{}", func)
                };
                Ok(format!("{}({})", func, args?.join(", ")))
            }
            ColumnLike::Aliased { col, name } => {
                Ok(format!("{}.alias('{}')", col.to_spark_query(ctx)?, name))
            }
            ColumnLike::BinaryOp { op, left, right } => Ok(format!(
                "{} {} {}",
                left.to_spark_query(ctx)?,
                op,
                right.to_spark_query(ctx)?,
            )),
            ColumnLike::UnaryNot { right } => Ok(format!("~{}", right.to_spark_query(ctx)?,)),
            ColumnLike::GetAttribute { col, attribute } => {
                Ok(format!("{}.{}", col.to_spark_query(ctx)?, attribute))
            }
        }
        .map(Into::into)
    }
}

impl From<bool> for ColumnLike {
    fn from(val: bool) -> Self {
        ColumnLike::literal(if val { "True" } else { "False" })
    }
}

impl From<&str> for ColumnLike {
    fn from(val: &str) -> Self {
        ColumnLike::string_literal(val)
    }
}

impl From<String> for ColumnLike {
    fn from(val: String) -> Self {
        ColumnLike::string_literal(val)
    }
}

macro_rules! column_like {
    ($name: ident) => { $name };
    (col($name: expr)) => { crate::ast::ColumnLike::named($name) };
    (lit(true)) => { crate::ast::ColumnLike::from(true) };
    (lit(false)) => { crate::ast::ColumnLike::from(false) };
    (lit(None)) => { crate::ast::ColumnLike::literal("None") };
    (lit($code: literal)) => { crate::ast::ColumnLike::literal(stringify!($code)) };
    (lit($code: expr)) => { crate::ast::ColumnLike::from($code) };
    // (py_lit($code: literal)) => { Raw::from($code) };
    (py_lit($code: expr)) => { crate::ast::PyLiteral::from($code) };
    (expr($fmt: literal $($args:tt)*)) => { crate::ast::ColumnLike::function_call(
        "expr",
        vec![PyLiteral::from( format!($fmt $($args)*) ).into()],
    ) };
    ([$($base: tt)*] . alias ( $name: expr ) ) => { crate::ast::ColumnLike::aliased(
        column_like!($($base)*),
        $name
    ) };
    ([$($base: tt)*] . $method: ident ( $([$($args: tt)*]),* )) => { crate::ast::ColumnLike::method_call(
        column_like!($($base)*),
        stringify!($method),
        vec![$(column_like!($($args)*).into()),*],
    ) };
    ([$($base: tt)*] . $attribute: ident) => { crate::ast::ColumnLike::get_attribute(
        column_like!($($base)*),
        stringify!($attribute)
    ) };
    ($function: ident ( $([$($args: tt)*]),* )) => { crate::ast::ColumnLike::function_call(
        stringify!($function),
        vec![$(column_like!($($args)*).into()),*],
    ) };
    ($function: ident ( $args: expr )) => { crate::ast::ColumnLike::function_call(
        stringify!($function),
        $args,
    ) };
    ([$($left: tt)*] $op: tt [$($right: tt)*]) => { crate::ast::ColumnLike::binary_op(
        column_like!($($left)*),
        stringify!($op),
        column_like!($($right)*),
    ) };
    (~ [$($right: tt)*]) => { crate::ast::ColumnLike::unary_not(
        column_like!($($right)*),
    ) };
    ($e: expr) => { $e };
}

pub(crate) use column_like;
