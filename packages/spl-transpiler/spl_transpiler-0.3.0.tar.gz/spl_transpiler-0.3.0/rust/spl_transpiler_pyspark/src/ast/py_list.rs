use crate::ast::RuntimeExpr;
use crate::{PysparkTranspileContext, PythonCode, ToSparkQuery};

#[derive(Debug, PartialEq, Clone, Hash)]
pub struct PyList(pub Vec<RuntimeExpr>);

impl ToSparkQuery for PyList {
    fn to_spark_query(&self, ctx: &PysparkTranspileContext) -> anyhow::Result<PythonCode> {
        let mut out_preface = vec![];
        let mut out_vals = vec![];

        for value in self.0.iter() {
            let PythonCode {
                preface,
                primary_df_code,
            } = value.to_spark_query(ctx)?;
            out_preface.extend(preface);
            out_vals.push(primary_df_code);
        }
        Ok(format!(r#"[ {} ]"#, out_vals.join(", ")).into())
    }
}

impl Extend<RuntimeExpr> for PyList {
    fn extend<T: IntoIterator<Item = RuntimeExpr>>(&mut self, iter: T) {
        self.0.extend(iter)
    }
}

impl IntoIterator for PyList {
    type Item = RuntimeExpr;
    type IntoIter = <Vec<RuntimeExpr> as IntoIterator>::IntoIter;

    fn into_iter(self) -> Self::IntoIter {
        self.0.into_iter()
    }
}

#[allow(unused_macros)]
macro_rules! py_list {
    () => { crate::ast::PyList(vec![]) };
    ($($value: expr),+ $(,)?) => {
        crate::ast::PyList(vec![$($value.into()),+])
    };
    (*$value: expr) => {
        crate::ast::PyList($value)
    };
}
