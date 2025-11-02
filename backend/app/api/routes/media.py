from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pathlib import Path
import uuid
import os
from sqlalchemy.orm import Session
from app.services import storage
from app.database.models_media import Media, ProcessingStatus
from app.database.session import get_db
from app.core.dependencies import get_current_user
from app.database.models_user import User
# Note: we define a local MediaRead (below) so we don't need to import the project's
# schema here. Importing it earlier caused a name collision and unexpected behavior.


router = APIRouter(tags=["Media"])

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
    file_url: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    emotion: Optional[dict] = None
    caption: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("/", response_model=MediaRead)
async def upload_media(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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
    owner_id = current_user.id  # Set the owner to the current logged-in user
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
        status=ProcessingStatus.PENDING,  # Set initial status
    )

    db.add(media_row)
    db.commit()
    db.refresh(media_row)

    # Build the response with FULL file URL (including backend domain)
    backend_url = os.getenv("BACKEND_URL", "https://memory-lane-backend.up.railway.app")
    response = MediaRead.from_orm(media_row)
    response.file_url = f"{backend_url}/uploads/{Path(media_row.stored_path).name}"
    
    return response


@router.get("/", response_model=List[MediaRead])
async def list_media(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all uploaded media for the current user."""
    backend_url = os.getenv("BACKEND_URL", "https://memory-lane-backend.up.railway.app")
    # Filter media by the current user's ID
    media_items = db.query(Media).filter(Media.owner_id == current_user.id).order_by(Media.created_at.desc()).all()
    results = []
    for item in media_items:
        media_read = MediaRead.from_orm(item)
        media_read.file_url = f"{backend_url}/uploads/{Path(item.stored_path).name}"
        results.append(media_read)
    return results


@router.delete("/{media_id}")
async def delete_media(
    media_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a media item and its file."""
    media_item = db.query(Media).filter(Media.id == media_id).first()
    
    if not media_item:
        raise HTTPException(status_code=404, detail="Media not found")
    
    # Ensure the user owns this media
    if media_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this media")
    
    # Delete the file from disk
    file_path = Path(media_item.stored_path)
    if file_path.exists():
        file_path.unlink()
    
    # Delete from database
    db.delete(media_item)
    db.commit()
    
    return {"message": "Media deleted successfully"}


@router.get("/status/{media_id}", response_model=MediaRead)
async def get_media_status(media_id: int, db: Session = Depends(get_db)):
    """
    Get the processing status and AI results for a media item.
    Frontend can poll this endpoint to track processing progress.
    """
    media_item = db.query(Media).filter(Media.id == media_id).first()
    
    if not media_item:
        raise HTTPException(status_code=404, detail="Media not found")
    
    response = MediaRead.from_orm(media_item)
    response.file_url = f"/uploads/{Path(media_item.stored_path).name}"
    
    return response
