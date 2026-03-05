from __future__ import annotations

from linkedin_easy_apply.config.loader import load_run_config
from linkedin_easy_apply.domain.models import AppConfig
from linkedin_easy_apply.observability.logger import log

from .orchestrator import LinkedInEasyApplyOrchestrator


def run_from_config(config_path: str = "config.yaml") -> None:
    run_cfg = load_run_config(config_path)
    app_config = AppConfig.from_dict(
        run_cfg.parameters, results_filename=run_cfg.results_filename
    )

    log.info(
        {
            k: run_cfg.parameters[k]
            for k in run_cfg.parameters.keys()
            if k not in ["username", "password"]
        }
    )

    bot = LinkedInEasyApplyOrchestrator(app_config)
    try:
        bot.start_apply(app_config.positions, app_config.locations)
    except KeyboardInterrupt:
        bot.log_event("session_interrupted", reason="keyboard_interrupt")
        log.warning("Session interrupted by user (Ctrl+C).")
    finally:
        try:
            bot.browser.quit()
        except Exception:
            pass


def main() -> None:
    run_from_config("config.yaml")
