"""Cross-browser factory for Selenium and Playwright."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config.browser_config import validate_browser, validate_engine
from config.settings import Settings, get_settings
from utils.logger_util import get_logger

logger = get_logger(__name__)

BrowserName = Literal["chrome", "edge", "firefox"]


def _apply_window(driver: WebDriver, settings: Settings) -> None:
    driver.set_window_size(settings.window_width, settings.window_height)
    driver.set_page_load_timeout(settings.page_load_timeout)
    # Explicit waits only — never rely on implicit waits in enterprise suites.
    driver.implicitly_wait(settings.implicit_wait)


def _chrome_options(settings: Settings) -> ChromeOptions:
    options = ChromeOptions()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        f"--window-size={settings.window_width},{settings.window_height}"
    )
    options.add_argument("--disable-notifications")
    return options


def _edge_options(settings: Settings) -> EdgeOptions:
    options = EdgeOptions()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        f"--window-size={settings.window_width},{settings.window_height}"
    )
    return options


def _firefox_options(settings: Settings) -> FirefoxOptions:
    options = FirefoxOptions()
    options.headless = settings.headless  # type: ignore[attr-defined]
    if settings.headless:
        options.add_argument("-headless")
    return options


def create_selenium_driver(
    browser: str | None = None,
    settings: Settings | None = None,
) -> WebDriver:
    """
    Create a Selenium WebDriver for Chrome, Edge, or Firefox.

    Drivers are resolved via ``webdriver-manager`` for portable local/CI use.
    """
    cfg = settings or get_settings()
    name = validate_browser(browser or cfg.browser)
    logger.info(
        "Launching Selenium | browser=%s headless=%s", name, cfg.headless
    )

    if name == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        driver: WebDriver = webdriver.Chrome(
            service=service, options=_chrome_options(cfg)
        )
    elif name == "edge":
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=_edge_options(cfg))
    else:
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=_firefox_options(cfg))

    _apply_window(driver, cfg)
    return driver


def quit_selenium_driver(driver: WebDriver | None) -> None:
    """Safely quit a Selenium driver."""
    if driver is None:
        return
    try:
        driver.quit()
        logger.info("Selenium driver quit successfully.")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Error while quitting Selenium driver: %s", exc)


@dataclass
class PlaywrightSession:
    """Holds Playwright runtime objects for fixture teardown."""

    playwright: Any
    browser: Any
    context: Any
    page: Any

    def close(self) -> None:
        """Tear down page → context → browser → Playwright runtime (``stop()``)."""
        try:
            if self.page is not None:
                self.page.close()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Error closing Playwright page: %s", exc)

        for closer, label in (
            (self.context, "context"),
            (self.browser, "browser"),
        ):
            try:
                closer.close()
            except Exception as exc:  # noqa: BLE001
                logger.warning("Error closing Playwright %s: %s", label, exc)

        # Sync API must call stop() — close() leaves an asyncio loop alive and
        # breaks the next test with "Sync API inside the asyncio loop".
        try:
            self.playwright.stop()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Error stopping Playwright runtime: %s", exc)

        logger.info("Playwright session closed.")


def create_playwright_session(
    browser: str | None = None,
    settings: Settings | None = None,
) -> PlaywrightSession:
    """
    Launch a Playwright browser session with a default context and page.

    Callers (fixtures) must invoke ``session.close()`` in teardown.
    """
    from playwright.sync_api import sync_playwright

    cfg = settings or get_settings()
    validate_engine("playwright")
    name = validate_browser(browser or cfg.browser)
    logger.info(
        "Launching Playwright | browser=%s headless=%s", name, cfg.headless
    )

    playwright = sync_playwright().start()
    launcher = {
        "chrome": playwright.chromium,
        "edge": playwright.chromium,
        "firefox": playwright.firefox,
    }[name]

    launch_kwargs: dict[str, Any] = {"headless": cfg.headless}
    if name == "edge":
        launch_kwargs["channel"] = "msedge"

    browser_obj = launcher.launch(**launch_kwargs)
    context = browser_obj.new_context(
        viewport={"width": cfg.window_width, "height": cfg.window_height},
        base_url=cfg.base_url,
    )
    page = context.new_page()
    page.set_default_timeout(cfg.explicit_wait * 1000)

    return PlaywrightSession(
        playwright=playwright,
        browser=browser_obj,
        context=context,
        page=page,
    )


class BrowserFactory:
    """
    Facade for engine-aware browser creation (SOLID: DIP-friendly entrypoint).

    Prefer fixtures calling ``create_selenium_driver`` /
    ``create_playwright_session`` directly; this class is useful when tests
    switch engines via configuration.
    """

    @staticmethod
    def create(settings: Settings | None = None) -> WebDriver | PlaywrightSession:
        cfg = settings or get_settings()
        engine = validate_engine(cfg.automation_engine)
        if engine == "playwright":
            return create_playwright_session(settings=cfg)
        return create_selenium_driver(settings=cfg)
