from __future__ import annotations

from core.config import Settings
from pages.root.organizations_page import OrganizationsPage
from utils.data_factory import (
    build_org_edit_payload,
    build_org_payload,
    generate_org_head_emails,
)


def test_root_can_create_organization(root_page, settings: Settings) -> None:
    organizations_page = OrganizationsPage(root_page)
    payload = build_org_payload(settings)

    organizations_page.open(settings.base_url)
    selected_email = organizations_page.create_organization(
        payload=payload,
        candidate_emails=generate_org_head_emails(settings),
    )

    organizations_page.open(settings.base_url)
    organizations_page.search_organization(payload.name)
    organizations_page.assert_organization_visible(payload.name)
    assert selected_email.endswith(f"@{settings.org_head_email_domain}")

def test_root_can_edit_organization_modals(root_page, settings: Settings) -> None:
    organizations_page = OrganizationsPage(root_page)
    create_payload = build_org_payload(settings)
    edit_payload = build_org_edit_payload()

    organizations_page.open(settings.base_url)
    selected_email = organizations_page.create_organization(
        payload=create_payload,
        candidate_emails=generate_org_head_emails(settings),
    )

    organizations_page.open(settings.base_url)
    organizations_page.search_organization(create_payload.name)
    organizations_page.edit_notes(create_payload.name, edit_payload.notes)
    organizations_page.edit_info(create_payload.name, edit_payload)

    organizations_page.search_organization(edit_payload.name)
    next_email = _next_email(selected_email, settings)
    organizations_page.edit_head_email(edit_payload.name, next_email)
    organizations_page.edit_storage(edit_payload.name, edit_payload.storage_quota, edit_payload.storage_unit)
    organizations_page.edit_ai_models(
        edit_payload.name,
        edit_payload.native_model_label,
        edit_payload.llm_label,
    )
    organizations_page.grant_tokens(edit_payload.name, edit_payload.tokens_to_grant)
    organizations_page.edit_quotas(
        edit_payload.name,
        edit_payload.users_quota,
        edit_payload.spaces_quota,
    )

    organizations_page.search_organization(edit_payload.name)
    organizations_page.assert_organization_visible(edit_payload.name)


def _next_email(current_email: str, settings: Settings) -> str:
    emails = generate_org_head_emails(settings)
    current_index = emails.index(current_email)
    if current_index + 1 >= len(emails):
        raise AssertionError("No next org-head email left in configured range.")
    return emails[current_index + 1]

