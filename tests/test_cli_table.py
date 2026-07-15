import pytest
from rich.table import Table

from docstr_health.cli.cli import RichOutput


def test_get_table_with_percentage_default():
    renderer = RichOutput()
    data = {"bad": 5, "good": 5}
    table = renderer.get_table(
        title="Test", headers=["Status", "Count", "Rate"], data=data
    )
    assert isinstance(table, Table)


def test_get_table_show_percentage_false_with_string_values():
    renderer = RichOutput()
    data = {
        "avg docstring length": "13.9 words",
        "longest docstring": "foo (5 words)",
    }
    table = renderer.get_table(
        title="Test",
        headers=["Metric", "Value"],
        data=data,
        show_percentage=False,
    )
    assert isinstance(table, Table)


def test_get_table_show_percentage_false_skips_percentage_column():
    renderer = RichOutput()
    data = {"skipped_module.py": "SyntaxError: '(' was never closed"}
    table = renderer.get_table(
        title="Skipped",
        headers=["Module", "Error"],
        data=data,
        show_percentage=False,
    )
    assert isinstance(table, Table)


def test_get_table_percentage_true_with_string_value_raises_typeerror():
    renderer = RichOutput()
    data = {"skipped_module.py": "SyntaxError: '(' was never closed"}
    with pytest.raises(TypeError):
        renderer.get_table(
            title="Test", headers=["Module", "Error", "Rate"], data=data
        )


def test_get_table_percentage_true_with_string_value_raises_valueerror():
    renderer = RichOutput()
    data = {"avg docstring length": "13.9 words", "total": 100}
    with pytest.raises(ValueError, match="invalid literal for int"):
        renderer.get_table(
            title="Test", headers=["Metric", "Value", "Rate"], data=data
        )
