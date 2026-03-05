# linkedin-easy-apply-bot

**LinkedIn Easy Apply Bot for developers and technical job seekers**.  
Automates repetitive LinkedIn Easy Apply steps with Python + Selenium, YAML-based form answering, session persistence, and diagnostics.

Targets search terms: `linkedin easy apply bot`, `linkedin automation python`, `job application bot for developers`, `selenium linkedin bot`, `easy apply automation`.

## Why Developers Use This

- Apply to more relevant software roles in less time
- Keep search sessions controlled (duration, breaks, throughput)
- Use structured answers for recurring application questions
- Preserve session continuity with cookie restore/save
- Debug failures quickly with logs and snapshots

## Why This Repo

- Env-based secrets (`.env`) instead of committing credentials in config
- Modular architecture (`app/`, `services/`, `infra/`, `domain/`, `qa/`)
- Structured event logging (`logs/events.jsonl`) and diagnostics traces
- Make-based developer workflow (`make run`, `make test`, `make format`)
- MIT license and contributor guide (`AGENTS.md`)

## Architecture

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

Entrypoint: `easy_apply_bot.py`

## How To Start

### 1. Install and bootstrap

```bash
make venv
make sync
cp .env.example .env
```

### 2. Configure `.env` (secrets + profile)

- `LINKEDIN_USERNAME`
- `LINKEDIN_PASSWORD`
- `LINKEDIN_PHONE_NUMBER`
- `LINKEDIN_LOCATION_COUNTRY`
- `LINKEDIN_LOCATION_CITY`
- `LINKEDIN_PROFILE_URL`
- `LINKEDIN_SALARY`
- `LINKEDIN_RATE`

### 3. Configure job targeting in `config.yaml`

- `positions` (target job titles)
- `locations` (target places/remote)
- `max_pages_per_search`
- `session_duration_*` and `short_break_*` pacing

### 4. Configure answer logic in `questions_answers.yaml`

- `defaults`: fallback values
- `profile`: years/work-auth/demographic fields
- `rules`: regex-based mappings for application questions

### 5. Run

```bash
make run
```

## First Login and 2FA (Important)

On first run, LinkedIn may request verification.  
When Chrome opens the login popup, enter the verification code sent to your email and confirm.  
After successful login, cookies are saved (under `.auth/`) so next runs are usually smoother.

## Commands

- `make run` - start the bot
- `make test` - run all tests (if present)
- `make format` - format code with Ruff
- `pre-commit run --all-files` - run repository checks

## Output Files

- `logs/` - runtime logs
- `logs/events.jsonl` - structured event timeline
- `results/` - application outcome records
- `debug/` - diagnostics and failure snapshots

## Privacy and Safety

- `.env`, `.auth`, logs, debug artifacts, and results are gitignored
- Keep credentials only in `.env`
- Use responsibly and review platform terms before automation

## Suggested GitHub Topics

Set these in repository topics for discoverability:

- `linkedin`
- `linkedin-easy-apply`
- `easy-apply`
- `job-search`
- `job-automation`
- `python`
- `selenium`
- `webdriver`
- `yaml`

## License

MIT License. Free for personal and commercial use with copyright notice retained.
