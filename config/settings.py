"""Centralized configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

from config.paths import PROJECT_ROOT


def _load_env_file() -> None:
    """Load `.env` from the project root if present."""
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(dotenv_path=env_path, override=False)


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _as_int(value: str | None, default: int) -> int:
    if value is None or value.strip() == "":
        return default
    return int(value)


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings for the automation framework."""

    base_url: str
    base_title: str
    browser: str
    headless: bool
    implicit_wait: int
    explicit_wait: int
    page_load_timeout: int
    window_width: int
    window_height: int
    automation_engine: str
    valid_username: str
    valid_password: str
    invalid_username: str
    invalid_password: str
    locked_username: str
    log_level: str
    screenshot_on_failure: bool
    reports_dir: Path
    screenshots_dir: Path
    logs_dir: Path
    pytest_workers: str
    reruns: int
    reruns_delay: int

    @property
    def is_selenium(self) -> bool:
        return self.automation_engine.lower() == "selenium"

    @property
    def is_playwright(self) -> bool:
        return self.automation_engine.lower() == "playwright"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return cached Settings built from environment variables.

    CLI overrides (via pytest) should call ``get_settings.cache_clear()``
    after mutating ``os.environ`` when needed.
    """
    _load_env_file()

    reports = PROJECT_ROOT / os.getenv("REPORTS_DIR", "reports")
    screenshots = PROJECT_ROOT / os.getenv("SCREENSHOTS_DIR", "screenshots")
    logs = PROJECT_ROOT / os.getenv("LOGS_DIR", "logs")

    return Settings(
        base_url=os.getenv("BASE_URL", "https://www.saucedemo.com/"),
        base_title=os.getenv("BASE_TITLE", "Swag Labs"),
        browser=os.getenv("BROWSER", "chrome").lower(),
        headless=_as_bool(os.getenv("HEADLESS"), default=False),
        implicit_wait=_as_int(os.getenv("IMPLICIT_WAIT"), default=0),
        explicit_wait=_as_int(os.getenv("EXPLICIT_WAIT"), default=15),
        page_load_timeout=_as_int(os.getenv("PAGE_LOAD_TIMEOUT"), default=30),
        window_width=_as_int(os.getenv("WINDOW_WIDTH"), default=1920),
        window_height=_as_int(os.getenv("WINDOW_HEIGHT"), default=1080),
        automation_engine=os.getenv("AUTOMATION_ENGINE", "selenium").lower(),
        valid_username=os.getenv("VALID_USERNAME", "standard_user"),
        valid_password=os.getenv("VALID_PASSWORD", "secret_sauce"),
        invalid_username=os.getenv("INVALID_USERNAME", "invalid_user"),
        invalid_password=os.getenv("INVALID_PASSWORD", "wrong_password"),
        locked_username=os.getenv("LOCKED_USERNAME", "locked_out_user"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        screenshot_on_failure=_as_bool(
            os.getenv("SCREENSHOT_ON_FAILURE"), default=True
        ),
        reports_dir=reports,
        screenshots_dir=screenshots,
        logs_dir=logs,
        pytest_workers=os.getenv("PYTEST_WORKERS", "auto"),
        reruns=_as_int(os.getenv("RERUNS"), default=1),
        reruns_delay=_as_int(os.getenv("RERUNS_DELAY"), default=1),
    )
