from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from core.config import Settings


def unique_suffix() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


@dataclass(frozen=True)
class OrganizationPayload:
    name: str
    abbreviation: str
    subtitle: str
    notes: str
    head_first_name: str
    head_last_name: str
    head_password: str
    users_quota: int
    spaces_quota: int
    storage_quota: int
    storage_unit: str
    tokens_balance: int
    native_model_label: str
    llm_label: str


@dataclass(frozen=True)
class OrganizationEditPayload:
    notes: str
    name: str
    abbreviation: str
    subtitle: str
    storage_quota: int
    storage_unit: str
    tokens_to_grant: int
    users_quota: int
    spaces_quota: int
    new_head_email: str
    native_model_label: str
    llm_label: str


def build_org_payload(settings: Settings) -> OrganizationPayload:
    suffix = unique_suffix()
    short = suffix[-6:]
    return OrganizationPayload(
        name=f"Auto Org {suffix}",
        abbreviation=f"AO{short[-4:]}",
        subtitle=f"Auto subtitle {short}",
        notes=f"Automation notes {suffix}",
        head_first_name="Hira",
        head_last_name=f"Auto{short}",
        head_password=settings.org_head_password,
        users_quota=10,
        spaces_quota=5,
        storage_quota=5,
        storage_unit="GB",
        tokens_balance=1000,
        native_model_label="Optical Character Recognition - 1",
        llm_label="GPT - 4.1",
    )


def build_org_edit_payload() -> OrganizationEditPayload:
    suffix = unique_suffix()
    short = suffix[-6:]
    return OrganizationEditPayload(
        notes=f"Updated notes {suffix}",
        name=f"Updated Org {suffix}",
        abbreviation=f"UP{short[-4:]}",
        subtitle=f"Updated subtitle {short}",
        storage_quota=7,
        storage_unit="GB",
        tokens_to_grant=250,
        users_quota=12,
        spaces_quota=6,
        new_head_email="",
        native_model_label="Optical Character Recognition - 1",
        llm_label="GPT - 4.1",
    )


def generate_org_head_emails(settings: Settings) -> list[str]:
    emails: list[str] = []
    start_suffix = max(settings.org_head_email_min_suffix, 10)
    for suffix in range(start_suffix, settings.org_head_email_max_suffix + 1):
        emails.append(
            f"{settings.org_head_email_prefix}+{suffix}@{settings.org_head_email_domain}"
        )
    return emails
