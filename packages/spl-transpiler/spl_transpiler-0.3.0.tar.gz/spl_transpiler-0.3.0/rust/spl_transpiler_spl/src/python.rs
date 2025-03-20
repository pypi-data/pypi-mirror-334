use crate::ast;
use pyo3::prelude::*;

macro_rules! impl_pyclass {
    ($name: ty { $arg_tp: ty }) => {
        #[pymethods]
        impl $name {
            #[allow(clippy::too_many_arguments)]
            #[new]
            fn py_new(value: $arg_tp) -> Self {
                Self ( value )
            }

            fn __repr__(&self) -> String {
                format!("{:?}", self)
            }
        }
    };
    ($name: path {$($arg: ident : $arg_tp: ty),*}) => {
        #[pymethods]
        impl $name {
            #[allow(clippy::too_many_arguments)]
            #[new]
            fn py_new($($arg: $arg_tp),*) -> Self {
                Self { $($arg),* }
            }

            fn __repr__(&self) -> String {
                format!("{:?}", self)
            }
        }
    };
}

pub(crate) use impl_pyclass;

// impl_pyclass!(ast::NullValue ());
impl_pyclass!(ast::BoolValue { bool });
impl_pyclass!(ast::IntValue { i64 });
impl_pyclass!(ast::StrValue { String });
impl_pyclass!(ast::DoubleValue { f64 });
impl_pyclass!(ast::TimeSpan {
    value: i64,
    scale: String
});
impl_pyclass!(ast::SnapTime { span: Option<ast::TimeSpan>, snap: String, snap_offset: Option<ast::TimeSpan> });
impl_pyclass!(ast::Field { String });
impl_pyclass!(ast::Wildcard { String });
impl_pyclass!(ast::Variable { String });
impl_pyclass!(ast::IPv4CIDR { String });
impl_pyclass!(ast::FV {
    field: String,
    value: String
});
impl_pyclass!(ast::FB {
    field: String,
    value: bool
});
impl_pyclass!(ast::FC {
    field: String,
    value: ast::Constant
});
impl_pyclass!(ast::CommandOptions { options: Vec<ast::FC> });
impl_pyclass!(ast::AliasedField {
    field: ast::Field,
    alias: String
});
// impl_pyclass!(ast::Binary { |left: ast::Expr| Box::new(left), |symbol: String| symbol, |right: ast::Expr| Box::new(right) } {{}});
// impl_pyclass!(ast::Unary { |symbol: String| symbol, |right: ast::Expr| Box::new(right) });
impl_pyclass!(ast::Call { name: String, args: Vec<ast::Expr> });
impl_pyclass!(ast::FieldIn { field: String, exprs: Vec<ast::Expr> });
// impl_pyclass!(ast::Alias { |expr: ast::Expr| Box::new(expr), |name: String| name });

impl_pyclass!(ast::Pipeline { commands: Vec<ast::Command> });

#[pymethods]
impl ast::Binary {
    #[new]
    fn py_new(left: ast::Expr, symbol: String, right: ast::Expr) -> Self {
        Self {
            left: Box::new(left),
            symbol,
            right: Box::new(right),
        }
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }

    #[getter]
    fn left(&self) -> ast::Expr {
        (*self.left).clone()
    }

    #[getter]
    fn right(&self) -> ast::Expr {
        (*self.right).clone()
    }
}

#[pymethods]
impl ast::Unary {
    #[new]
    fn py_new(symbol: String, right: ast::Expr) -> Self {
        Self {
            symbol,
            right: Box::new(right),
        }
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }

    #[getter]
    fn right(&self) -> ast::Expr {
        (*self.right).clone()
    }
}

#[pymethods]
impl ast::Alias {
    #[new]
    fn py_new(expr: ast::Expr, name: String) -> Self {
        Self {
            expr: Box::new(expr),
            name,
        }
    }

    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }

    #[getter]
    fn expr(&self) -> ast::Expr {
        (*self.expr).clone()
    }
}

