from dataclasses import dataclass
import os


@dataclass(frozen=True)
class RootUser:
    email: str
    password: str


@dataclass(frozen=True)
class OrgUpdateData:
    notes: str
    organization_name: str


BASE_URL = os.getenv("ROOT_BASE_URL", "https://root.fordata.ai")

ROOT_USER = RootUser(
    email=os.getenv("ROOT_EMAIL", "datanextroot@betacodespk.com"),
    password=os.getenv("ROOT_PASSWORD", "datanext@26"),
)

ORG_UPDATE_DATA = OrgUpdateData(
    notes=os.getenv("ROOT_ORG_NOTES", "automation"),
    organization_name=os.getenv("ROOT_ORG_NAME", "SEC p"),
)

# Keep this in config in case the menu trigger id changes by environment.
ORG_ACTIONS_TRIGGER = os.getenv("ROOT_ORG_ACTIONS_TRIGGER", "#radix-_r_4_")
