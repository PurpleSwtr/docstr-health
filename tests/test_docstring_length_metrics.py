from docstr_health.models.report import ModuleReport
from docstr_health.checkers.project import ProjectChecker


def test_module_report_empty_average():
    report = ModuleReport(module_status="good", inspected_functions=[])
    assert report.average_docstring_length == 0.0


def test_module_report_empty_median():
    report = ModuleReport(module_status="good", inspected_functions=[])
    assert report.median_docstring_length == 0.0


def test_module_report_empty_longest():
    report = ModuleReport(module_status="good", inspected_functions=[])
    assert report.longest_docstring is None


def test_module_report_populated_average():
    report = ModuleReport(
        module_status="good",
        inspected_functions=[],
        docstring_lengths=[("a", 10), ("b", 20), ("c", 30), ("d", 40)],
    )
    assert report.average_docstring_length == 25.0


def test_module_report_populated_median():
    report = ModuleReport(
        module_status="good",
        inspected_functions=[],
        docstring_lengths=[("a", 10), ("b", 20), ("c", 30), ("d", 40)],
    )
    assert report.median_docstring_length == 25.0


def test_module_report_populated_longest():
    report = ModuleReport(
        module_status="good",
        inspected_functions=[],
        docstring_lengths=[("a", 10), ("b", 20), ("c", 30), ("d", 40)],
    )
    assert report.longest_docstring == ("d", 40)


def test_module_report_odd_length_median():
    report = ModuleReport(
        module_status="good",
        inspected_functions=[],
        docstring_lengths=[("a", 10), ("b", 20), ("c", 30)],
    )
    assert report.median_docstring_length == 20.0


def test_project_checker_zero_reports_average():
    checker = ProjectChecker.__new__(ProjectChecker)
    checker._reports = []
    assert checker.get_avg_docstring_length() == 0.0


def test_project_checker_zero_reports_median():
    checker = ProjectChecker.__new__(ProjectChecker)
    checker._reports = []
    assert checker.get_median_docstring_length() == 0.0


def test_project_checker_zero_reports_longest():
    checker = ProjectChecker.__new__(ProjectChecker)
    checker._reports = []
    assert checker.get_longest_docstring() is None


def test_project_checker_aggregate_average():
    report1 = ModuleReport(
        module_status="good",
        inspected_functions=[],
        docstring_lengths=[("a", 10), ("b", 20)],
    )
    report2 = ModuleReport(
        module_status="good", inspected_functions=[], docstring_lengths=[("c", 30)]
    )
    checker = ProjectChecker.__new__(ProjectChecker)
    checker._reports = [report1, report2]
    assert checker.get_avg_docstring_length() == 20.0


def test_project_checker_aggregate_median():
    report1 = ModuleReport(
        module_status="good",
        inspected_functions=[],
        docstring_lengths=[("a", 10), ("b", 20)],
    )
    report2 = ModuleReport(
        module_status="good", inspected_functions=[], docstring_lengths=[("c", 30)]
    )
    checker = ProjectChecker.__new__(ProjectChecker)
    checker._reports = [report1, report2]
    assert checker.get_median_docstring_length() == 20.0


def test_project_checker_aggregate_longest():
    report1 = ModuleReport(
        module_status="good",
        inspected_functions=[],
        docstring_lengths=[("a", 10), ("b", 20)],
    )
    report2 = ModuleReport(
        module_status="good", inspected_functions=[], docstring_lengths=[("c", 30)]
    )
    checker = ProjectChecker.__new__(ProjectChecker)
    checker._reports = [report1, report2]
    assert checker.get_longest_docstring() == ("c", 30)
