pub fn escape_maybe_dotted(s: impl AsRef<str>) -> String {
    let s = s.as_ref().to_string();
    if s.contains(".") && !s.contains("`") {
        format!("`{s}`")
    } else {
        s
    }
}

#[cfg(test)]
pub mod test {
    use crate::ast::TransformedPipeline;
    use crate::base::test::test_pyspark_transpile_context;
    use crate::base::RuntimeSelection;
    use crate::utils::escape_maybe_dotted;
    use crate::ToSparkQuery;
    use anyhow::Result;
    use log::debug;
    use regex::Regex;
    use spl_transpiler_python_formatter::format_python_code;
    use std::ops::Deref;

    pub fn assert_python_code_eq(
        generated_code: impl ToString,
        reference_code: impl ToString,
        remove_newlines: bool,
    ) {
        let generated_code = generated_code.to_string();
        let generated_code = _cleanup(&generated_code, remove_newlines).unwrap_or_else(|_| {
            panic!("Failed to format rendered Spark query: {}", generated_code)
        });
        let reference_code = _cleanup(&reference_code, remove_newlines)
            .expect("Failed to format target Spark query");
        assert_eq!(generated_code, reference_code);
    }

    fn _remove_extraneous_newlines(code: impl ToString) -> Result<String> {
        let re: Regex = Regex::new(r#"[\n ]+"#)?;
        Ok(re
            .replace_all(code.to_string().as_str(), " ")
            .deref()
            .to_string())
    }

    fn _remove_trailing_commas(code: impl ToString) -> Result<String> {
        let re: Regex = Regex::new(r#",\s*([)\]])"#)?;
        Ok(re
            .replace_all(code.to_string().as_str(), "$1")
            .deref()
            .to_string())
    }

    fn _cleanup(code: &impl ToString, remove_newlines: bool) -> Result<String> {
        let mut code = format_python_code(code.to_string().replace(",)", ")"))?;
        if remove_newlines {
            code = _remove_extraneous_newlines(code)?;
        }
        code = _remove_trailing_commas(code)?;
        Ok(code)
    }

    pub fn generates(spl_query: &str, spark_query: &str) {
        let ctx = test_pyspark_transpile_context(RuntimeSelection::Disallow);
        let (_, pipeline_ast) =
            spl_transpiler_spl::parser::pipeline(spl_query).expect("Failed to parse SPL query");
        let rendered = TransformedPipeline::transform(pipeline_ast, ctx.clone())
            .expect("Failed to convert SPL query to Spark query")
            .to_spark_query(&ctx)
            .expect("Failed to render Spark query");

        assert_python_code_eq(rendered, spark_query, true);
    }

    pub fn generates_runtime(spl_query: &str, spark_query: &str) {
        let ctx = test_pyspark_transpile_context(RuntimeSelection::Require);
        let (_, pipeline_ast) =
            spl_transpiler_spl::parser::pipeline(spl_query).expect("Failed to parse SPL query");
        let rendered = TransformedPipeline::transform(pipeline_ast, ctx.clone())
            .expect("Failed to convert SPL query to Spark query")
            .to_spark_query(&ctx)
            .expect("Failed to render Spark query");

        assert_python_code_eq(rendered, spark_query, false);
    }

    pub fn generates_maybe_runtime(spl_query: &str, spark_query: &str) {
        let ctx = test_pyspark_transpile_context(RuntimeSelection::Allow);
        let (_, pipeline_ast) =
            spl_transpiler_spl::parser::pipeline(spl_query).expect("Failed to parse SPL query");
        let rendered = TransformedPipeline::transform(pipeline_ast, ctx.clone())
            .expect("Failed to convert SPL query to Spark query")
            .to_spark_query(&ctx)
            .expect("Failed to render Spark query");

        debug!("Generated code: {}", rendered.to_string());

        assert_python_code_eq(rendered, spark_query, false);
    }

    #[test]
    fn test_maybe_escape_dotted() {
        assert_eq!(escape_maybe_dotted("column"), "column");
        assert_eq!(
            escape_maybe_dotted("column.with.dots"),
            "`column.with.dots`"
        );
        assert_eq!(escape_maybe_dotted("`column`"), "`column`");
        assert_eq!(
            escape_maybe_dotted("`column`.`with.dots`"),
            "`column`.`with.dots`"
        );
    }
}
