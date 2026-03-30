from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class ApiConfig:
    base_url: str
    login_email: str
    login_password: str
    folder_id: int
    media_dir: Path
    post_title: str
    ignore_https_errors: bool


def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def load_config() -> ApiConfig:
    root_dir = Path(__file__).resolve().parents[1]
    media_dir = root_dir / "media"

    return ApiConfig(
        base_url=os.getenv("DATANEXT_BASE_URL", "https://appbackend.fordata.ai"),
        login_email=os.getenv("DATANEXT_LOGIN_EMAIL", "hira.khalid+2@betacodespk.com"),
        login_password=os.getenv("DATANEXT_LOGIN_PASSWORD", "Forbmax@23"),
        folder_id=int(os.getenv("DATANEXT_FOLDER_ID", "12")),
        media_dir=media_dir,
        post_title=os.getenv("DATANEXT_POST_TITLE", "Post title"),
        ignore_https_errors=_as_bool(os.getenv("DATANEXT_IGNORE_HTTPS_ERRORS", "false")),
    )

