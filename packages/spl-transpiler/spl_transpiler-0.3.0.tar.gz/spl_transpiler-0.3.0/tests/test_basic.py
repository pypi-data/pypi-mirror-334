import pytest

from spl_transpiler import parse, ast, render_pyspark, convert_spl_to_pyspark
from utils import assert_python_code_equals


def test_parse():
    assert parse("head count>10") == ast.Pipeline(
        commands=[
            ast.Command.HeadCommand(
                ast.HeadCommand(
                    eval_expr=ast.Expr.Binary(
                        ast.Binary(
                            left=ast.Expr.Leaf(
                                ast.LeafExpr.Constant(
                                    ast.Constant.Field(ast.Field("count"))
                                )
                            ),
                            symbol=">",
                            right=ast.Expr.Leaf(
                                ast.LeafExpr.Constant(
                                    ast.Constant.Int(ast.IntValue(10))
                                )
                            ),
                        )
                    ),
                    keep_last=ast.BoolValue(False),
                    null_option=ast.BoolValue(False),
                )
            )
        ]
    )


def test_convert_to_pyspark():
    spl_code = r"code IN(4*, 5*)"
    expected_pyspark_code = r"table_source(spark, index='main').where((F.col('code').ilike('4%') | F.col('code').ilike('5%')),)"

    converted_code = render_pyspark(parse(spl_code))
    direct_converted_code = convert_spl_to_pyspark(spl_code)

    assert_python_code_equals(converted_code, expected_pyspark_code)
    assert_python_code_equals(direct_converted_code, expected_pyspark_code)


def test_formatting():
    spl_code = "index=main"
    pyspark_code = r'table_source(spark, index="main")'

    parsed = parse(spl_code)

    with pytest.raises(TypeError):
        render_pyspark(parsed, doesnt_exist=False)

    with pytest.raises(TypeError):
        render_pyspark(parsed, format_code=False)

    actual = render_pyspark(parsed)

    assert actual == pyspark_code
