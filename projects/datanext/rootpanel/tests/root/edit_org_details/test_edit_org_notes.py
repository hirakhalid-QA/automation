from __future__ import annotations

from core.config import Settings
from pages.root.organizations_page import OrganizationsPage
from utils.data_factory import build_org_edit_payload


def test_root_can_edit_organization_notes(root_page, settings: Settings) -> None:
    organizations_page = OrganizationsPage(root_page)
    edit_payload = build_org_edit_payload()

    organizations_page.open(settings.base_url)
    org_name = organizations_page.get_first_organization_name()
    organizations_page.edit_notes(org_name, edit_payload.notes)
    organizations_page.assert_notes_persisted(org_name, edit_payload.notes)
