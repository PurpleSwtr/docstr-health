from conftest import run_cli


def test_cli_version(cli_args):
    result = run_cli(cli_args, "--version")
    assert result.returncode == 0
    assert "docstr-health" in result.stdout


def test_cli_version_stderr_empty(cli_args):
    result = run_cli(cli_args, "--version")
    assert result.stderr == "" or result.stderr is None
