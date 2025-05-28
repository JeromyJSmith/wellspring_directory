# Wellspring Book Production System Guide

## Build & Test Commands
- Build: `python -m hatchling build`
- Install dependencies: `pip install -e ".[dev,ai,research]"` or `uv install -e ".[full]"`
- Run tests: `pytest -ra --strict-markers tests/`
- Run single test: `pytest tests/test_file.py::test_function -v`
- Lint code: `black .`
- System test: `python test_system.py`
- CLI usage: `python wellspring_cli.py [command]`
- Process typography: `python em_dash_replacement/scripts/em_dash_processor.py`
- Generate visual infographics: `python deep_research_agent/scripts/visual_opportunities_generator.py`
- Initialize database: `python shared_utils/data/init_database.py`

## Code Style Guidelines
- Black formatting with line length 100
- Python 3.9+ support (target all versions 3.9-3.12)
- Type hints required for all parameters and returns
- Use dataclasses for structured data models
- Module imports order: stdlib → third-party → local
- Error handling: Specific exceptions with detailed logging
- SQLite for persistent storage with clear schema design
- Docstrings with triple quotes for all modules, classes, methods
- Keep files < 500 lines; split complex functionality
- Comment non-obvious code with `# Reason:`
- Context manager patterns for database and file operations

## Agent Orchestration & Data Model
- Agent communication via strict JSON contracts
- Data persistence through SQLite database (wellspring.db)
- Main tables: typography_sessions, em_dash_patterns, visual_opportunities
- Log processing sessions and statistics for traceability
- Confidence thresholds control automation vs. manual review
- Report generation in structured markdown format
- Context-based pattern matching with similarity scoring

## Project Organization
- Typography corrections: `em_dash_replacement/`
- Research outputs: `deep_research_agent/`
- Agent workflows: `google_adk_agents/`
- Shared utilities: `shared_utils/`
- Configuration: `config.json` and pyproject.toml `[tool.wellspring]`
- Agent rules: `.cursor/rules/`