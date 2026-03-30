from playwright.sync_api import APIRequestContext

from modules.http import post_json


def create_manual_metadata(
    request_context: APIRequestContext,
    post_title: str,
    folder_id: int,
    media_file_id: int,
    item_title: str,
    item_about: str,
) -> dict:
    payload = {
        "post_title": post_title,
        "folder_id": folder_id,
        "items": [
            {
                "media_file_id": media_file_id,
                "title": item_title,
                "about": item_about,
            }
        ],
    }
    return post_json(
        request_context=request_context,
        endpoint="/api/manual-metadata/",
        payload=payload,
        action="Create Manual-Metadata API",
    )

