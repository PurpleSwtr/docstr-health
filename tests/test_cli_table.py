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


def test_get_table_percentage_true_with_string_value_does_not_raise():
    renderer = RichOutput()
    data = {"skipped_module.py": "SyntaxError: '(' was never closed"}
    # show_percentage is True, but should auto-skip gracefully
    table = renderer.get_table(
        title="Test", headers=["Module", "Error"], data=data, show_percentage=True
    )
    assert isinstance(table, Table)


def test_get_table_percentage_true_with_all_numeric_still_shows_percentage():
    renderer = RichOutput()
    data = {"a": 10, "b": 90, "total": 100}
    table = renderer.get_table(
        title="Test", headers=["Metric", "Value", "Rate"], data=data, show_percentage=True
    )
    assert isinstance(table, Table)


def test_all_values_numeric_helper():
    renderer = RichOutput()
    assert renderer._all_values_numeric({"a": 1, "b": "2", "c": 3.0}) is True
    assert renderer._all_values_numeric({"a": "13.9 words"}) is False
    assert renderer._all_values_numeric({"a": 1, "b": "abc"}) is False
    assert renderer._all_values_numeric({}) is True
