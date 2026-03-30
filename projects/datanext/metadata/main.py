from playwright.sync_api import sync_playwright

from modules.auth_api import login
from modules.config import load_config
from modules.manual_metadata_api import create_manual_metadata
from modules.media_api import create_media_file
from modules.utils import (
    build_about_from_file,
    build_title_from_file,
    generate_batch_id,
    generate_batch_sequence,
    pick_random_media_file,
)


def run() -> None:
    config = load_config()
    selected_file = pick_random_media_file(config.media_dir)
    batch_id = generate_batch_id()
    batch_sequence = generate_batch_sequence()

    print(f"[START] Base URL: {config.base_url}")
    print(f"[FILE] Selected media: {selected_file.name}")
    print(f"[BATCH] batch_id={batch_id}, batch_sequence={batch_sequence}")

    with sync_playwright() as playwright:
        request_context = playwright.request.new_context(
            base_url=config.base_url,
            ignore_https_errors=config.ignore_https_errors,
        )
        try:
            login_response = login(
                request_context=request_context,
                email=config.login_email,
                password=config.login_password,
            )
            user_email = login_response.get("user", {}).get("email")
            print(f"[LOGIN] Success for user: {user_email}")

            media_response = create_media_file(
                request_context=request_context,
                file_path=selected_file,
                folder_id=config.folder_id,
                batch_id=batch_id,
                batch_sequence=batch_sequence,
            )
            media_file_id = int(media_response["id"])
            print(f"[MEDIA] Created media_file_id: {media_file_id}")

            manual_title = build_title_from_file(selected_file.name, batch_sequence)
            manual_about = build_about_from_file(selected_file.name)

            metadata_response = create_manual_metadata(
                request_context=request_context,
                post_title=config.post_title,
                folder_id=config.folder_id,
                media_file_id=media_file_id,
                item_title=manual_title,
                item_about=manual_about,
            )
            print(f"[MANUAL_METADATA] Created post_id: {metadata_response.get('post_id')}")
            print("[DONE] API flow completed successfully.")
        finally:
            request_context.dispose()


if __name__ == "__main__":
    run()

