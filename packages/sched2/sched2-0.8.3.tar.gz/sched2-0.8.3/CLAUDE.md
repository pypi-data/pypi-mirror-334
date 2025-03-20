# sched2 Development Guidelines

## Commands
- Run linters: `make fix`
- Check linting: `make check` 
- Run all tests: `make test` or `uv run pytest -v`
- Run a single test: `uv run pytest -v tests/test_sched2.py::test_name`
- Publish to PyPI: `make publish`

## Code Style Guidelines
- Use ruff for formatting and linting
- Follow PEP 8 conventions
- Import order: standard library, then third-party, then local
- Use docstrings for all public functions, methods, and classes
- Include type hints where appropriate
- Use descriptive variable names in snake_case
- Use clear error messages with specific exception types
- Use pytest for testing with descriptive test names
- Keep functions focused and small (single responsibility)
- For repeating patterns, use standard Python idioms
- Maintain backward compatibility for public API