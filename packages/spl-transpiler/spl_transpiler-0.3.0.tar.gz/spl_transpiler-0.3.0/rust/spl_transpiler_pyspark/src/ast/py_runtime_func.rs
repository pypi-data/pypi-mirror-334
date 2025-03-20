use crate::ast::PyDict;
use crate::ast::PyList;
use crate::{PysparkTranspileContext, PythonCode, ToSparkQuery};

#[derive(Debug, PartialEq, Clone, Hash)]
pub struct PyRuntimeFunc {
    pub name: String,
    pub args: PyList,
    pub kwargs: PyDict,
}

impl PyRuntimeFunc {
    #[allow(dead_code)]
    pub fn new(name: impl ToString, args: impl Into<PyList>, kwargs: impl Into<PyDict>) -> Self {
        PyRuntimeFunc {
            name: name.to_string(),
            args: args.into(),
            kwargs: kwargs.into(),
        }
    }
}

impl ToSparkQuery for PyRuntimeFunc {
    fn to_spark_query(&self, ctx: &PysparkTranspileContext) -> anyhow::Result<PythonCode> {
        let mut out_preface = vec![];
        let mut out_args = vec![];

        for arg in self.args.0.iter() {
            let PythonCode {
                preface,
                primary_df_code,
            } = arg.to_spark_query(ctx)?;
            out_preface.extend(preface);
            out_args.push(primary_df_code);
        }

        for (key, value) in self.kwargs.0.iter() {
            let PythonCode {
                preface,
                primary_df_code,
            } = value.to_spark_query(ctx)?;
            out_preface.extend(preface);
            out_args.push(format!("{}={}", key, primary_df_code).to_string());
        }

        Ok(format!("functions.{}({})", self.name, out_args.join(", ")).into())
    }
}

#[allow(unused_macros)]
macro_rules! py_runtime_func {
    ($func: ident ( $($arg: expr),* ; $($kwkey: ident = $kwval: expr),* )) => {
        crate::ast::PyRuntimeFunc::new(
            stringify!($func),
            py_list!($($arg),*),
            py_dict!($($kwkey = $kwval),*),
        )
    };
}
