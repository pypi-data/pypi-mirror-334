use crate::base::{PysparkTranspileContext, PythonCode};
use std::fmt::Debug;
use std::hash::Hash;

use anyhow::{anyhow, Result};

pub trait CodeTransformer {
    fn update_code(&self, code: PythonCode, ctx: &PysparkTranspileContext) -> Result<PythonCode>;
}

pub trait SingletonCodeTransformer {
    const KEY: &'static str;
    type Transformer: CodeTransformer;
}

#[derive(Debug, PartialEq, Clone, Hash)]
pub enum CodeTransformerType {
    MonkeyPatch,
}

impl CodeTransformer for CodeTransformerType {
    fn update_code(&self, code: PythonCode, ctx: &PysparkTranspileContext) -> Result<PythonCode> {
        match self {
            CodeTransformerType::MonkeyPatch => {
                RequiresMonkeyPatch::update_code(&RequiresMonkeyPatch, code, ctx)
            }
        }
    }
}

impl<S: SingletonCodeTransformer<Transformer: Default>> CodeTransformer for S {
    fn update_code(
        &self,
        mut code: PythonCode,
        ctx: &PysparkTranspileContext,
    ) -> Result<PythonCode> {
        let already_applied;
        {
            let singleton_list = ctx
                .singletons
                .read()
                .map_err(|e| anyhow!("Failed to acquire read lock: {}", e))?;
            already_applied = singleton_list.contains(&Self::KEY.to_string());
        }

        if !already_applied {
            // TODO: If runtime is disabled, just copy-paste the monkeypatch code directly
            code = S::Transformer::default().update_code(code, ctx)?;

            let mut singleton_list = ctx
                .singletons
                .write()
                .map_err(|e| anyhow!("Failed to acquire read lock: {}", e))?;
            singleton_list.insert(Self::KEY.to_string());
        }

        Ok(code)
    }
}

#[derive(Debug, PartialEq, Clone, Hash, Default)]
pub struct ApplyMonkeyPatch;

impl CodeTransformer for ApplyMonkeyPatch {
    fn update_code(&self, code: PythonCode, _ctx: &PysparkTranspileContext) -> Result<PythonCode> {
        let PythonCode {
            mut preface,
            primary_df_code,
        } = code;
        preface.insert(0, "from pyspark_spl_tools.monkeypatches import install_monkeypatches\ninstall_monkeypatches()".to_string());
        Ok(PythonCode {
            primary_df_code,
            preface,
        })
    }
}

#[derive(Debug, PartialEq, Clone, Hash, Default)]
pub struct RequiresMonkeyPatch;

impl SingletonCodeTransformer for RequiresMonkeyPatch {
    const KEY: &'static str = "MONKEYPATCH";
    type Transformer = ApplyMonkeyPatch;
}
