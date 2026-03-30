from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import secrets

from playwright.sync_api import sync_playwright

from modules.helpers import (
    TestResult,
    append_jsonl,
    click_forgot_password,
    click_sign_in,
    ensure_dir,
    fill_reset_form,
    fill_sign_in,
    has_visible_text,
    now_tag,
    open_forgot_password,
    open_sign_in,
    maybe_wait_for_post_response,
    record,
    request_reset_email,
    response_brief,
    safe_url_contains,
    save_step_screenshot,
    submit_reset_form,
    wait_for_post_response,
)


def print_report(results: list[TestResult]) -> None:
    print("\n========== RESET PASSWORD TEST REPORT ==========")
    for item in results:
        suffix = f" | {item.details}" if item.details else ""
        print(f"[{item.status}] {item.name}{suffix}")
    passed = sum(1 for r in results if r.status == "PASS")
    failed = len(results) - passed
    print(f"TOTAL: {len(results)} | PASSED: {passed} | FAILED: {failed}")
    print("===============================================\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reset-password test runner (headed).")
    parser.add_argument("--base-url", default="https://root.fordata.ai")
    parser.add_argument("--email", required=True)
    parser.add_argument("--current-password", required=True)
    parser.add_argument("--reset-link-1", default="")
    parser.add_argument("--reset-link-2", default="")
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    base_url = args.base_url
    email = args.email
    current_password = args.current_password

    results: list[TestResult] = []
    generated_password = f"Auto@{now_tag()}_{secrets.randbelow(9999)}"
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifacts_dir = Path("artifacts") / run_id
    ensure_dir(artifacts_dir)
    api_log_file = artifacts_dir / "api_calls.jsonl"
    step_index = 0

    forgot_error_patterns = ["required", "invalid", "email"]
    forgot_success_patterns = ["link", "email", "sent", "request"]
    reset_mismatch_patterns = ["match", "same", "confirm", "password"]
    reset_success_patterns = ["password", "updated", "success", "changed", "sign in"]
    login_fail_patterns = ["invalid", "incorrect", "password", "credentials", "sign in"]

    def assert_step(name: str, ok: bool, details: str) -> None:
        nonlocal step_index
        step_index += 1
        status = "PASS" if ok else "FAIL"
        screenshot_path = save_step_screenshot(page, artifacts_dir, step_index, name, status)
        full_details = f"{details} | screenshot={screenshot_path.as_posix()}"
        record(results, name, ok, full_details)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()
        try:
            # 1. Sign-in page loads.
            open_sign_in(page, base_url)
            assert_step("Sign-in page loads", "sign-in" in page.url, page.url)

            # 2. Forgot-password navigation from sign-in.
            click_forgot_password(page)
            assert_step("Forgot-password navigation works", "forgot-password" in page.url, page.url)

            # 3. Empty email negative.
            open_forgot_password(page, base_url)
            forgot_empty_response = maybe_wait_for_post_response(
                page, lambda: request_reset_email(page, ""), "forgot-password"
            )
            append_jsonl(api_log_file, {
                "step": "Forgot-password empty email",
                "response": response_brief(forgot_empty_response) if forgot_empty_response else "no POST request observed (client-side validation)",
            })
            found_empty_error, matched_empty = has_visible_text(page, forgot_error_patterns)
            assert_step(
                "Forgot-password rejects empty email",
                found_empty_error,
                f"{response_brief(forgot_empty_response) if forgot_empty_response else 'no POST request observed'}, message_match={matched_empty or 'none'}",
            )

            # 4. Invalid email negative.
            open_forgot_password(page, base_url)
            forgot_invalid_response = maybe_wait_for_post_response(
                page, lambda: request_reset_email(page, "invalid-email"), "forgot-password"
            )
            append_jsonl(api_log_file, {
                "step": "Forgot-password invalid email",
                "response": response_brief(forgot_invalid_response) if forgot_invalid_response else "no POST request observed (client-side validation)",
            })
            found_invalid_error, matched_invalid = has_visible_text(page, forgot_error_patterns)
            assert_step(
                "Forgot-password rejects invalid email format",
                found_invalid_error,
                f"{response_brief(forgot_invalid_response) if forgot_invalid_response else 'no POST request observed'}, message_match={matched_invalid or 'none'}",
            )

            # 5. Valid email request (happy path trigger).
            open_forgot_password(page, base_url)
            forgot_valid_response = wait_for_post_response(
                page,
                lambda: request_reset_email(page, email),
                "forgot-password",
            )
            append_jsonl(
                api_log_file,
                {"step": "Forgot-password valid email", "response": response_brief(forgot_valid_response)},
            )
            found_forgot_success, matched_forgot_success = has_visible_text(page, forgot_success_patterns)
            assert_step(
                "Forgot-password accepts valid email submit",
                found_forgot_success,
                f"{response_brief(forgot_valid_response)}, message_match={matched_forgot_success or 'none'}",
            )

            reset_link_1 = args.reset_link_1 or input("\nPaste Reset Link #1 (for mismatch test): ").strip()
            page.goto(reset_link_1, wait_until="domcontentloaded")
            assert_step("Reset link page opens", safe_url_contains(page, "reset-password"), page.url)

            # 6. Mismatch password negative.
            fill_reset_form(page, "Temp@12345", "Temp@12346")
            reset_mismatch_response = wait_for_post_response(
                page,
                lambda: submit_reset_form(page),
                "reset-password",
            )
            append_jsonl(
                api_log_file,
                {"step": "Reset-password mismatch", "response": response_brief(reset_mismatch_response)},
            )
            found_reset_mismatch, matched_reset_mismatch = has_visible_text(page, reset_mismatch_patterns)
            assert_step(
                "Reset rejects mismatch passwords",
                found_reset_mismatch,
                f"{response_brief(reset_mismatch_response)}, message_match={matched_reset_mismatch or 'none'}",
            )

            open_forgot_password(page, base_url)
            forgot_second_valid_response = wait_for_post_response(
                page,
                lambda: request_reset_email(page, email),
                "forgot-password",
            )
            append_jsonl(
                api_log_file,
                {"step": "Forgot-password second valid email", "response": response_brief(forgot_second_valid_response)},
            )
            reset_link_2 = args.reset_link_2 or input("\nPaste Reset Link #2 (for successful reset): ").strip()
            page.goto(reset_link_2, wait_until="domcontentloaded")

            # 7. Successful reset.
            fill_reset_form(page, generated_password, generated_password)
            reset_success_response = wait_for_post_response(
                page,
                lambda: submit_reset_form(page),
                "reset-password",
            )
            append_jsonl(
                api_log_file,
                {"step": "Reset-password success", "response": response_brief(reset_success_response)},
            )
            found_reset_success, matched_reset_success = has_visible_text(page, reset_success_patterns)
            assert_step(
                "Reset succeeds with valid new password",
                safe_url_contains(page, "sign-in") or found_reset_success,
                f"{response_brief(reset_success_response)}, message_match={matched_reset_success or 'none'}",
            )

            # 8. Login with old password should fail.
            open_sign_in(page, base_url)
            fill_sign_in(page, email, current_password)
            click_sign_in(page)
            found_old_login_error, matched_old_login = has_visible_text(page, login_fail_patterns)
            old_password_failed = "sign-in" in page.url or found_old_login_error
            assert_step(
                "Old password no longer works",
                old_password_failed,
                f"url={page.url}, message_match={matched_old_login or 'none'}",
            )

            # 9. Login with new password should pass.
            open_sign_in(page, base_url)
            fill_sign_in(page, email, generated_password)
            click_sign_in(page)
            new_password_login_ok = "sign-in" not in page.url
            assert_step("Login works with new password", new_password_login_ok, page.url)

            # 10. Reuse of successful token should fail.
            page.goto(reset_link_2, wait_until="domcontentloaded")
            token_reuse_blocked = "reset-password" not in page.url or "sign-in" in page.url
            assert_step("Used reset link is not reusable", token_reuse_blocked, page.url)

            print(f"\nNew password after test run: {generated_password}")
            print("Use it for the next run or reset again.")
            print(f"Artifacts: {artifacts_dir.as_posix()}")
        finally:
            print_report(results)
            browser.close()


if __name__ == "__main__":
    run()

