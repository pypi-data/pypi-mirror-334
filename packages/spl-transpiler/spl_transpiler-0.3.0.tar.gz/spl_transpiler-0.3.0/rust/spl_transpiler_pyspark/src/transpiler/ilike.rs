use spl_transpiler_spl::ast::{StrValue, Wildcard};

pub trait AsLikeString {
    fn as_like_string(&self) -> String;
}

impl AsLikeString for StrValue {
    fn as_like_string(&self) -> String {
        self.0.replace("\\", "\\\\").replace("%", "\\%")
    }
}

impl AsLikeString for Wildcard {
    fn as_like_string(&self) -> String {
        self.0.replace("%", "\\%").replace("*", "%")
    }
}
