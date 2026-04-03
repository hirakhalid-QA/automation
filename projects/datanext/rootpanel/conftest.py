from __future__ import annotations

from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Error, Page, Playwright, sync_playwright

from core.config import Settings, load_settings
from pages.auth.login_page import LoginPage


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Browser:
    browser = playwright_instance.chromium.launch(
        headless=settings.headless,
        slow_mo=settings.slow_mo,
    )
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser, settings: Settings) -> BrowserContext:
    context = browser.new_context(ignore_https_errors=True)
    context.set_default_timeout(settings.timeout_ms)
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page


@pytest.fixture()
def root_page(page: Page, settings: Settings) -> Page:
    login_page = LoginPage(page)
    login_page.open(settings.base_url)
    login_page.login(settings.root_email, settings.root_password)
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return

    page = item.funcargs.get("page") or item.funcargs.get("root_page")
    if page is None:
        return

    artifacts_dir = Path(__file__).resolve().parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    screenshot = artifacts_dir / f"{item.name}.png"
    try:
        page.screenshot(path=str(screenshot), full_page=True)
    except Error:
        return
