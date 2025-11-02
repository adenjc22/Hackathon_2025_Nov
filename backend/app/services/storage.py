from pathlib import Path
import uuid
import json

UPLOAD_DIR = Path("Uploads")

def save_upload(file, contents: bytes, owner_id: int) -> Path:
    ext = Path(file.filename).suffix
    filename = f"{owner_id}_{uuid.uuid4().hex}{ext}"
    dest = UPLOAD_DIR / filename
    with open(dest, "wb") as f:
        f.write(contents)
    return dest

def extract_metadata(file_path: Path) -> dict:
    return {
        "stored_at": str(file_path),
        "size_bytes": file_path.stat().st_size,
    }