pub fn ast_pymodule(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<ast::NullValue>()?;
    m.add_class::<ast::BoolValue>()?;
    m.add_class::<ast::IntValue>()?;
    m.add_class::<ast::StrValue>()?;
    m.add_class::<ast::DoubleValue>()?;
    m.add_class::<ast::TimeSpan>()?;
    m.add_class::<ast::SnapTime>()?;
    m.add_class::<ast::Field>()?;
    m.add_class::<ast::Wildcard>()?;
    m.add_class::<ast::Variable>()?;
    m.add_class::<ast::IPv4CIDR>()?;
    m.add_class::<ast::FV>()?;
    m.add_class::<ast::FB>()?;
    m.add_class::<ast::FC>()?;
    m.add_class::<ast::AliasedField>()?;
    m.add_class::<ast::Binary>()?;
    m.add_class::<ast::Unary>()?;
    m.add_class::<ast::Call>()?;
    m.add_class::<ast::FieldIn>()?;
    m.add_class::<ast::Alias>()?;

    m.add_class::<crate::commands::cmd::search::SearchCommand>()?;
    m.add_class::<crate::commands::cmd::eval::EvalCommand>()?;
    m.add_class::<crate::commands::cmd::convert::FieldConversion>()?;
    m.add_class::<crate::commands::cmd::convert::ConvertCommand>()?;
    m.add_class::<crate::commands::cmd::lookup::LookupOutput>()?;
    m.add_class::<crate::commands::cmd::lookup::LookupCommand>()?;
    m.add_class::<crate::commands::cmd::collect::CollectCommand>()?;
    m.add_class::<crate::commands::cmd::where_::WhereCommand>()?;
    m.add_class::<crate::commands::cmd::table::TableCommand>()?;
    m.add_class::<crate::commands::cmd::head::HeadCommand>()?;
    m.add_class::<crate::commands::cmd::fields::FieldsCommand>()?;
    m.add_class::<crate::commands::cmd::sort::SortCommand>()?;
    m.add_class::<crate::commands::cmd::stats::StatsCommand>()?;
    m.add_class::<crate::commands::cmd::rex::RexCommand>()?;
    m.add_class::<crate::commands::cmd::rename::RenameCommand>()?;
    m.add_class::<crate::commands::cmd::regex::RegexCommand>()?;
    m.add_class::<crate::commands::cmd::join::JoinCommand>()?;
    m.add_class::<crate::commands::cmd::return_::ReturnCommand>()?;
    m.add_class::<crate::commands::cmd::fill_null::FillNullCommand>()?;
    m.add_class::<crate::commands::cmd::event_stats::EventStatsCommand>()?;
    m.add_class::<crate::commands::cmd::stream_stats::StreamStatsCommand>()?;
    m.add_class::<crate::commands::cmd::dedup::DedupCommand>()?;
    m.add_class::<crate::commands::cmd::input_lookup::InputLookupCommand>()?;
    m.add_class::<crate::commands::cmd::format::FormatCommand>()?;
    m.add_class::<crate::commands::cmd::mv_combine::MvCombineCommand>()?;
    m.add_class::<crate::commands::cmd::mv_expand::MvExpandCommand>()?;
    m.add_class::<crate::commands::cmd::make_results::MakeResultsCommand>()?;
    m.add_class::<crate::commands::cmd::add_totals::AddTotalsCommand>()?;
    m.add_class::<crate::commands::cmd::bin::BinCommand>()?;
    m.add_class::<crate::commands::cmd::multi_search::MultiSearchCommand>()?;
    m.add_class::<crate::commands::cmd::map::MapCommand>()?;
    m.add_class::<ast::Pipeline>()?;

    m.add_class::<ast::Constant>()?;
    m.add_class::<ast::LeafExpr>()?;
    m.add_class::<ast::Expr>()?;
    m.add_class::<ast::FieldLike>()?;
    m.add_class::<ast::FieldOrAlias>()?;
    m.add_class::<ast::Command>()?;

    Ok(())
}
