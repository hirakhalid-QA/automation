from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage
from utils.data_factory import OrganizationEditPayload, OrganizationPayload


class OrganizationsPage(BasePage):
    def open(self, base_url: str) -> None:
        self.page.goto(f"{base_url}/organizations", wait_until="domcontentloaded")
        expect(self.page.get_by_role("button", name="Create New")).to_be_visible()

    def open_create_form(self) -> None:
        self.click_button("Create New")
        expect(self.page.get_by_role("heading", name="Create New Organization")).to_be_visible()

    def create_organization(self, payload: OrganizationPayload, candidate_emails: list[str]) -> str:
        self.open_create_form()
        self._fill_step_one(payload)
        self._go_next()

        selected_email = self._complete_step_two_with_retry(payload, candidate_emails)
        self._fill_step_three(payload)
        self._go_next()
        self._submit_with_repair(payload, selected_email)
        return selected_email

    def search_organization(self, name: str) -> None:
        self.page.get_by_placeholder("Search organizations...").fill(name)

    def open_card_menu(self, name: str) -> None:
        card = self._organization_card(name)
        card.get_by_role("button").last.click()

    def edit_notes(self, org_name: str, notes: str) -> None:
        self.open_card_menu(org_name)
        self.page.get_by_text("Edit Organization Notes").click()
        self.page.locator("textarea").fill(notes)
        self.click_button("Save Changes")

    def get_first_organization_name(self) -> str:
        cards = self.page.locator("div").filter(has_text="Org. Manager:")
        first_card = cards.first
        expect(first_card).to_be_visible()
        lines = [line.strip() for line in first_card.inner_text().splitlines() if line.strip()]
        if not lines:
            raise AssertionError("No organization card text found on organizations page.")
        return lines[0]

    def assert_notes_persisted(self, org_name: str, expected_notes: str) -> None:
        self.open_card_menu(org_name)
        self.page.get_by_text("Edit Organization Notes").click()
        actual_notes = self.page.locator("textarea").input_value()
        assert actual_notes == expected_notes
        self.click_button("Cancel")

    def edit_info(self, org_name: str, payload: OrganizationEditPayload) -> None:
        self.open_card_menu(org_name)
        self.page.get_by_text("Edit Organization Info").click()
        self.fill_label("Organization Name", payload.name)
        self.fill_label("Organization Abbreviation", payload.abbreviation)
        self.fill_label("Organization Subtitle", payload.subtitle)
        self.click_button("Save Changes")

    def edit_head_email(self, org_name: str, new_email: str) -> None:
        self.open_card_menu(org_name)
        self.page.get_by_text("Edit Organization Head Email").click()
        self.fill_label("New Email Address", new_email)
        self.click_button("Update Email")

    def edit_storage(self, org_name: str, storage_quota: int, unit: str) -> None:
        self.open_card_menu(org_name)
        self.page.get_by_text("Edit Storage Quota").click()
        self.fill_label("Organization Storage Quota", str(storage_quota))
        self.page.locator("select").last.select_option(label=unit)
        self.click_button("Update Storage")

    def edit_ai_models(self, org_name: str, native_model_label: str, llm_label: str) -> None:
        self.open_card_menu(org_name)
        self.page.get_by_text("Edit AI Models").click()
        self._check_labeled_option(native_model_label)
        self._check_labeled_option(llm_label)
        self.click_button("Update AI Models")

    def grant_tokens(self, org_name: str, tokens_to_grant: int) -> None:
        self.open_card_menu(org_name)
        self.page.get_by_text("Edit AI Tokens").click()
        self.fill_placeholder("Enter number of tokens to add", str(tokens_to_grant))
        self.click_button("Grant Tokens")

    def edit_quotas(self, org_name: str, users_quota: int, spaces_quota: int) -> None:
        self.open_card_menu(org_name)
        self.page.get_by_text("Edit User & Space Quota").click()
        self.fill_label("Organization Users Quota", str(users_quota))
        self.fill_label("Organization Space Quota", str(spaces_quota))
        self.click_button("Update Quotas")

    def assert_organization_visible(self, name: str) -> None:
        expect(self._organization_card(name)).to_be_visible()

    def _organization_card(self, name: str) -> Locator:
        return self.page.locator("div").filter(has_text=name).nth(0)

    def _fill_step_one(self, payload: OrganizationPayload) -> None:
        self.fill_placeholder("Enter organization name", payload.name)
        self.fill_placeholder("Enter organization abbreviation", payload.abbreviation)
        self.fill_placeholder("Enter organization subtitle", payload.subtitle)
        self.page.locator("textarea").fill(payload.notes)

    def _complete_step_two_with_retry(self, payload: OrganizationPayload, candidate_emails: list[str]) -> str:
        for email in candidate_emails:
            self.fill_label("First Name", payload.head_first_name)
            self.fill_label("Last Name", payload.head_last_name)
            self.fill_label("Email Address", email)
            self._go_next()
            if not self._step_has_email_validation_error():
                return email
        raise AssertionError("No available org-head email found in configured +1..+99 range.")

    def _fill_step_three(self, payload: OrganizationPayload) -> None:
        self.fill_label("Organization Users Quota", str(payload.users_quota))
        self.fill_label("Organization Space Quota", str(payload.spaces_quota))
        self.fill_label("Organization Storage Quota", str(payload.storage_quota))
        self.page.locator("select").last.select_option(label=payload.storage_unit)
        self._ensure_create_models_selected()
        self.fill_label("Tokens Balance", str(payload.tokens_balance))

    def _submit_with_repair(self, payload: OrganizationPayload, selected_email: str) -> None:
        self.click_button("Submit")
        if self.page.get_by_text("Validation Error").count():
            self.click_button("Previous")
            self._fill_step_three(payload)
            self._go_next()
            self.click_button("Submit")
            if self.page.get_by_text("Validation Error").count():
                self.click_button("Previous")
                self.click_button("Previous")
                self._complete_step_two_with_retry(payload, [selected_email])
                self._fill_step_three(payload)
                self._go_next()
                self.click_button("Submit")

    def _go_next(self) -> None:
        self.click_button("Next")

    def _step_has_email_validation_error(self) -> bool:
        return self.page.get_by_text("valid email address", exact=False).count() > 0 or (
            self.page.get_by_text("already", exact=False).count() > 0
        )

    def _check_labeled_option(self, label: str) -> None:
        target = self.page.get_by_text(label, exact=False)
        if target.count():
            container = target.first.locator("xpath=ancestor::*[self::label or self::div][1]")
            checkbox = container.locator('[role="checkbox"]').first
            if checkbox.count() and checkbox.get_attribute("aria-checked") != "true":
                checkbox.click()

    def _ensure_create_models_selected(self) -> None:
        checkboxes = self.page.get_by_role("checkbox")
        native_checkbox = checkboxes.nth(0)
        llm_checkbox = checkboxes.nth(1)

        if native_checkbox.count() and native_checkbox.get_attribute("aria-checked") != "true":
            native_checkbox.scroll_into_view_if_needed()
            native_checkbox.click(force=True)
            self.page.wait_for_timeout(300)

        if llm_checkbox.count() and llm_checkbox.get_attribute("aria-checked") != "true":
            llm_checkbox.scroll_into_view_if_needed()
            llm_checkbox.click(force=True)
            self.page.wait_for_timeout(300)
