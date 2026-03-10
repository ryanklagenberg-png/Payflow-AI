import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import settings


async def save_file(file: UploadFile) -> str:
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix if file.filename else ""
    filename = f"{uuid.uuid4()}{ext}"
    file_path = upload_dir / filename

    content = await file.read()
    file_path.write_bytes(content)

    return str(file_path)


def get_file(path: str) -> bytes:
    return Path(path).read_bytes()
