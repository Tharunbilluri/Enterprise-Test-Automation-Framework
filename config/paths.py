"""Filesystem path constants for the framework."""

from __future__ import annotations

from pathlib import Path

# Enterprise-Test-Automation-Framework/ (repository root)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

TESTS_DIR: Path = PROJECT_ROOT / "tests"
PAGES_DIR: Path = PROJECT_ROOT / "pages"
LOCATORS_DIR: Path = PROJECT_ROOT / "locators"
UTILS_DIR: Path = PROJECT_ROOT / "utils"
CONFIG_DIR: Path = PROJECT_ROOT / "config"
TESTDATA_DIR: Path = PROJECT_ROOT / "testdata"
RESOURCES_DIR: Path = PROJECT_ROOT / "resources"
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
SCREENSHOTS_DIR: Path = PROJECT_ROOT / "screenshots"
LOGS_DIR: Path = PROJECT_ROOT / "logs"
