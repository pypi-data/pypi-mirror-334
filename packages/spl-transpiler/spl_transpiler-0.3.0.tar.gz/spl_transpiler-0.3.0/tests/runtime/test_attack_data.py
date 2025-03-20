import json
import logging
import re
import traceback
import warnings
from datetime import datetime
from pathlib import Path
from typing import Annotated, Dict

import pandas as pd
import pytest
import yaml
from pydantic import BaseModel, AfterValidator, validate_call
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType

from spl_transpiler import convert_spl_to_pyspark
from spl_transpiler.macros import substitute_macros
from pyspark_spl_tools.case_sensitivity import make_schema_case_insensitive
from .utils import execute_transpiled_pyspark_code

log = logging.getLogger(__name__)

ATTACK_DATA_ROOT = Path(__file__).parent.parent / "sample_data" / "attack_data"
DATA_DIR = ATTACK_DATA_ROOT / ".data"
INPUTS_DIR = DATA_DIR / "inputs"
OUTPUTS_DIR = DATA_DIR / "outputs"
QUERY_DIR = ATTACK_DATA_ROOT.parent / "queries"


class TestDefinition(BaseModel):
    name: str
    ignore: bool
    input_file: (
        Annotated[Path, AfterValidator(lambda p: INPUTS_DIR / "custom" / p)] | None
    ) = None
    output_file: Annotated[Path, AfterValidator(lambda p: OUTPUTS_DIR / p)]
    query_file: Annotated[Path, AfterValidator(lambda p: QUERY_DIR / p)]


class TestSuite(BaseModel):
    # prefix: Annotated[CloudPath, BeforeValidator(cloudpathlib_client.CloudPath)]
    tests: list[TestDefinition]

    @property
    def test_map(self):
        return {test.name: test for test in self.tests}


test_suite_defn = TestSuite.model_validate(
    yaml.safe_load(open(ATTACK_DATA_ROOT / "tests.inputs.yaml"))
)


@validate_call(config=dict(arbitrary_types_allowed=True))
def _load_data(spark: SparkSession, path: Path) -> DataFrame:
    assert ".parquet" in path.name, "Let's please just use parquet files for everything"

    schema_path = path.with_suffix(f"{path.suffix}.schema.json")
    if schema_path.exists():
        schema = StructType.fromJson(json.load(open(schema_path)))
    else:
        warnings.warn(f"No pre-built schema found for {path}, generating one now...")
        orig_schema = spark.read.parquet(str(path)).schema
        schema = make_schema_case_insensitive(orig_schema)
        json.dump(schema.jsonValue(), open(schema_path, "w"), indent=2)

    df = spark.read.schema(schema).parquet(str(path))
    return df


@pytest.fixture(scope="session", autouse=True)
def data_models(spark):
    for path in INPUTS_DIR.glob("datamodel/*.parquet"):
        *dm_name, _ = path.name.split(".")
        dm_name = ".".join(dm_name)
        log.info(f"Loading data model from [red]{path.name=} as {dm_name=}")
        df = _load_data(spark, path)
        df.createOrReplaceTempView(f"`{dm_name}`")


@pytest.fixture(scope="session", autouse=True)
def lookups(spark):
    for path in INPUTS_DIR.glob("lookup/*.parquet"):
        dm_name = re.match(r"^([\d\w_]+?)(?:_?\d{8})?\.parquet$", path.name)
        assert dm_name is not None, path.name
        dm_name = dm_name.group(1)
        log.info(f"Loading lookup table from [red]{path.name=} as {dm_name=}")
        df = _load_data(spark, path)
        df.createOrReplaceTempView(f"`{dm_name}`")


def _normalize_df(spark_df: DataFrame):
    df = spark_df.toPandas()

    df = df[list(sorted(df.columns))]
    if "count" in df.columns:
        df["count"] = pd.to_numeric(df["count"], errors="coerce")
    df = df.sort_values(
        by=[
            c
            for c, dtype in sorted(spark_df.dtypes, key=lambda p: p[0])
            if not dtype.startswith("array<")
        ]
    )

    for col, dtype in spark_df.dtypes:
        if dtype.startswith("array<"):
            df[col] = df[col].apply(lambda x: sorted(x) if isinstance(x, list) else x)

    df = df.reset_index(drop=True)

    # Truncate fields to 2027 characters due to Splunk limit of 2027 characters
    # in fields for tsidx (e.g. used by tstats). No settings known to change this.
    # df = df.applymap(lambda x: x[:2027] if isinstance(x, str) else x)
    if "process" in df.columns:
        df["process"] = df["process"].apply(
            lambda x: x[:2027] if isinstance(x, str) else x
        )
    return df


