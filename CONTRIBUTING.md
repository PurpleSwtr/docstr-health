# Contributing to Docstr-Health

Thank you for considering contributing! This document provides guidelines to help you get started.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
  - [Commit style](#commit-style)
- [Reporting Issues](#reporting-issues)
- [License](#license)

## Getting Started

### Prerequisites

- Python 3.11+ (CPython)
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### Development Setup

```shell
git clone https://github.com/PurpleSwtr/docstr-health.git
cd docstr-health

uv venv
uv sync --group dev
```

## Project Structure

```
docstr_health/
├── __init__.py          # Package entry point (exports __version__)
├── main.py              # CLI entry point
├── config.toml          # User-facing configuration (symbols, colors, keywords)
├── cli/                 # CLI layer (argparse, Rich output)
│   ├── cli.py           # RichOutput — terminal rendering
│   ├── parser.py        # Argument parser
│   └── progress_bar.py  # Progress display
├── checkers/            # Core logic
│   ├── base.py          # BaseChecker abstract class
│   ├── docstring.py     # DocstringChecker — quality grading logic
│   ├── project.py       # ProjectChecker — orchestrates per-module checks
│   └── typecheck.py     # Type annotation checker
├── core/                # Shared infrastructure
│   ├── config.py        # Configuration singleton (caching, version)
│   ├── enums.py         # StatusDocstring, ModuleStatus, StatusTypechecking
│   ├── exceptions.py    # Custom exceptions
│   ├── interfaces.py    # Abstract interfaces
│   ├── logger.py        # Logging setup
│   └── settings.py      # AppSettings from CLI args
├── models/              # Data models
│   ├── module.py        # PythonModule
│   ├── function.py      # PythonFunction
│   ├── class.py         # PythonClass
│   └── report.py        # ModuleReport
└── sources/             # Source providers
    ├── base.py          # BaseSource abstract class
    ├── local.py         # Local directory scanner
    ├── git_repo.py      # Remote Git repository scanner
    └── pypi_package.py  # PyPI package scanner
```

## Code Style

- **Type annotations** are required for all public functions and methods

Before submitting, ensure your code:

```shell
uv run ruff check .

uv run mypy docstr_health
```

## Pull Request Process

1. **Fork** the repository and create a branch from `main`
2. **Commit** your changes with clear, descriptive messages
3. **Ensure** all tests pass and coverage doesn't decrease
4. **Open** a pull request and fill out the template
5. **Respond** to review feedback — we may ask for changes

### Commit style

Use conventional commits when possible:

```
feat: add --fail-under flag for CI integration
fix: handle empty modules gracefully
docs: update README with new examples
refactor: extract status classification to separate method
```

## Reporting Issues

- **Bug reports**: include the full command you ran, the output, and the environment (Python version, OS)
- **Feature requests**: describe the use case and how it would benefit the project
- **Questions**: feel free to open a discussion

---

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).

---

**Thank you for contributing to docstr-health!**
