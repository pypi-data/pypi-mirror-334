use anyhow::anyhow;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use spl_transpiler_spl::{ast, macros, parser};

use spl_transpiler_pyspark::{
    PysparkTranspileContext, RuntimeSelection, ToSparkQuery, TransformedPipeline,
};
use spl_transpiler_python_formatter::format_python_code;

fn _parse(spl_code: &str) -> anyhow::Result<ast::Pipeline> {
    match parser::pipeline(spl_code) {
        Ok(("", pipeline)) => Ok(pipeline),
        Ok(_) => Err(anyhow!("Failed to fully parse input")),
        Err(e) => Err(anyhow!("Error parsing SPL: {}", e)),
    }
}

fn _detect_macros(spl_code: &str) -> anyhow::Result<(Vec<(&str, macros::MacroCall)>, &str)> {
    match macros::spl_macros(spl_code) {
        Ok(("", res)) => Ok(res),
        Ok(_) => Err(anyhow!("Failed to fully parse input")),
        Err(e) => Err(anyhow!("Error parsing SPL: {}", e)),
    }
}

fn _render_pyspark(pipeline: &ast::Pipeline, allow_runtime: bool) -> anyhow::Result<String> {
    let ctx = PysparkTranspileContext::new(match allow_runtime {
        true => RuntimeSelection::Allow,
        false => RuntimeSelection::Disallow,
    });
    let transformed_pipeline: TransformedPipeline =
        TransformedPipeline::transform(pipeline.clone(), ctx.clone())?;
    let mut code = transformed_pipeline.to_spark_query(&ctx)?.to_string();
    code = format_python_code(code)?;
    Ok(code)
}

#[pymodule]
fn spl_transpiler(m: &Bound<'_, PyModule>) -> PyResult<()> {
    #[pyfn(m)]
    /// Parses SPL query code into a syntax tree.
    fn parse(spl_code: &str) -> PyResult<ast::Pipeline> {
        _parse(spl_code).map_err(|e| PyValueError::new_err(format!("{}", e)))
    }

    #[pyfn(m)]
    /// Parses SPL query code into a syntax tree.
    fn detect_macros(spl_code: &str) -> PyResult<(Vec<(&str, macros::MacroCall)>, &str)> {
        _detect_macros(spl_code).map_err(|e| PyValueError::new_err(format!("{}", e)))
    }

    #[pyfn(m)]
    #[pyo3(signature = (pipeline, *, allow_runtime=false))]
    /// Renders a parsed SPL syntax tree into equivalent PySpark query code, if possible.
    fn render_pyspark(pipeline: &ast::Pipeline, allow_runtime: bool) -> PyResult<String> {
        _render_pyspark(pipeline, allow_runtime)
            .map_err(|e| PyValueError::new_err(format!("{}", e)))
    }

    m.add_class::<macros::MacroCall>()?;

    let ast_m = PyModule::new(m.py(), "ast")?;
    spl_transpiler_spl::python::ast_pymodule(&ast_m)?;
    m.add_submodule(&ast_m)?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;

    Ok(())
}

#[cfg(test)]
mod test {
    use super::*;
    use rstest::rstest;

    #[rstest]
    fn test_parse() {
        let spl_code = "index=main";
        let pyspark_code = r#"table_source(spark, index="main")"#;

        let parsed = _parse(spl_code).expect("Failed to parse SPL query");
        let actual = _render_pyspark(&parsed, false).expect("Failed to render PySpark query");

        assert_eq!(actual, pyspark_code);
    }
}
