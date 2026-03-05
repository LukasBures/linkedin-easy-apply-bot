# Repository Guidelines

## Project Structure & Module Organization
Core code lives in `linkedin_easy_apply/`:

- `app/` orchestration and runtime entry (`orchestrator.py`, `runner.py`)
- `services/` business workflows (session, apply flow, questions, diagnostics, throughput)
- `infra/` browser/repository adapters
- `config/` config loader + schema
- `domain/` typed models
- `observability/` logger + JSONL event logging
- `qa/` auto-answer engine (`questions_answers.yaml`-driven)

Compatibility entrypoints: `easy_apply_bot.py` and `linkedin_easy_apply/bot.py`.
Runtime artifacts are written to `logs/`, `results/`, and `debug/`.

## Build, Test, and Development Commands
- `make venv` - create Python 3.12 virtual env via `uv`
- `make sync` - install dependencies from `pyproject.toml`/`uv.lock`
- `make run` - start the bot using `config.yaml` + `.env`
- `make format` - format code with Ruff
- `make test` - run discovered pytest files (excluding vendored/runtime dirs)
- `pre-commit run --all-files` - run repository hooks locally

## Coding Style & Naming Conventions
Use Python 3.12, 4-space indentation, and type hints for new/refactored code.
Use `snake_case` for functions/variables, `PascalCase` for classes, and keep modules focused by responsibility.
Prefer adding new behavior in `services/` or `infra/` instead of growing orchestrator logic.
Formatting/linting is Ruff-based via pre-commit.

## Testing Guidelines
Test framework: `pytest` (invoked by `make test`).
Naming: `test_*.py` or `*_test.py`.
Place new tests under `tests/` (recommended) or adjacent test modules.
Mock browser/LinkedIn interactions where possible; prioritize deterministic tests for config loading, answer rendering, filtering, and event/result persistence.

## Commit & Pull Request Guidelines
History uses short imperative messages; conventional prefixes are acceptable (`feat:`, `fix:`, `refactor:`).
Keep commits atomic and scoped to one concern.
PRs should include:
- purpose and behavior change summary
- key files/modules touched
- validation evidence (`make format`, `make test`, and any manual runtime checks)
- config/security impact notes

## Security & Configuration Tips
Do not commit secrets. Keep credentials/profile/compensation in `.env`:
`LINKEDIN_USERNAME`, `LINKEDIN_PASSWORD`, `LINKEDIN_PHONE_NUMBER`, `LINKEDIN_LOCATION_COUNTRY`, `LINKEDIN_LOCATION_CITY`, `LINKEDIN_PROFILE_URL`, `LINKEDIN_SALARY`, `LINKEDIN_RATE`.
Use `.env.example` as template and keep cookie/debug artifacts private.
