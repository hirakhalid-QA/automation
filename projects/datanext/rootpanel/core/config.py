from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


@dataclass(frozen=True)
class Settings:
    base_url: str
    root_email: str
    root_password: str
    org_head_email_prefix: str
    org_head_email_domain: str
    org_head_email_min_suffix: int
    org_head_email_max_suffix: int
    org_head_password: str
    headless: bool
    slow_mo: int
    timeout_ms: int


def load_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[1]
    load_dotenv(project_root / ".env")

    return Settings(
        base_url=os.getenv("BASE_URL", "https://root.fordata.ai"),
        root_email=os.getenv("ROOT_EMAIL", "datanextroot@betacodespk.com"),
        root_password=os.getenv("ROOT_PASSWORD", "datanext@26"),
        org_head_email_prefix=os.getenv("ORG_HEAD_EMAIL_PREFIX", "hira.khalid"),
        org_head_email_domain=os.getenv("ORG_HEAD_EMAIL_DOMAIN", "betacodespk.com"),
        org_head_email_min_suffix=int(os.getenv("ORG_HEAD_EMAIL_MIN_SUFFIX", "1")),
        org_head_email_max_suffix=int(os.getenv("ORG_HEAD_EMAIL_MAX_SUFFIX", "99")),
        org_head_password=os.getenv("ORG_HEAD_PASSWORD", "Forbmax@23"),
        headless=_as_bool(os.getenv("HEADLESS", "false")),
        slow_mo=int(os.getenv("SLOW_MO", "100")),
        timeout_ms=int(os.getenv("TIMEOUT_MS", "15000")),
    )
