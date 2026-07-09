# Roadmap

## [v0.2.0] - Statistics & Reporting ← Development Status: 3 - Alpha

- Percentage metrics (docstring presence, status breakdown)
- Per-module and project overall score/rating
- JSON and Markdown export (`--output json|md`)
- Average, median, longest docstring stats

## [v0.3.0] — Rich Display & Checkers ← Development Status: 3 - Alpha

- Tree view with `rich.Tree` (modules → classes → functions)
- Visual distinction of classes vs functions
- Type annotation checker (per-function args/return state)
- Test coverage checker
- Project structure checker (README, pyproject.toml, .gitignore)

## [v0.4.0] — CLI Expansion ← Development Status: 4 - Beta

- `--function`, `--module`, `--from-file` flags
- Private/dunder methods inclusion flag
- `@staticmethod` detection suggestion
- Custom parser error output
- Skipped modules in statistics table with color

## [v1.0.0] — Production Ready ← Development Status: 5 - Production/Stable

- Pre-commit hook
- Exit codes for CI integration
- Performance optimization (memory usage)
- Comprehensive documentation (mkdocs)
- SECURITY.md, CITATION.cff
- PEP 257 / PEP 263 audit
