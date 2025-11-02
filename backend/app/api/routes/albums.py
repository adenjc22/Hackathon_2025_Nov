"""
Albums API Routes - Auto-generated albums based on AI tags
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from pathlib import Path
import os

from app.database.session import get_db
from app.database.models_media import Media, ProcessingStatus
from app.database.models_user import User
from app.core.dependencies import get_current_user


router = APIRouter(tags=["Albums"])


class AlbumResponse(BaseModel):
    """Response model for an album"""
    id: str
    title: str
    coverUrl: str
    mediaCount: int
    tag: Optional[str] = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[AlbumResponse])
async def list_albums(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate smart albums based on AI-detected tags.
    
    Creates albums for:
    - People photos
    - Common tags (nature, indoor, outdoor, etc.)
    - Top detected objects/scenes
    """
    backend_url = os.getenv("BACKEND_URL", "https://memory-lane-backend.up.railway.app")
    
    # Get all processed media for current user
    media_items = db.query(Media).filter(
        Media.owner_id == current_user.id,
        Media.status == ProcessingStatus.DONE,
        Media.tags.isnot(None)
    ).all()
    
    if not media_items:
        return []
    
    # Count tags across all photos
    tag_counts: Dict[str, List[Media]] = {}
    
    for item in media_items:
        if item.tags and isinstance(item.tags, list):
            for tag in item.tags:
                tag_lower = tag.lower()
                if tag_lower not in tag_counts:
                    tag_counts[tag_lower] = []
                tag_counts[tag_lower].append(item)
    
    # Create albums for tags with multiple photos
    albums = []
    
    # Special album: People
    people_photos = [item for item in media_items if item.has_people]
    if people_photos:
        first_photo = people_photos[0]
        albums.append(AlbumResponse(
            id="people",
            title="People",
            coverUrl=f"{backend_url}/uploads/{Path(first_photo.stored_path).name}",
            mediaCount=len(people_photos),
            tag="people"
        ))
    
    # Create albums for common tags (minimum 2 photos)
    sorted_tags = sorted(
        [(tag, photos) for tag, photos in tag_counts.items() if len(photos) >= 2],
        key=lambda x: len(x[1]),
        reverse=True
    )
    
    # Limit to top 20 albums
    for tag, photos in sorted_tags[:20]:
        # Skip if already covered by "People" album
        if tag in ['person', 'people', 'man', 'woman', 'child', 'face', 'portrait']:
            continue
        
        # Use first photo as cover
        cover_photo = photos[0]
        
        albums.append(AlbumResponse(
            id=f"tag-{tag}",
            title=tag.title(),  # Capitalize first letter
            coverUrl=f"{backend_url}/uploads/{Path(cover_photo.stored_path).name}",
            mediaCount=len(photos),
            tag=tag
        ))
    
    return albums


@router.get("/{album_id}/media", response_model=List[Dict[str, Any]])
async def get_album_media(
    album_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all media items in a specific album.
    
    Args:
        album_id: Album identifier (e.g., "people", "tag-nature")
    """
    backend_url = os.getenv("BACKEND_URL", "https://memory-lane-backend.up.railway.app")
    
    # Query base: user's processed media
    query = db.query(Media).filter(
        Media.owner_id == current_user.id,
        Media.status == ProcessingStatus.DONE
    )
    
    # Filter by album type
    if album_id == "people":
        query = query.filter(Media.has_people == True)
    elif album_id.startswith("tag-"):
        # Extract tag from album_id
        tag = album_id.replace("tag-", "")
        # Filter for media containing this tag
        # Note: SQLite JSON filtering is limited, so we'll filter in Python
        all_media = query.all()
        filtered_media = [
            item for item in all_media
            if item.tags and isinstance(item.tags, list) and tag in [t.lower() for t in item.tags]
        ]
        
        # Build response
        results = []
        for item in filtered_media:
            results.append({
                "id": item.id,
                "filename": item.filename,
                "file_url": f"{backend_url}/uploads/{Path(item.stored_path).name}",
                "tags": item.tags,
                "caption": item.caption,
                "has_people": item.has_people,
                "created_at": item.created_at.isoformat() if item.created_at else None
            })
        
        return results
    else:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # For non-tag albums (like "people")
    media_items = query.all()
    
    results = []
    for item in media_items:
        results.append({
            "id": item.id,
            "filename": item.filename,
            "file_url": f"{backend_url}/uploads/{Path(item.stored_path).name}",
            "tags": item.tags,
            "caption": item.caption,
            "has_people": item.has_people,
            "created_at": item.created_at.isoformat() if item.created_at else None
        })
    
    return results
