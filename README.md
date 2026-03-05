# LinkedIn Easy Apply Bot (Python, Selenium, Easy Apply Automation)

A production-focused **LinkedIn Easy Apply automation bot** built with **Python 3.12** and **Selenium**.
It automates repetitive Easy Apply workflows with configurable search targets, session pacing, structured logs, and rule-based question answering.

Keywords: `linkedin-easy-apply-bot`, `linkedin automation`, `selenium python bot`, `easy apply automation`, `job application bot`, `yaml form autofill`.

## Why This Repository

This project is designed for developers and technical job seekers who want to:

- Automate repetitive Easy Apply steps
- Run controlled job-search sessions (duration, breaks, throughput)
- Keep auditable outputs (`logs/events.jsonl`, `results/*.json`)
- Reuse deterministic question-answer rules from YAML

## Key Features

- Easy Apply workflow orchestration with retry/stall diagnostics
- Cookie session restore/save for LinkedIn authentication continuity
- Configurable role/location search loops with page caps
- Throughput metrics: attempts, failures, success rate, projected applications/hour
- Auto-answer engine for common application questions
- Debug snapshots for failed flows

## Repository Structure

```text
linkedin_easy_apply/
  app/            # orchestration + runtime entry
  services/       # apply/session/questions/diagnostics/throughput services
  infra/          # browser and persistence adapters
  config/         # loader + schema
  domain/         # typed runtime models
  observability/  # logger + JSONL events
  qa/             # question answer engine
```

Compatibility entrypoint: `easy_apply_bot.py`

## Suggested GitHub Topics

Set these repository topics in GitHub for discoverability:

- `linkedin`
- `linkedin-easy-apply`
- `python`
- `selenium`
- `automation`
- `job-search`
- `easy-apply`
- `webdriver`
- `yaml`

## Quick Start

```bash
make venv
make sync
cp .env.example .env
```

Set required environment variables in `.env`:

- `LINKEDIN_USERNAME`
- `LINKEDIN_PASSWORD`
- `LINKEDIN_PHONE_NUMBER`
- `LINKEDIN_LOCATION_COUNTRY`
- `LINKEDIN_LOCATION_CITY`
- `LINKEDIN_PROFILE_URL`
- `LINKEDIN_SALARY`
- `LINKEDIN_RATE`

Then edit non-secret search settings in `config.yaml` and run:

```bash
make run
```

## Development

- `make format` - format Python code with Ruff
- `make test` - run project tests if present
- `pre-commit run --all-files` - run repository checks

## Outputs

- `logs/` runtime logs
- `logs/events.jsonl` structured event timeline
- `results/` application outcome records
- `debug/` failure and first-job diagnostics

## Security & Privacy

- `.env`, cookies, logs, debug artifacts, and results are ignored by git
- Keep credentials only in `.env`
- Review automation behavior and comply with platform terms

## License

MIT License - free for personal and commercial use, with attribution retained.
