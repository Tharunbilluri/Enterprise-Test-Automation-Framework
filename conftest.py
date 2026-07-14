"""
Root pytest configuration: CLI options, fixtures, failure screenshots.

Supports Selenium and Playwright engines, cross-browser, headless,
and timestamped report/log artifact directories.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from typing import Any

import pytest

from config.settings import get_settings
from utils.browser_util import (
    PlaywrightSession,
    create_playwright_session,
    create_selenium_driver,
    quit_selenium_driver,
)
from utils.file_util import ensure_directory, load_testdata, timestamp_slug
from utils.logger_util import get_logger
from utils.report_util import write_allure_environment, write_run_manifest
from utils.screenshot_util import capture_failure_screenshot

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# CLI configuration
# ---------------------------------------------------------------------------

def pytest_addoption(parser: pytest.Parser) -> None:
    """Register enterprise CLI flags for configurable execution."""
    group = parser.getgroup("enterprise-taf")
    group.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser: chrome | edge | firefox (overrides .env)",
    )
    group.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser headless (overrides .env)",
    )
    group.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Force headed mode even if .env HEADLESS=true",
    )
    group.addoption(
        "--engine",
        action="store",
        default=None,
        choices=["selenium", "playwright"],
        help="Automation engine: selenium | playwright",
    )
    group.addoption(
        "--app-url",
        action="store",
        default=None,
        dest="app_url",
        help="Override application BASE_URL (avoids conflict with pytest-base-url)",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Apply CLI overrides to environment and prepare artifact dirs."""
    if config.getoption("--browser"):
        os.environ["BROWSER"] = str(config.getoption("--browser")).lower()
    if config.getoption("--engine"):
        os.environ["AUTOMATION_ENGINE"] = str(config.getoption("--engine")).lower()
    if config.getoption("--app-url"):
        os.environ["BASE_URL"] = str(config.getoption("--app-url"))

    if config.getoption("--headless"):
        os.environ["HEADLESS"] = "true"
    elif config.getoption("--headed"):
        os.environ["HEADLESS"] = "false"

    get_settings.cache_clear()
    settings = get_settings()

    ensure_directory(settings.reports_dir)
    ensure_directory(settings.screenshots_dir)
    ensure_directory(settings.logs_dir)

    # Timestamped HTML report path (pytest-html uses --html from addopts;
    # override when running so each run is unique under reports/).
    stamp = timestamp_slug()
    html_path = settings.reports_dir / f"report_{stamp}.html"
    if hasattr(config.option, "htmlpath"):
        config.option.htmlpath = str(html_path)

    write_allure_environment()
    write_run_manifest()

    logger.info(
        "Framework configured | engine=%s browser=%s headless=%s base_url=%s",
        settings.automation_engine,
        settings.browser,
        settings.headless,
        settings.base_url,
    )


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def settings():
    """Session-scoped settings object."""
    return get_settings()


@pytest.fixture(scope="session")
def test_data() -> dict[str, Any]:
    """Load Sauce Demo JSON testdata once per session."""
    return load_testdata("saucedemo_data.json")


@pytest.fixture
def driver(settings) -> Generator[Any, None, None]:
    """
    Function-scoped Selenium WebDriver.

    Skips automatically when AUTOMATION_ENGINE=playwright.
    """
    if settings.automation_engine != "selenium":
        pytest.skip("Selenium driver fixture requires AUTOMATION_ENGINE=selenium")

    web_driver = create_selenium_driver(settings=settings)
    logger.info("Selenium driver created for test")
    yield web_driver
    quit_selenium_driver(web_driver)


@pytest.fixture
def pw_session(settings) -> Generator[PlaywrightSession, None, None]:
    """
    Function-scoped Playwright session (browser + page).

    Skips automatically when AUTOMATION_ENGINE=selenium.
    """
    if settings.automation_engine != "playwright":
        pytest.skip("Playwright fixture requires AUTOMATION_ENGINE=playwright")

    session = create_playwright_session(settings=settings)
    yield session
    session.close()


@pytest.fixture
def page(pw_session: PlaywrightSession):
    """Convenience fixture exposing the Playwright page."""
    return pw_session.page


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Capture screenshots on test failure for Selenium or Playwright."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when != "call" or not report.failed:
        return

    settings = get_settings()
    if not settings.screenshot_on_failure:
        return

    test_name = item.name
    driver = item.funcargs.get("driver")
    page = item.funcargs.get("page")
    pw_session = item.funcargs.get("pw_session")

    if driver is not None:
        path = capture_failure_screenshot(driver, test_name, engine="selenium")
        _attach_png_to_allure(path)
    elif page is not None:
        path = capture_failure_screenshot(page, test_name, engine="playwright")
        _attach_png_to_allure(path)
    elif pw_session is not None:
        path = capture_failure_screenshot(pw_session.page, test_name, engine="playwright")
        _attach_png_to_allure(path)


def _attach_png_to_allure(path: Any) -> None:
    if path is None:
        return
    try:
        import allure

        with open(path, "rb") as handle:
            allure.attach(
                handle.read(),
                name=path.name,
                attachment_type=allure.attachment_type.PNG,
            )
    except Exception as exc:  # noqa: BLE001
        logger.debug("Could not attach screenshot to Allure: %s", exc)
