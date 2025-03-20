import textwrap

from ruff_api import format_string


def format_python_code(code):
    return format_string(
        "sample.py",
        textwrap.dedent(code),
    ).strip()


def assert_python_code_equals(actual, expected):
    actual = format_python_code(actual)
    expected = format_python_code(expected)
    assert actual == expected
