import re
from functools import cache

from pyspark.sql import DataFrame, functions as F, GroupedData


def groupByMaybeExploded(self: DataFrame, by: list) -> GroupedData:
    by_strings = [c for c in by if isinstance(c, str)]
    return self.withColumns(
        {
            c: F.explode(c)
            for c, tp in self.dtypes
            if c in by_strings and str(tp).lower().startswith("array<")
        }
    ).groupBy(by)


def _expand_wildcard(df: DataFrame, name: str):
    if not isinstance(name, str):
        return [name]

    if "*" not in name:
        return [name]

    # TODO: Rework to support any number of wildcards
    if name.count("*") != 1:
        raise ValueError(
            "If using wildcard in rename, must have exactly one `*` on each side"
        )

    left, _, right = name.partition("*")

    from_regex = re.compile(f"{re.escape(left)}(?P<slot>.*?){re.escape(right)}")

    return [col for col in df.columns if from_regex.fullmatch(col)]


def _expand_wildcard_paired(df: DataFrame, from_name: str, to_name: str):
    if "*" not in from_name:
        return [(from_name, to_name)]

    # TODO: Rework to support any number of wildcards
    if from_name.count("*") != 1 or to_name.count("*") != 1:
        raise ValueError(
            "If using wildcard in rename, must have exactly one `*` on each side"
        )

    from_left, _, from_right = from_name.partition("*")
    to_left, _, to_right = to_name.partition("*")

    # TODO: Fix this logic to support name paths correctly, including backtick handling
    # Right now, this handles "`Processes`.*" -> "Processes.*"
    from_left = from_left.replace("`", "")
    from_right = from_right.replace("`", "")

    from_regex = re.compile(
        f"{re.escape(from_left)}(?P<slot>.*?){re.escape(from_right)}"
    )
    to_regex = f"{to_left}\\g<slot>{to_right}"

    return [
        (col, from_regex.sub(to_regex, col))
        for col in df.columns
        if from_regex.fullmatch(col)
    ]


def withColumnsRenamedWithWildcards(
    self: DataFrame, renames: dict[str, str]
) -> DataFrame:
    expanded_renames = {
        k: v
        for k_orig, v_orig in renames.items()
        for k, v in _expand_wildcard_paired(self, k_orig, v_orig)
    }

    drop_columns = [c for c in expanded_renames.values() if c in self.columns]
    if drop_columns:
        self = self.drop(*drop_columns)

    return self.withColumnsRenamed(expanded_renames)


def selectWithWildcards(self: DataFrame, *columns) -> DataFrame:
    return self.select(*(c for raw_c in columns for c in _expand_wildcard(self, raw_c)))


def withColumnMaybe(self: DataFrame, name, value, *required_columns) -> DataFrame:
    if all(c in self.columns for c in required_columns):
        return self.withColumn(name, value)
    else:
        return self


@cache
def install_monkeypatches():
    DataFrame._spltranspiler__groupByMaybeExploded = groupByMaybeExploded
    DataFrame._spltranspiler__withColumnsRenamedWithWildcards = (
        withColumnsRenamedWithWildcards
    )
    DataFrame._spltranspiler__withColumnMaybe = withColumnMaybe
    DataFrame._spltranspiler__selectWithWildcards = selectWithWildcards
