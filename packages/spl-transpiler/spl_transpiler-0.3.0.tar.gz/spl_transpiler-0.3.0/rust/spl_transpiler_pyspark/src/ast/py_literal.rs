use crate::{PysparkTranspileContext, PythonCode, ToSparkQuery};

#[derive(Debug, PartialEq, Clone, Hash)]
// #[pyclass(frozen,eq,hash)]
pub struct PyLiteral(pub String);

impl<T: Into<PyLiteral>> From<Option<T>> for PyLiteral {
    fn from(value: Option<T>) -> PyLiteral {
        match value {
            Some(v) => v.into(),
            None => PyLiteral("None".into()),
        }
    }
}

impl ToSparkQuery for PyLiteral {
    fn to_spark_query(&self, _ctx: &PysparkTranspileContext) -> anyhow::Result<PythonCode> {
        Ok(self.0.to_string().into())
    }
}

macro_rules! py_literal_impl {
    ($t: ty) => {
        py_literal_impl!($t, value, value.to_string());
    };
    ($t: ty, $name: ident, $exp: expr) => {
        impl From<$t> for PyLiteral {
            fn from($name: $t) -> PyLiteral {
                PyLiteral($exp)
            }
        }
    };
}

fn format_str<S: AsRef<str>>(s: S) -> String {
    let s = s.as_ref();
    let contains_backslash = s.contains("\\");
    format!("{}\"{}\"", if contains_backslash { "r" } else { "" }, s)
}

py_literal_impl!(String, value, format_str(value));
py_literal_impl!(&str, value, format_str(value));

py_literal_impl!(i8);
py_literal_impl!(u8);

py_literal_impl!(i16);
py_literal_impl!(u16);

py_literal_impl!(i32);
py_literal_impl!(u32);
py_literal_impl!(f32);

py_literal_impl!(i64);
py_literal_impl!(u64);
py_literal_impl!(f64);

py_literal_impl!(i128);
py_literal_impl!(u128);

py_literal_impl!(isize);
py_literal_impl!(usize);

py_literal_impl!(
    bool,
    value,
    if value { "True".into() } else { "False".into() }
);
