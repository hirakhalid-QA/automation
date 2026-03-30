from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Callable

from playwright.sync_api import Page, Response, TimeoutError as PlaywrightTimeoutError


@dataclass
class TestResult:
    name: str
    status: str
    details: str


def now_tag() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def record(results: list[TestResult], name: str, ok: bool, details: str = "") -> None:
    results.append(TestResult(name=name, status="PASS" if ok else "FAIL", details=details))


def slugify(text: str) -> str:
    lowered = text.lower().strip()
    lowered = re.sub(r"[^a-z0-9]+", "_", lowered)
    lowered = re.sub(r"_+", "_", lowered).strip("_")
    return lowered or "step"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_step_screenshot(page: Page, artifacts_dir: Path, step_index: int, step_name: str, status: str) -> Path:
    filename = f"{step_index:02d}_{slugify(step_name)}_{status.lower()}.png"
    file_path = artifacts_dir / filename
    page.screenshot(path=str(file_path), full_page=True)
    return file_path


def append_jsonl(file_path: Path, payload: dict) -> None:
    with file_path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(payload, ensure_ascii=True) + "\n")


def click_forgot_password(page: Page) -> None:
    page.get_by_role("link", name=re.compile("forgot password", re.I)).click()


def fill_sign_in(page: Page, email: str, password: str) -> None:
    page.get_by_role("textbox", name=re.compile("^Email:?$", re.I)).fill(email)
    page.get_by_role("textbox", name=re.compile("^Password:?$", re.I)).fill(password)


def click_sign_in(page: Page) -> None:
    page.get_by_role("button", name=re.compile("^Sign in$", re.I)).click()


def open_sign_in(page: Page, base_url: str) -> None:
    page.goto(f"{base_url}/sign-in", wait_until="domcontentloaded")


def open_forgot_password(page: Page, base_url: str) -> None:
    page.goto(f"{base_url}/forgot-password", wait_until="domcontentloaded")


def request_reset_email(page: Page, email: str) -> None:
    email_box = page.get_by_role("textbox", name=re.compile("^Email:?$", re.I))
    email_box.fill(email)
    page.get_by_role("button", name=re.compile("Send Update Password Link", re.I)).click()


def fill_reset_form(page: Page, new_password: str, confirm_password: str) -> None:
    page.get_by_role("textbox", name=re.compile("^New Password:?$", re.I)).fill(new_password)
    page.get_by_role("textbox", name=re.compile("^Confirm New Password:?$", re.I)).fill(confirm_password)


def submit_reset_form(page: Page) -> None:
    page.get_by_role("button", name=re.compile("^Reset Password$", re.I)).click()


def wait_for_post_response(
    page: Page,
    trigger_action: Callable[[], None],
    url_contains: str,
    timeout_ms: int = 15000,
) -> Response:
    with page.expect_response(
        lambda response: response.request.method == "POST" and url_contains in response.url,
        timeout=timeout_ms,
    ) as response_info:
        trigger_action()
    return response_info.value


def maybe_wait_for_post_response(
    page: Page,
    trigger_action: Callable[[], None],
    url_contains: str,
    timeout_ms: int = 4000,
) -> Response | None:
    try:
        with page.expect_response(
            lambda response: response.request.method == "POST" and url_contains in response.url,
            timeout=timeout_ms,
        ) as response_info:
            trigger_action()
        return response_info.value
    except PlaywrightTimeoutError:
        # Some negative validations are client-side only and send no request.
        return None


def response_brief(response: Response) -> str:
    body_preview = response.text()
    if len(body_preview) > 220:
        body_preview = body_preview[:220] + "..."
    return f"status={response.status}, url={response.url}, body={body_preview}"


def has_visible_text(page: Page, patterns: list[str], timeout_ms: int = 5000) -> tuple[bool, str]:
    for pattern in patterns:
        locator = page.get_by_text(re.compile(pattern, re.I))
        try:
            locator.first.wait_for(state="visible", timeout=timeout_ms)
            return True, pattern
        except PlaywrightTimeoutError:
            continue
    return False, ""


def safe_url_contains(page: Page, text: str, timeout_ms: int = 7000) -> bool:
    try:
        page.wait_for_url(f"**{text}**", timeout=timeout_ms)
        return True
    except PlaywrightTimeoutError:
        return text in page.url

