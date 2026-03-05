from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from linkedin_easy_apply.app.orchestrator import LinkedInEasyApplyOrchestrator


class ServiceBase:
    def __init__(self, bot: "LinkedInEasyApplyOrchestrator") -> None:
        self.bot = bot
