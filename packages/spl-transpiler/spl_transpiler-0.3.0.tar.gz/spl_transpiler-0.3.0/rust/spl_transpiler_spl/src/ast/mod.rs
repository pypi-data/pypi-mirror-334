mod alias;
mod aliased_field;
mod binary;
mod bool_value;
mod call;
mod command;
mod command_options;
mod constant;
mod double_value;
mod expr;
mod fb;
mod fc;
mod field;
mod field_in;
mod field_like;
mod field_or_alias;
mod fv;
mod int_value;
mod ipv4_cidr;
mod leaf_expr;
mod null_value;
mod pipeline;
mod search_modifier;
mod snap_time;
mod str_value;
mod time_modifier;
mod time_span;
mod unary;
mod variable;
mod wildcard;

pub use alias::*;
pub use aliased_field::*;
pub use binary::*;
pub use bool_value::*;
pub use call::*;
pub use command::*;
pub use command_options::*;
pub use constant::*;
pub use double_value::*;
pub use expr::*;
pub use fb::*;
pub use fc::*;
pub use field::*;
pub use field_in::*;
pub use field_like::*;
pub use field_or_alias::*;
pub use fv::*;
pub use int_value::*;
pub use ipv4_cidr::*;
pub use leaf_expr::*;
pub use null_value::*;
pub use pipeline::*;
pub use search_modifier::*;
pub use snap_time::*;
pub use str_value::*;
pub use time_modifier::*;
pub use time_span::*;
pub use unary::*;
pub use variable::*;
pub use wildcard::*;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_boolean_to_expr() {
        let bool_value = BoolValue::from(true);
        let expr: Expr = bool_value.clone().into();
        assert_eq!(
            expr,
            Expr::Leaf(LeafExpr::Constant(Constant::Bool(bool_value)))
        );
    }
}
