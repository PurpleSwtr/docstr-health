import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def project_root() -> Path:
    return PROJECT_ROOT


@pytest.fixture
def cli_args(project_root: Path) -> list[str]:
    return [sys.executable, "-m", "docstr_health"]


def run_cli(
    cli_args: list[str], *extra_args: str, cwd: Path | None = None
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [*cli_args, *extra_args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
