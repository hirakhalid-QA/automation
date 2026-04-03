from __future__ import annotations

from pages.auth.login_page import LoginPage


def test_root_login_success(page, settings) -> None:
    login_page = LoginPage(page)
    login_page.open(settings.base_url)
    login_page.assert_login_form_visible()
    login_page.login(settings.root_email, settings.root_password)
    login_page.assert_logged_in()
