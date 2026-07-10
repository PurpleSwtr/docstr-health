# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2026-07-10

### Bug Fixes

- Fix `FileNotFoundError` on first run by ensuring `~/.cache/docstr-health/logs/` exists before logger initialization

## [0.1.0] - 2026-07-09

### Features

- Core docstring parsing engine with quality grading (bad → good → special → epic)
- CLI with argparse supporting local, Git, and PyPI targets
- Rich terminal UI with color-coded output, panels, and tables
- Remote Git repository scanning with caching
- PyPI package scanning (via pip or uv)
- Progress bar display during scanning
- Configuration via `config.toml` (symbols, colors, keyword levels)
- Multiple docstring requirement levels
- Module-level statistics with per-status breakdown
- Async function detection and support
- PEP 257 section awareness (Args, Returns, Raises, etc.)
- Custom exception classes
- Cache and no-cache modes for remote sources
- Skipped modules tracking with error display

### Flags

- `--repo-url` — scan remote Git repositories
- `--pypi-package` — scan PyPI packages
- `--cache-dir` — custom cache directory
- `--no-cache` — disable caching
- `--compact` — summary-only output
- `--doc-modules` — include module `__doc__`
- `--ignore-tests` — skip test files
- `--version` — show version

### Infrastructure

- Project scaffolding with `pyproject.toml` (uv-based build)
- Type checking with mypy, linting with ruff
