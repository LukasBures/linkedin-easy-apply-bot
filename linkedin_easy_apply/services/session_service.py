from __future__ import annotations

import json
import time
from pathlib import Path

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from linkedin_easy_apply.observability.logger import log

from .base import ServiceBase


class SessionService(ServiceBase):
    def start_linkedin(self, username: str, password: str) -> None:
        log.info("Logging in.....Please wait :)  ")
        self.bot.browser.get(
            "https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin"
        )
        try:
            user_field = self.bot.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            pw_field = self.bot.wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            login_button = self.bot.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            user_field.send_keys(username)
            user_field.send_keys(Keys.TAB)
            time.sleep(2)
            pw_field.send_keys(password)
            time.sleep(2)
            login_button.click()
            time.sleep(8)
            if self.is_logged_in():
                self.bot.log_event("login_success", method="credentials")
            else:
                self.bot.log_event(
                    "login_uncertain",
                    method="credentials",
                    current_url=self.bot.browser.current_url,
                )
        except (TimeoutException, NoSuchElementException, WebDriverException) as exc:
            log.error(f"Login flow failed: {exc}")
            self.bot.log_event("login_error", method="credentials", error=str(exc))

    def is_logged_in(self) -> bool:
        try:
            current_url = (self.bot.browser.current_url or "").lower()
            if "/login" in current_url or "/checkpoint/challenge" in current_url:
                return False
            if any(
                path in current_url
                for path in ("/feed", "/jobs", "/mynetwork", "/messaging")
            ):
                return True
            return (
                len(
                    self.bot.browser.find_elements(
                        By.CSS_SELECTOR,
                        "a[data-test-global-nav-link='profile'], a[href*='/in/']",
                    )
                )
                > 0
            )
        except Exception:
            return False

    def restore_session_from_cookies(self) -> bool:
        cookie_file = Path(self.bot.cookies_path)
        if not cookie_file.exists():
            self.bot.log_event(
                "cookies_restore_skipped",
                reason="cookie_file_missing",
                cookies_path=self.bot.cookies_path,
            )
            return False

        try:
            with open(cookie_file, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            if not isinstance(cookies, list):
                self.bot.log_event(
                    "cookies_restore_skipped",
                    reason="cookie_file_invalid",
                    cookies_path=self.bot.cookies_path,
                )
                return False

            self.bot.browser.get("https://www.linkedin.com/")
            for cookie in cookies:
                if not isinstance(cookie, dict):
                    continue
                c = dict(cookie)
                if "sameSite" in c and c["sameSite"] not in ("Strict", "Lax", "None"):
                    c.pop("sameSite", None)
                if "expiry" in c:
                    try:
                        c["expiry"] = int(c["expiry"])
                    except Exception:
                        c.pop("expiry", None)
                try:
                    self.bot.browser.add_cookie(c)
                except Exception:
                    continue

            self.bot.browser.get("https://www.linkedin.com/feed/")
            time.sleep(2)
            ok = self.is_logged_in()
            self.bot.log_event(
                "cookies_restore_result",
                success=ok,
                cookies_path=self.bot.cookies_path,
                current_url=self.bot.browser.current_url,
            )
            return ok
        except Exception as exc:
            self.bot.log_event(
                "cookies_restore_error",
                cookies_path=self.bot.cookies_path,
                error=str(exc),
            )
            return False

    def save_session_cookies(self) -> None:
        try:
            cookies = self.bot.browser.get_cookies()
            with open(self.bot.cookies_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            self.bot.log_event(
                "cookies_saved",
                cookies_path=self.bot.cookies_path,
                cookie_count=len(cookies),
            )
        except Exception as exc:
            self.bot.log_event(
                "cookies_save_error", cookies_path=self.bot.cookies_path, error=str(exc)
            )
