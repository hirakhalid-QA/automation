from framework.base.base_page import BasePage


class LoginPage(BasePage):
    def goto_sign_in(self, base_url: str) -> None:
        self.page.goto(f"{base_url}/sign-in")

    def login_as_root(self, email: str, password: str) -> None:
        self.by_role("textbox", "Email:").fill(email)
        self.by_role("textbox", "Password:").fill(password)
        self.by_role("button", "Sign in").click()
        self.page.wait_for_load_state("networkidle")

