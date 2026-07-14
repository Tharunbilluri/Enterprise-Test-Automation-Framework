"""Configuration package public exports."""

from config.browser_config import (
    SUPPORTED_BROWSERS,
    SUPPORTED_ENGINES,
    playwright_common_args,
    selenium_common_args,
    validate_browser,
    validate_engine,
)
from config.paths import PROJECT_ROOT, TESTDATA_DIR
from config.settings import Settings, get_settings

__all__ = [
    "PROJECT_ROOT",
    "TESTDATA_DIR",
    "Settings",
    "SUPPORTED_BROWSERS",
    "SUPPORTED_ENGINES",
    "get_settings",
    "playwright_common_args",
    "selenium_common_args",
    "validate_browser",
    "validate_engine",
]
