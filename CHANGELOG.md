# Changelog

All notable changes to this project will be documented in this file.

## [0.1.4] - 2026-08-28

### Bug Fixes

- Fix silent output
- CI mode was enabled by default (`ci = true`), suppressing all terminal output
- CI mode now can be enabled explicitly with the `--ci` flag or via `ci = true` in config

## [0.1.3] - 2026-08-28

### Features

- Add percentage metrics to file and overall statistics tables
- Support configuration via `pyproject.toml` with `[tool.docstr-health]` section
- Add `--short-names` flag to display short module names instead of full paths
- Add configurable status thresholds
- Add CI mode for quiet output and non-zero exit code when project status falls below the configured level

### Bug Fixes

- Fix double counting of functions and classes
- Fix memory leak by clearing cached functions on tree release and sharing a single output instance
- Speed up large-codebase scanning (CPython now checked in ~20 seconds instead ~140 seconds) via AST caching and disabled type-comment parsing
- Reduce I/O by loading `pyproject.toml` config once
- Use `file://` URI format instead of raw paths in report titles

### Refactoring

- Introduce `DocstrHealthError` base class with dedicated exceptions and non-zero exit codes

## [0.1.2] - 2026-07-10

### Bug Fixes

- Fix the type hinting bug with support for versions 3.11-3.12

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
