from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pathlib import Path
import uuid
from sqlalchemy.orm import Session
from app.services import storage
from app.database.models_media import Media 
from app.database.session import get_db
# Note: we define a local MediaRead (below) so we don't need to import the project's
# schema here. Importing it earlier caused a name collision and unexpected behavior.


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
        from_attributes = True


@router.post("/", response_model=MediaRead)
async def upload_media(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Save an uploaded file to disk (using app.services.storage) and return metadata.

    Note: This endpoint intentionally does not require the DB layer. If you want to
    persist media rows to the database, add a DB model and a dependency for `get_db`.
    """
    contents = await file.read()

    if len(contents) > max_size:
        raise HTTPException(status_code=413, detail="File too large")
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=415, detail="Unsupported media type")

    # Ensure the storage service writes into the same upload dir that this module
    # (and the tests) may monkeypatch. Tests patch `app.api.routes.media.UPLOAD_DIR`,
    # so copy that into the storage module before saving.
    storage.UPLOAD_DIR = UPLOAD_DIR

    # Use the existing storage service to save the file
    ext = Path(file.filename).suffix or ".bin"
    owner_id = None
    dest_path = storage.save_upload(file, contents, owner_id)
    metadata = storage.extract_metadata(dest_path)

    # Persist the DB row. The Media model requires `stored_path` and `size_bytes`.
    # SQLAlchemy auto-generates id, created_at, and updated_at.
    media_row = Media(
        filename=file.filename,
        stored_path=str(dest_path),
        mime_type=file.content_type,
        size_bytes=metadata.get("size_bytes", len(contents)),
        metadata_json=metadata,
        owner_id=owner_id,
    )

    db.add(media_row)
    db.commit()
    db.refresh(media_row)

    # Return a response model using ORM mode
    return MediaRead.from_orm(media_row)
