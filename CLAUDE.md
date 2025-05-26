# Wellspring Book Production System Guide

## Build & Test Commands
- Build: `python -m hatchling build`
- Install dev dependencies: `pip install -e ".[dev]"` or `uv install -e ".[dev]"`
- Run tests: `pytest -ra --strict-markers tests/`
- Run single test: `pytest tests/test_file.py::test_function -v`
- Lint code: `black .`
- System test: `python test_system.py`
- CLI usage: `python wellspring_cli.py [command]`
- Process typography: `python em_dash_replacement/scripts/em_dash_processor.py`

## Code Style Guidelines
- Black formatting with line length 100
- Python 3.9+ support (3.9, 3.10, 3.11, 3.12)
- Type hints required for all function parameters and returns
- Docstrings for all modules, classes, and public methods
- Module imports order: stdlib, third-party, local
- Error handling: use try/except with specific exception types
- Prefer async patterns for agent workflows
- Keep files under 500 lines when possible
- Comment non-obvious code and explain intent with `# Reason:`

## Em Dash Replacement Rules
- Replace em dashes with context-appropriate punctuation
- Common replacements:
  - Parenthetical info: em dash → commas
  - Ranges: em dash → "to" or "-"
  - Attribution: em dash → period + space + em dash
  - Abrupt change: em dash → comma or semicolon
  - List introduction: em dash → colon
- Always consider: sentence structure, paragraph coherence, author's intent
- Log all changes with page/line numbers and replacement rationale

## Project Organization
- Typography corrections use `em_dash_replacement/` directory
- Research outputs go in `deep_research_agent/` directory
- Shared utilities live in `shared_utils/`
- Configuration managed through `config.json`
- Agent orchestration via rules in `.cursor/rules/` directory