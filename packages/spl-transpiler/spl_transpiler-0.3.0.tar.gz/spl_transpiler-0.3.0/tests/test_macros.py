from spl_transpiler import render_pyspark
from spl_transpiler.macros import substitute_macros, parse_with_macros
from utils import format_python_code


def test_macro_substitution():
    macros = {
        "f": dict(definition="index=main"),
        "g": dict(arguments=["f"], definition="ctime($f$)"),
    }

    assert substitute_macros("`f`", macros) == "index=main"
    assert substitute_macros("`f` | eval x=y", macros) == "index=main | eval x=y"
    assert (
        substitute_macros("`f` | eval x=`g(y)`", macros)
        == "index=main | eval x=ctime(y)"
    )
    assert (
        substitute_macros("`f` | eval x=`g(f=y)`", macros)
        == "index=main | eval x=ctime(y)"
    )

    spl = "`f`"
    pyspark = r"table_source(spark, index='main')"

    actual = render_pyspark(parse_with_macros(spl, macros))
    expected = format_python_code(pyspark)
    assert actual == expected
