# Enterprise Test Automation Framework

Production-style UI test automation framework for [Sauce Demo](https://www.saucedemo.com/), built with **Python 3.12+**, **Pytest**, **Selenium**, **Playwright**, **Page Object Model**, **Allure**, and **GitHub Actions**.

Designed for GitHub portfolios and SDET / Solution Engineer interviews: clean architecture, explicit waits, cross-browser execution, parallel runs, retries, and rich reporting.

---

## Project overview

| Goal | Approach |
|------|----------|
| Maintainable UI automation | Page Object Model + separated locators |
| Stable synchronization | Explicit waits only (`implicit_wait = 0`) |
| Multi-engine demo | Selenium (primary) + Playwright (parity smoke) |
| CI-ready evidence | HTML + Allure reports, screenshots on failure, logs |
| Configurable runs | `.env` + CLI (`--browser`, `--headless`, `--engine`) |

### Automated coverage

- Login (valid)
- Invalid login (wrong credentials / locked user) — data-driven JSON
- Logout
- Product listing
- Product sorting (A–Z, Z–A, price low/high)
- Add to cart / remove from cart
- Checkout + complete purchase
- Assertions: URL, title, errors, cart count, product names/prices, checkout success

---

## Folder structure

```text
Enterprise-Test-Automation-Framework/
├── tests/                  # Pytest suites (smoke, ui, regression, api)
├── pages/                  # Page Objects (Selenium + Playwright)
├── locators/               # Centralized selectors
├── utils/                  # Logger, waits, browser, screenshots, files, reports
├── config/                 # Settings, paths, browser config
├── testdata/               # JSON data-driven inputs
├── reports/                # HTML + Allure outputs (generated)
├── screenshots/            # Failure screenshots (generated)
├── logs/                   # Timestamped run logs (generated)
├── resources/              # Allure categories and static assets
├── .github/workflows/      # CI pipeline
├── conftest.py             # Fixtures, CLI, failure hooks
├── pytest.ini              # Markers, defaults, reruns
├── requirements.txt
└── .env.example
```

---

## Technologies used

- Python 3.12+
- Selenium 4 + webdriver-manager
- Playwright
- Pytest, pytest-xdist, pytest-html, pytest-rerunfailures
- Allure (allure-pytest)
- Faker, python-dotenv, requests
- GitHub Actions

---

## Installation

```bash
cd Enterprise-Test-Automation-Framework

python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

# Playwright browsers (required for --engine=playwright)
playwright install
# or: playwright install chromium

cp .env.example .env               # optional; defaults already provided
```

---

## Running tests

### Defaults (Selenium + Chrome from `.env`)

```bash
pytest
```

### By tag

```bash
pytest -m smoke
pytest -m regression
pytest -m sanity
pytest -m "smoke and login"
pytest -m "cart and not playwright"
```

### Cross-browser / headless / CLI overrides

```bash
pytest --browser=chrome --headless
pytest --browser=edge --headed
pytest --browser=firefox -m smoke
pytest --app-url=https://www.saucedemo.com/
```

### Parallel execution

```bash
pytest -n auto
pytest -n 4 -m regression
```

### Retry failed tests

Configured in `pytest.ini` (`--reruns=1`). Override:

```bash
pytest --reruns=2 --reruns-delay=1
```

---

## Running Selenium

```bash
pytest --engine=selenium --browser=chrome --headless -m "(smoke or regression) and not playwright"
```

Or via environment:

```bash
export AUTOMATION_ENGINE=selenium
export BROWSER=chrome
export HEADLESS=true
pytest -m smoke
```

---

## Running Playwright

```bash
playwright install chromium
pytest tests/ui/test_playwright_smoke.py --engine=playwright --browser=chrome --headless
```

Or:

```bash
pytest -m playwright --engine=playwright --headless
```

> Selenium fixtures skip when `AUTOMATION_ENGINE=playwright`, and Playwright fixtures skip when the engine is Selenium. Run engines in separate commands or CI jobs.

---

## GitHub Actions

Workflow: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

On push/PR to `main` / `master` / `develop` (and manual `workflow_dispatch`):

1. Install Python 3.12 + dependencies  
2. Run Selenium smoke/regression (Chrome headless, `pytest-xdist`)  
3. Generate pytest-HTML + Allure report  
4. Upload HTML, Allure, screenshots, and logs as artifacts  
5. Parallel job: Playwright Chromium smoke tests + HTML artifact  

---

## Screenshots

- On failure, `conftest.py` captures PNG under `screenshots/`
- Naming: `FAIL_<test_name>_<timestamp>.png`
- PNG is also attached to Allure when available
- Toggle: `SCREENSHOT_ON_FAILURE=true|false` in `.env`

---

## Reports

| Report | Location | How |
|--------|----------|-----|
| pytest-html | `reports/report_*.html` / `reports/report.html` | Generated automatically |
| Allure results | `reports/allure-results/` | `--alluredir` in `pytest.ini` |
| Allure HTML | local via CLI | see below |
| Logs | `logs/test_run_*.log` | Logger utility |
| Run manifest | `reports/run_manifest_*.json` | Written at session start |

### View Allure locally

```bash
# macOS (Homebrew): brew install allure
allure serve reports/allure-results
# or
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

---

## Architecture notes (interview-ready)

- **SOLID / SRP**: locators, pages, utils, tests each own one concern  
- **BasePage / BaseTest**: shared interactions and assertions  
- **Config as env**: 12-factor friendly for local + CI  
- **Explicit waits only**: enterprise-stable synchronization  
- **Data-driven JSON**: invalid login + sorting + product fixtures  

---

## Future enhancements

- API contract suite with `requests` + schema validation  
- BrowserStack / Sauce Labs remote WebDriver  
- Visual regression (Playwright screenshots / Percy)  
- Accessibility checks (axe-core)  
- TestRail / Jira Xray publishing  
- Dockerized runner image  
- Allure history trend hosting (GitHub Pages)

---

## License

MIT (or your preferred license) — update before publishing publicly.
