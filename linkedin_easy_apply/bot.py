from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from linkedin_easy_apply.domain.models import AppConfig
from linkedin_easy_apply.observability.logger import log, setup_logger

from .app.orchestrator import LinkedInEasyApplyOrchestrator


class EasyApplyBot(LinkedInEasyApplyOrchestrator):
    """Backward-compatible facade over the new orchestrator architecture."""

    def __init__(
        self,
        username,
        password,
        phone_number,
        salary,
        rate,
        upload_files=None,
        results_filename="results.json",
        events_filename="logs/events.jsonl",
        cookies_path=".auth/linkedin_cookies.json",
        location_country="CZ",
        location_city="New York",
        blacklist=None,
        blacklist_titles=None,
        experience_level=None,
        ans_yaml_path="questions_answers.yaml",
        max_pages_per_search: int = 3,
        session_duration_hours_min: float = 3.0,
        session_duration_hours_max: float = 5.0,
        short_break_min_seconds: int = 20,
        short_break_max_seconds: int = 75,
        short_break_every_min_minutes: int = 8,
        short_break_every_max_minutes: int = 18,
        throughput_window_minutes: int = 30,
        shuffle_search_combos: bool = False,
    ) -> None:
        setup_logger()

        payload: dict[str, Any] = {
            "username": username,
            "password": password,
            "phone_number": phone_number,
            "salary": salary,
            "rate": rate,
            "uploads": upload_files or {},
            "positions": [],
            "locations": [],
            "events_filename": events_filename,
            "cookies_path": cookies_path,
            "location_country": location_country,
            "location_city": location_city,
            "blacklist": blacklist or [],
            "blackListTitles": blacklist_titles or [],
            "experience_level": experience_level or [],
            "ans_yaml_path": ans_yaml_path,
            "max_pages_per_search": max_pages_per_search,
            "session_duration_hours_min": session_duration_hours_min,
            "session_duration_hours_max": session_duration_hours_max,
            "short_break_min_seconds": short_break_min_seconds,
            "short_break_max_seconds": short_break_max_seconds,
            "short_break_every_min_minutes": short_break_every_min_minutes,
            "short_break_every_max_minutes": short_break_every_max_minutes,
            "shuffle_search_combos": shuffle_search_combos,
            "throughput_window_minutes": throughput_window_minutes,
        }

        if results_filename == "results.json":
            results_filename = (
                f"results/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json"
            )

        config = AppConfig.from_dict(payload, results_filename=results_filename)
        super().__init__(config)


__all__ = ["EasyApplyBot", "log", "setup_logger"]
