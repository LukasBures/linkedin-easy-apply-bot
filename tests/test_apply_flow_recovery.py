from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.modules.setdefault(
    "pyautogui",
    SimpleNamespace(
        position=lambda: (0, 0),
        moveTo=lambda *args, **kwargs: None,
        keyDown=lambda *args, **kwargs: None,
        press=lambda *args, **kwargs: None,
        keyUp=lambda *args, **kwargs: None,
    ),
)

from linkedin_easy_apply.services.apply_flow_service import ApplyFlowService
from linkedin_easy_apply.services.question_service import QuestionService


class FakeDialog:
    def __init__(self, text: str = "", *, displayed: bool = True, screen: str = ""):
        self.text = text
        self._displayed = displayed
        self._screen = screen

    def is_displayed(self) -> bool:
        return self._displayed

    def get_attribute(self, name: str) -> str:
        if name == "data-sdui-screen":
            return self._screen
        if name == "aria-label":
            return self.text
        return ""


class FakeBrowser:
    def __init__(self, page_source: str, dialogs: list[FakeDialog] | None = None):
        self.page_source = page_source
        self._dialogs = dialogs or []

    def find_elements(self, by, value):
        return list(self._dialogs)


class FakeBot:
    def __init__(self, browser: FakeBrowser | None = None):
        self.browser = browser
        self.location_city = "Prague"
        self.location_country = "Czechia"


class ApplyFlowRecoveryTests(unittest.TestCase):
    def test_detect_daily_easy_apply_limit_from_page_source(self) -> None:
        service = ApplyFlowService(
            FakeBot(
                FakeBrowser(
                    "<html><body>You reached today’s Easy Apply limit. "
                    "Save this job and continue applying tomorrow.</body></html>"
                )
            )
        )

        detected, marker = service.detect_daily_easy_apply_limit()

        self.assertTrue(detected)
        self.assertEqual(marker, "you reached today's easy apply limit")

    def test_detect_daily_easy_apply_limit_from_dialog_screen(self) -> None:
        service = ApplyFlowService(
            FakeBot(
                FakeBrowser(
                    "<html></html>",
                    dialogs=[
                        FakeDialog(
                            "Great effort applying today.",
                            screen="com.linkedin.sdui.flagshipnav.jobs.EasyApplyFuseLimitDialogModal",
                        )
                    ],
                )
            )
        )

        detected, marker = service.detect_daily_easy_apply_limit()

        self.assertTrue(detected)
        self.assertEqual(marker, "dialog_screen")

    def test_accommodation_prompt_uses_na_placeholder(self) -> None:
        service = QuestionService(FakeBot())

        answer = service.humanize_free_text_answer(
            (
                "We want everyone to have a fair chance to succeed. "
                "If you have a disability, condition, or specific need that requires "
                "adjustments to our recruitment process, please let us know below so "
                'we are able to best support you (if you do not require any adjustment, '
                'please type "N/A").'
            ),
            "",
            "textarea",
        )

        self.assertEqual(answer, "N/A")


if __name__ == "__main__":
    unittest.main()
