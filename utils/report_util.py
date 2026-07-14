"""Reporting helpers: Allure environment metadata and timestamped paths."""

from __future__ import annotations

from pathlib import Path

from config.settings import get_settings
from utils.file_util import ensure_directory, timestamp_slug, write_json
from utils.logger_util import get_logger

logger = get_logger(__name__)


def allure_results_dir() -> Path:
    """Return (and create) the Allure results directory."""
    settings = get_settings()
    path = ensure_directory(settings.reports_dir / "allure-results")
    return path


def html_report_path() -> Path:
    """Return a timestamped pytest-html report path."""
    settings = get_settings()
    ensure_directory(settings.reports_dir)
    return settings.reports_dir / f"report_{timestamp_slug()}.html"


def write_allure_environment() -> Path:
    """
    Write ``environment.properties`` for Allure dashboard context.

    Call from CI or locally before ``allure generate``.
    """
    settings = get_settings()
    results = allure_results_dir()
    env_file = results / "environment.properties"
    lines = [
        f"Browser={settings.browser}",
        f"Headless={settings.headless}",
        f"Engine={settings.automation_engine}",
        f"Base.URL={settings.base_url}",
        f"Python.Framework=Enterprise-TAF",
        f"Explicit.Wait.Seconds={settings.explicit_wait}",
    ]
    env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info("Wrote Allure environment.properties -> %s", env_file)
    return env_file


def write_run_manifest() -> Path:
    """Persist a small JSON manifest of the current run configuration."""
    settings = get_settings()
    manifest = {
        "browser": settings.browser,
        "headless": settings.headless,
        "engine": settings.automation_engine,
        "base_url": settings.base_url,
        "timestamp": timestamp_slug(),
    }
    path = settings.reports_dir / f"run_manifest_{manifest['timestamp']}.json"
    write_json(path, manifest)
    return path
