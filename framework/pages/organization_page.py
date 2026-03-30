from framework.base.base_page import BasePage
from playwright.sync_api import Page


class OrganizationPage(BasePage):
    def __init__(self, page: Page, actions_trigger: str) -> None:
        super().__init__(page)
        self.actions_trigger = actions_trigger

    def open_actions_menu(self) -> None:
        self.page.locator(self.actions_trigger).click()

    def edit_organization_notes(self, notes: str) -> None:
        self.open_actions_menu()
        self.by_role("menuitem", "Edit Organization Notes").click()
        self.by_role("textbox", "Notes: (optional) Additional").fill(notes)
        self.by_role("button", "Save Changes").click()

    def edit_organization_name(self, name: str) -> None:
        self.open_actions_menu()
        self.by_role("menuitem", "Edit Organization Info").click()
        self.by_role("textbox", "Organization Name Special").fill(name)
        self.by_role("button", "Save Changes").click()

