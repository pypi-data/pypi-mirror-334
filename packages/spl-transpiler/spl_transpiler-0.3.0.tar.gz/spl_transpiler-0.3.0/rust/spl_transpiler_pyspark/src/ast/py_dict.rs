use crate::ast::RuntimeExpr;
use crate::{PysparkTranspileContext, PythonCode, ToSparkQuery};

#[derive(Debug, PartialEq, Clone, Hash)]
pub struct PyDict(pub Vec<(String, RuntimeExpr)>);

impl PyDict {
    pub fn push(&mut self, key: impl ToString, value: impl Into<RuntimeExpr>) {
        self.0.push((key.to_string(), value.into()));
    }
}

impl ToSparkQuery for PyDict {
    fn to_spark_query(&self, ctx: &PysparkTranspileContext) -> anyhow::Result<PythonCode> {
        let mut out_preface = vec![];
        let mut out_vals = vec![];

        for (key, value) in self.0.iter() {
            let PythonCode {
                preface,
                primary_df_code,
            } = value.to_spark_query(ctx)?;
            out_preface.extend(preface);
            out_vals.push(format!("\"{}\": {}", key, primary_df_code).to_string());
        }
        Ok(format!(r#"{{ {} }}"#, out_vals.join(", ")).into())
    }
}

impl Extend<(String, RuntimeExpr)> for PyDict {
    fn extend<T: IntoIterator<Item = (String, RuntimeExpr)>>(&mut self, iter: T) {
        self.0.extend(iter)
    }
}

impl IntoIterator for PyDict {
    type Item = (String, RuntimeExpr);
    type IntoIter = <Vec<(String, RuntimeExpr)> as IntoIterator>::IntoIter;

    fn into_iter(self) -> Self::IntoIter {
        self.0.into_iter()
    }
}

macro_rules! py_dict {
    () => { crate::ast::PyDict(vec![]) };
    ($($key: ident = $value: expr),+ $(,)?) => {
        crate::ast::PyDict(vec![$((stringify!($key).into(), $value.into())),+])
    };
}

pub(crate) use py_dict;
