from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
import uuid
from app.services import storage


router = APIRouter(prefix="/media", tags=["Media"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
max_size = 10 * 1024 * 1024  # 10 MB
allowed_types = ("image/jpeg", "image/png")


class MediaBase(BaseModel):
    filename: str = Field(..., min_length=1)
    mime_type: str = Field(..., min_length=1)
    size_bytes: int = Field(..., ge=0)
    description: Optional[str] = None


class MediaRead(MediaBase):
    id: Optional[int] = None
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


@router.post("/", response_model=MediaRead)
async def upload_media(file: UploadFile = File(...), owner_id: Optional[int] = None):
    """Save an uploaded file to disk (using app.services.storage) and return metadata.

    Note: This endpoint intentionally does not require the DB layer. If you want to
    persist media rows to the database, add a DB model and a dependency for `get_db`.
    """
    contents = await file.read()

    if len(contents) > max_size:
        raise HTTPException(status_code=413, detail="File too large")
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=415, detail="Unsupported media type")

    # Use the existing storage service to save the file
    dest_path = storage.save_upload(file, contents, owner_id)
    metadata = storage.extract_metadata(dest_path)

    return MediaRead(
        filename=file.filename,
        mime_type=file.content_type,
        size_bytes=metadata.get("size_bytes", len(contents)),
        description=None,
        id=None,
        owner_id=owner_id,
        created_at=datetime.utcnow(),
        updated_at=None,
    )