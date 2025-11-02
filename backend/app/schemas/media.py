from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class MediaBase(BaseModel):
    filename: str = Field(..., min_length=1)
    mime_type: str = Field(..., min_length=1)
    size_bytes: int = Field(..., ge=0)
    metadata_json: dict[str, Any] | None = None


class MediaRead(MediaBase):
    id: int
    stored_path: str
    owner_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True