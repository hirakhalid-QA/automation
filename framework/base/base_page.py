from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def by_role(self, role: str, name: str) -> Locator:
        return self.page.get_by_role(role, name=name)