def _normalize_df_pair(actual, expected):
    expected = expected.replace("null", None)

    for col, dtype in actual.dtypes.items():
        assert col in expected, (
            f"Column {col} found in actual output but missing from expected output"
        )
        try:
            expected[col] = expected[col].astype(dtype)
        except Exception as e:
            raise TypeError(
                f"Column {col} found in both actual and expected outputs, but values in expected output could not be type cast to match actual dtype {dtype}"
            ) from e

    return actual, expected


def _assert_df_equals(actual: DataFrame, expected: DataFrame):
    from pandas.testing import assert_frame_equal

    expected = _normalize_df(expected)
    actual = _normalize_df(actual)

    actual, expected = _normalize_df_pair(actual, expected)

    try:
        assert_frame_equal(actual, expected, check_dtype=False)
    except:
        with pd.option_context("display.max_rows", None, "display.max_columns", None):
            log.error(f"=== Actual ===\n{actual}")
            log.error(f"=== Expected ===\n{expected}")
        raise


@pytest.fixture(scope="session")
def test_results():
    results_path = ATTACK_DATA_ROOT / "tests.outputs.yaml"
    if results_path.exists():
        with open(results_path, "r") as f:
            results = yaml.unsafe_load(f) or {}
    else:
        results = {}

    try:
        yield results
    finally:
        yaml_text = yaml.safe_dump(results, sort_keys=False)
        results_path.write_text(yaml_text)


def sanitize_view_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)


@pytest.fixture(scope="session")
def input_data_views(spark: SparkSession) -> Dict[Path, str]:
    input_files = {test.input_file for test in test_suite_defn.tests if test.input_file}
    data_views = {}

    log.info(f"Input Files: {input_files}")

    for input_file in input_files:
        raw_view_name = f"input_{input_file.name.replace('.', '_')}"
        temp_view_name = sanitize_view_name(raw_view_name)
        log.info(f"Loading and caching input data: {input_file} as {temp_view_name}")
        df = _load_data(spark, input_file)
        df.cache().createOrReplaceTempView(temp_view_name)
        data_views[input_file] = temp_view_name

    log.info(f"Data Views: {data_views}")
    yield data_views

    for temp_view_name in data_views.values():
        log.info(f"Dropping temp view: {temp_view_name}")
        spark.catalog.dropTempView(temp_view_name)


# For each sample file, test that the transpiled query, when run against the input data, produces the output data
@pytest.mark.parametrize(
    "test_defn",
    list(sorted(test_suite_defn.tests, key=lambda x: (not x.ignore, x.name))),
    ids=lambda x: x.name,
)
# @pytest.mark.parametrize("allow_runtime", [True, False], ids=lambda x: "runtime" if x else "standalone")
@pytest.mark.parametrize(
    "allow_runtime", [False], ids=lambda x: "runtime" if x else "standalone"
)
def test_transpiled_query(
    spark,
    macros,
    test_defn: TestDefinition,
    allow_runtime: bool,
    test_results,
    input_data_views: Dict[Path, str],
) -> None:
    test_results[test_defn.name] = result = dict(
        name=test_defn.name,
        ignore=test_defn.ignore,
        empty=None,
        spl_query=None,
        base_command=None,
        transpiled_query=None,
        success=False,
        error_message=None,
        duration=None,
    )
    start_time = datetime.now()

    if test_defn.ignore:
        pytest.skip(f"Skipping test for ignored test {test_defn.name=}")

    try:
        # attack_data = AttackDefinition.load_from_yaml(attack_data_path)
        # If the size of the output_file is 0, skip this test
        output_path = test_defn.output_file
        if not output_path.exists():
            result["empty"] = True
            pytest.skip(f"Skipping test for empty/missing output_file {output_path=}")
        result["empty"] = False

        query = substitute_macros(test_defn.query_file.read_text(), macros)
        result["spl_query"] = query

        _query = query.strip()
        if _query.startswith("|"):
            _query = _query[1:].strip()
            result["base_command"] = _query.split()[0]
        else:
            result["base_command"] = "search"

        log.info(f"Query:\n[green]{query}")
        transpiled_code = convert_spl_to_pyspark(query, allow_runtime=allow_runtime)
        result["transpiled_query"] = transpiled_code

        if test_defn.input_file:
            temp_view_name = input_data_views[test_defn.input_file]
            transpiled_code = transpiled_code.replace("main", temp_view_name)

        try:
            expected_results = _load_data(spark, test_defn.output_file)
        except Exception as e:
            result["error_message"] = (
                f"Failed to load expected output data from {test_defn.output_file}: {e}"
            )
            pytest.skip(
                f"Failed to load expected output data from {test_defn.output_file}"
            )

        query_results = execute_transpiled_pyspark_code(transpiled_code)
        _assert_df_equals(query_results, expected_results)
        result["success"] = True
    except Exception:
        result["error_message"] = traceback.format_exc()
        raise
    finally:
        result["duration"] = (datetime.now() - start_time).total_seconds()
