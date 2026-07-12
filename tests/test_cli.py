from conftest import run_cli


def test_cli_version(cli_args):
    result = run_cli(cli_args, "--version")
    assert result.returncode == 0
    assert "docstr-health" in result.stdout
    assert result.stderr == "" or result.stderr is None


def test_cli_help(cli_args):
    result = run_cli(cli_args, "-h")
    assert result.returncode == 0


def test_cli_path(cli_args):
    result = run_cli(cli_args, ".")
    assert result.returncode == 0
    assert "General" in result.stdout
    allowed_words = ["good", "bad", "warning", "epic", "special"]
    assert any(word in result.stdout for word in allowed_words)


def test_cli_repo_url(cli_args):
    result = run_cli(
        cli_args,
        "--repo-url",
        "https://github.com/PurpleSwtr/docstr-health",
        "--cache-dir",
        ".pytest_cache/repos",
    )
    assert result.returncode == 0


def test_cli_pypi_package(cli_args):
    result = run_cli(cli_args, "--pypi-package", "docstr-health")
    assert result.returncode == 0
