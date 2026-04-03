from __future__ import annotations

from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def open(self, base_url: str) -> None:
        self.page.goto(f"{base_url}/sign-in", wait_until="networkidle")
        self.page.wait_for_load_state("networkidle")

    def login(self, email: str, password: str) -> None:
        email_field = self.page.locator('input[name="email"], input[type="email"]').first
        password_field = self.page.locator('input[name="password"], input[type="password"]').first
        sign_in_button = self.page.get_by_role("button", name="Sign in")

        expect(email_field).to_be_visible()
        expect(password_field).to_be_visible()
        expect(sign_in_button).to_be_enabled()
        email_field.fill(email)
        password_field.fill(password)
        self.page.wait_for_timeout(500)
        sign_in_button.click()
        self.page.wait_for_url("**/organizations", timeout=30000)
        self.page.wait_for_load_state("networkidle")

    def assert_logged_in(self) -> None:
        assert "/organizations" in self.page.url

    def assert_login_form_visible(self) -> None:
        expect(self.page.get_by_role("button", name="Sign in")).to_be_visible()
