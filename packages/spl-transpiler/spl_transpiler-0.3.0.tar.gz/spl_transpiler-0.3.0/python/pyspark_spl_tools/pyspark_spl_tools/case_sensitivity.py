import functools
# import logging

import pyspark
from packaging.version import Version
from pyspark.sql.types import DataType, StringType, StructType, ArrayType, StructField


# log = logging.getLogger(__name__)


# def make_dataframe_case_insensitive(df: DataFrame, safe: bool = True, force_lowercase: bool = False) -> DataFrame:
#     """Converts a dataframe to make all strings behave case-insensitively.
#
#     If Pyspark supports collation, then strings are collated to use lowercase comparisons without loss of data.
#
#     Otherwise, strings are explicitly lowercased, which results in loss of data but guarantees case-insensitive behavior.
#
#     Lowercasing can be disabled by setting `safe=False`, or forced by setting `force_lowercase=True`.
#
#     Note that strings with different collations cannot be compared, so make sure to collate all dataframes you wish to work with.
#
#     Args:
#         df: The input dataframe to transform.
#         safe: If true, lowercasing is always disabled. If no other option is available, a runtime error is raised.
#         force_lowercase: If true, lowercasing is always used even if collation is available. If safe=true, a runtime error is raised.
#
#     Returns:
#         The original dataframe with all strings (including those nested in structs and arrays[?]) made case-insensitive
#     """
#
#     def collate_string(column_name: str, column_expr):
#         pyspark_supports_collation = Version(pyspark.__version__) > Version("3")
#         match (pyspark_supports_collation, safe, force_lowercase):
#             case (_, True, True):
#                 raise RuntimeError("Cannot force lowercase safely, either set safe=False, or force_lowercase=False")
#             case (False, True, _):
#                 raise RuntimeError("There is no safe way to enable case-insensitive strings in Spark <4, please upgrade to Pyspark 4.x or set `safe=False` to accept the necessary data loss")
#             case (_, _, True):
#                 method = "lowercase"
#             case (True, _, _):
#                 method = "collate"
#             case _:
#                 raise NotImplementedError(f"Unhandled collation behavior: {pyspark_supports_collation=}, {safe=}, {force_lowercase=}")
#
#         log.info(f"Detected string column at {column_name=}, handling with {method=}")
#
#         match method:
#             case "lowercase":
#                 return F.lower(column_expr).alias(column_name)
#             case "collate":
#                 return F.collate(column_expr, "UTF8_LCASE").alias(column_name)
#             case _:
#                 raise NotImplementedError(f"Unhandled insensitivity method: {method}")
#
#     def collate_struct(column_name: str, dtype):
#         log.info(f"Detected struct column at {column_name=}, handling recursively")
#         final_fields = {}
#         for field in dtype.fields:
#             final_fields[field.name] = collate_recursive(f"`{column_name}`.`{field.name}`", F.col(f"`{column_name}`.`{field.name}`"), field.dataType)
#         return F.named_struct(
#             *(
#                 arg
#                 for field_name, field_expr in final_fields.items()
#                 for arg in [F.lit(field_name), field_expr]
#             )
#         ).alias(column_name)
#
#     # TODO: Support array<_> types
#
#     def collate_recursive(column_name: str, column_expr, dtype: DataType):
#         log.info(f"Working on redefining {column_name=}, dtype={dtype=}")
#         match dtype:
#             case StringType():
#                 return collate_string(column_name, column_expr)
#             case StructType():
#                 return collate_struct(column_name, dtype)
#             case _:
#                 log.info(f"Unknown column type: {dtype=}, returning as-is")
#                 return column_expr
#
#     fields = [
#         collate_recursive(field.name, F.col(f"`{field.name}`"), field.dataType)
#               for field in df.schema
#     ]
#     return df.select(*fields)
#
#
# DataFrame.makeCaseInsensitive = make_dataframe_case_insensitive


@functools.singledispatch
def _make_type_case_insensitive(tp: DataType) -> DataType:
    return tp


@_make_type_case_insensitive.register
def _(_: StringType) -> StringType:
    return StringType(collation="UTF8_LCASE")


@_make_type_case_insensitive.register
def _(tp: StructType) -> StructType:
    return StructType(
        [
            StructField(
                field.name,
                _make_type_case_insensitive(field.dataType),
                nullable=field.nullable,
                metadata=field.metadata,
            )
            for field in tp.fields
        ]
    )


@_make_type_case_insensitive.register
def _(tp: ArrayType) -> ArrayType:
    return ArrayType(_make_type_case_insensitive(tp.elementType), containsNull=False)


def make_schema_case_insensitive(schema: StructType) -> StructType:
    assert Version(pyspark.__version__) > Version("3"), (
        "Schema can only support case-insensitive collation in Spark >=4.x"
    )

    return _make_type_case_insensitive(schema)  # noqa:
