from pathlib import Path
from playwright.sync_api import APIRequestContext

from modules.http import post_form


def create_media_file(
    request_context: APIRequestContext,
    file_path: Path,
    folder_id: int,
    batch_id: str,
    batch_sequence: int,
) -> dict:
    file_bytes = file_path.read_bytes()
    payload = {
        "media_file": {
            "name": file_path.name,
            "mimeType": "application/octet-stream",
            "buffer": file_bytes,
        },
        "folder_id": str(folder_id),
        "batch_id": batch_id,
        "batch_sequence": str(batch_sequence),
    }
    return post_form(
        request_context=request_context,
        endpoint="/api/media-files/",
        data=payload,
        action="Create Media-File API",
    )

