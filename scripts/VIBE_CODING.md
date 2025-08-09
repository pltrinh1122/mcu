# Component-Specific Vibe-Coding: scripts

## Additional Validation

- Python syntax: `python -m py_compile scripts/*.py`
- Recommended formatting: `black --check scripts/`
- Recommended linting: `flake8 scripts/`
- Recommended type checking: `mypy scripts/`
- Security scanning: Deferred (Operator decision)

## Component-Specific Tests

- If unit tests exist under `tests/` for Python modules in `scripts/`, run `pytest tests/`.
- Otherwise, perform focused smoke checks for modified scripts (e.g., `--help` runs) when safe.

## Component Conventions

- New Python code uses OOP patterns (classes, encapsulation, type hints, docstrings).
- Prefer clear public interfaces and error handling via specific exceptions.
- Follow Conventional Commits for messages affecting `scripts/`.

## Notes

- Auto-install missing tools when needed; if installation is blocked/unavailable, pause and request Operator approval before proceeding.
- Do not modify or migrate `__vibew-*` files.
- Link checks are optional and run only on Operator request.


