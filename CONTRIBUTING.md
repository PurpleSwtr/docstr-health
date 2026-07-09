# Contributing to Docstr-Health

Thank you for considering contributing! This document provides guidelines to help you get started.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Branching Strategy](#branching-strategy)
- [Issue Management](#issue-management)
  - [Labels](#labels)
  - [Closing Issues](#closing-issues)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
  - [Commit Style](#commit-style)
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

---

## Branching Strategy

We follow a **Git Flow-inspired** branching model to keep `main` stable at all times.

| Branch      | Purpose                                                                                                                             |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `main`      | **Stable releases only.** Never commit directly here. Every merge into `main` corresponds to a tagged release.                      |
| `dev`       | **Integration branch.** All feature branches and bugfixes are merged here first. This is the default branch for active development. |
| `feature/*` | New features (e.g., `feature/json-export`, `feature/markdown-output`). Branched from `dev`.                                         |
| `fix/*`     | Bug fixes (e.g., `fix/empty-module-crash`). Branched from `dev`.                                                                    |
| `release/*` | Release preparation branches. Branched from `dev`, merged into both `main` and `dev`.                                               |
| `hotfix/*`  | Urgent production fixes. Branched from `main`, merged into both `main` and `dev`.                                                   |

### Workflow

1. **Always branch from `dev`** — never from `main` (unless it's a hotfix).
2. **Keep your branch up-to-date** — regularly pull/rebase from `dev` to avoid merge conflicts.
3. **Merge back into `dev`** — open a Pull Request targeting `dev`, not `main`.
4. **`dev` → `main`** — only done during a release, typically via a `release/*` branch.

```
main    ─────────────────────────● (v0.2.0) ──────────
                                ↗
dev     ────●────●────●────●───●────────────────────────
           ↗    ↗    ↗    ↗
feature  ●    ●    ●    ●
```

---

## Issue Management

### Labels

We use the following labels to categorize and prioritize issues:

| Label              | Description                                                   |
| ------------------ | ------------------------------------------------------------- |
| `bug`              | Something isn't working as expected                           |
| `feature`          | New feature request                                           |
| `enhancement`      | Improvement to existing functionality                         |
| `documentation`    | Improvements or additions to documentation                    |
| `tests`            | Related to testing (adding tests, fixing test infrastructure) |
| `good first issue` | Good for newcomers                                            |
| `help wanted`      | Extra attention or community help needed                      |

**When creating an issue:**

- Assign at least one **type** label (`bug`, `feature`, `enhancement`, `documentation`, `tests`)
- Assign a **priority** label if known
- Assign a **milestone** label (e.g., `v0.2.0`) if the issue targets a specific release

**When starting work on an issue:**

- Assign it to yourself
- Add the `status: in-progress` label
- Link it to your branch/PR (see [Closing Issues](#closing-issues))

### Closing Issues

Issues should be closed **automatically** when the related PR is merged. Use one of the following keywords in your PR description or commit message:

```
Closes #123
Fixes #456
Resolves #789
```

You can close multiple issues at once:

```
Closes #12, #34, #56
```

**Manual closing** is acceptable only when:

- The issue is a duplicate (link to the original)
- The issue is no longer relevant (explain why)
- The issue cannot be reproduced (provide details)

Always leave a comment explaining why an issue is being closed manually.

---

## Code Style

- **Type annotations** are required for all public functions and methods
- Follow existing naming conventions and module structure

Before submitting, ensure your code:

```bash
uv run ruff check .
uv run mypy docstr_health
```

---

## Pull Request Process

1. **Create a branch** from `dev` using the appropriate prefix:

   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit with clear, descriptive messages (see [Commit Style](#commit-style))

3. **Ensure quality:**

   ```bash
   uv run ruff check .
   uv run mypy docstr_health
   uv run pytest
   ```

4. **Open a Pull Request** targeting `dev` (not `main`!)
   - Fill out the PR template
   - Link related issues using `Closes #N`
   - Request review from maintainers

5. **Respond to feedback** — we may ask for changes before merging

6. **After merge** — your branch will be deleted automatically

### Commit Style

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add --fail-under flag for CI integration
fix: handle empty modules gracefully
docs: update README with new examples
refactor: extract status classification to separate method
test: add unit tests for DocstringChecker
chore: update dependencies
```

**Format:** `<type>(<scope>): <description>`

| Type       | Description                                             |
| ---------- | ------------------------------------------------------- |
| `feat`     | New feature                                             |
| `fix`      | Bug fix                                                 |
| `docs`     | Documentation only                                      |
| `style`    | Formatting, no code change                              |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test`     | Adding or fixing tests                                  |
| `chore`    | Maintenance tasks                                       |

---

## Reporting Issues

- **Bug reports**: include the full command you ran, the output, and the environment (Python version, OS)
- **Feature requests**: describe the use case and how it would benefit the project
- **Questions**: feel free to open a discussion

---

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

**Thank you for contributing to docstr-health!**
