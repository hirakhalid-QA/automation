from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def click_button(self, name: str) -> None:
        self.page.get_by_role("button", name=name).click()

    def fill_placeholder(self, placeholder: str, value: str) -> None:
        self.page.get_by_placeholder(placeholder).fill(value)

    def fill_label(self, label: str, value: str) -> None:
        self.page.get_by_label(label, exact=False).fill(value)

    def expect_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(f"**{fragment}**")

    def wait_for_toast(self) -> Locator:
        validation_toast = self.page.get_by_text("Validation Error", exact=False)
        if validation_toast.count():
            validation_toast.last.wait_for(timeout=5_000)
            return validation_toast.last

        success_toast = self.page.locator('[role="status"], [data-sonner-toast]').last
        success_toast.wait_for(timeout=5_000)
        return success_toast

    def text_exists(self, text: str) -> bool:
        return self.page.get_by_text(text, exact=False).count() > 0

    def close_modal(self) -> None:
        close_button = self.page.get_by_role("button", name="Close")
        if close_button.count():
            close_button.click()
            return
        self.page.keyboard.press("Escape")
