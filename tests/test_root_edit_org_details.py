from playwright.sync_api import Page

from framework.pages.login_page import LoginPage
from framework.pages.organization_page import OrganizationPage
from projects.project_config import (
    BASE_URL,
    ORG_ACTIONS_TRIGGER,
    ORG_UPDATE_DATA,
    ROOT_USER,
)


def test_root_can_edit_organization_details(page: Page) -> None:
    login_page = LoginPage(page)
    organization_page = OrganizationPage(page, actions_trigger=ORG_ACTIONS_TRIGGER)

    login_page.goto_sign_in(BASE_URL)
    login_page.login_as_root(email=ROOT_USER.email, password=ROOT_USER.password)

    organization_page.edit_organization_notes(notes=ORG_UPDATE_DATA.notes)
    organization_page.edit_organization_name(name=ORG_UPDATE_DATA.organization_name)

