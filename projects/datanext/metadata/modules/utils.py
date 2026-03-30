from pathlib import Path
import random
import uuid


def pick_random_media_file(media_dir: Path) -> Path:
    if not media_dir.exists() or not media_dir.is_dir():
        raise FileNotFoundError(f"Media directory not found: {media_dir}")

    files = [path for path in media_dir.iterdir() if path.is_file()]
    if not files:
        raise FileNotFoundError(f"No media files found in: {media_dir}")

    return random.choice(files)


def generate_batch_id() -> str:
    return str(uuid.uuid4())


def generate_batch_sequence() -> int:
    return random.randint(1, 999999)


def build_title_from_file(file_name: str, batch_sequence: int) -> str:
    return f"{Path(file_name).stem} - batch-sequence: {batch_sequence}"


def build_about_from_file(file_name: str) -> str:
    return f"Auto-generated metadata for uploaded file: {file_name}"

