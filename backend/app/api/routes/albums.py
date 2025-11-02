"""
Albums API Routes - AI-Generated Smart Albums
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel, Field
from pathlib import Path
from datetime import datetime
import os

from app.database.session import get_db
from app.database.models_album import Album
from app.database.models_media import Media, ProcessingStatus
from app.database.models_user import User
from app.core.dependencies import get_current_user
from app.services.album_service import SmartAlbumService
from app.services.search_service import SearchService
from app.utils.embeddings import embedding_service


router = APIRouter(tags=["Albums"])


def get_backend_url(request: Request) -> str:
    """
    Dynamically determine backend URL based on environment.
    """
    backend_url = os.getenv("BACKEND_URL")
    if backend_url:
        return backend_url
    return str(request.base_url).rstrip('/')


# Response Models
class AlbumSummary(BaseModel):
    """Summary info for an album"""
    id: int
    title: str
    theme_tag: str
    cover_url: Optional[str] = None
    media_count: int
    description: Optional[str] = None
    is_auto_generated: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MediaInAlbum(BaseModel):
    """Media item within an album"""
    id: int
    filename: str
    file_url: str
    caption: Optional[str] = None
    tags: Optional[List[str]] = None
    has_people: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class AlbumDetail(BaseModel):
    """Detailed album with all media"""
    id: int
    title: str
    theme_tag: str
    description: Optional[str] = None
    cover_url: Optional[str] = None
    media_count: int
    is_auto_generated: bool
    created_at: datetime
    media_items: List[MediaInAlbum]
    
    class Config:
        from_attributes = True


class AlbumSuggestion(BaseModel):
    """Suggested album that could be created"""
    theme: str
    title: str
    photo_count: int


class CreateAlbumRequest(BaseModel):
    """Request to manually create an album"""
    title: str = Field(..., min_length=1, max_length=100)
    theme_tag: Optional[str] = None
    media_ids: Optional[List[int]] = None


class CreateAlbumFromPromptRequest(BaseModel):
    """Request to create an album from a natural language prompt"""
    prompt: str = Field(..., min_length=1, description="Natural language description of photos to include")
    title: Optional[str] = Field(None, description="Optional custom title, otherwise generated from prompt")


class AddPhotosRequest(BaseModel):
    """Request to add photos to an album"""
    media_ids: List[int] = Field(..., min_items=1, description="List of media IDs to add to album")


# API Endpoints

@router.get("/", response_model=List[AlbumSummary])
async def list_albums(
    request: Request,
    auto_only: Optional[bool] = Query(None, description="Filter by auto-generated albums only"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all albums for the current user with optional filtering.
    
    Query parameters:
    - auto_only: true = only AI-generated albums, false = only manual albums, null = all albums
    
    Albums are automatically created based on:
    - Common tags (nature, outdoor, food, etc.)
    - People detection
    - Dominant themes in photos
    """
    backend_url = get_backend_url(request)
    
    # Build query with optional filter
    query = db.query(Album).filter(Album.owner_id == current_user.id)
    
    if auto_only is not None:
        if auto_only:
            # Only auto-generated albums
            query = query.filter(Album.is_auto_generated == 1)
        else:
            # Only manual albums
            query = query.filter(Album.is_auto_generated == 0)
    
    # Get albums ordered by photo count
    albums = query.order_by(desc(Album.media_count)).all()
    
    # Build response with cover URLs
    result = []
    for album in albums:
        cover_url = None
        if album.cover_media:
            cover_url = f"{backend_url}/uploads/{Path(album.cover_media.stored_path).name}"
        
        result.append(AlbumSummary(
            id=album.id,
            title=album.title,
            theme_tag=album.theme_tag,
            cover_url=cover_url,
            media_count=album.media_count,
            description=album.description,
            is_auto_generated=bool(album.is_auto_generated),
            created_at=album.created_at,
            updated_at=album.updated_at
        ))
    
    return result


@router.get("/{album_id}", response_model=AlbumDetail)
async def get_album(
    album_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed information about a specific album including all its media.
    """
    backend_url = get_backend_url(request)
    
    # Get album
    album = db.query(Album).filter(
        Album.id == album_id,
        Album.owner_id == current_user.id
    ).first()
    
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Get all media in album
    media_items = album.media_items.all()
    
    # Build media list
    media_list = []
    for media in media_items:
        media_list.append(MediaInAlbum(
            id=media.id,
            filename=media.filename,
            file_url=f"{backend_url}/uploads/{Path(media.stored_path).name}",
            caption=media.caption,
            tags=media.tags,
            has_people=media.has_people or False,
            created_at=media.created_at
        ))
    
    # Build response
    cover_url = None
    if album.cover_media:
        cover_url = f"{backend_url}/uploads/{Path(album.cover_media.stored_path).name}"
    
    return AlbumDetail(
        id=album.id,
        title=album.title,
        theme_tag=album.theme_tag,
        description=album.description,
        cover_url=cover_url,
        media_count=album.media_count,
        is_auto_generated=bool(album.is_auto_generated),
        created_at=album.created_at,
        media_items=media_list
    )


@router.post("/", response_model=AlbumSummary)
async def create_album(
    album_data: CreateAlbumRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Manually create a new album.
    
    Args:
        album_data: Album title and optional media IDs
    """
    backend_url = get_backend_url(request)
    
    # Create album
    theme_tag = album_data.theme_tag or album_data.title.lower().replace(' ', '_')
    
    new_album = Album(
        owner_id=current_user.id,
        title=album_data.title,
        theme_tag=theme_tag,
        is_auto_generated=0,  # Manually created
        media_count=0
    )
    
    db.add(new_album)
    db.flush()
    
    # Add media if provided
    if album_data.media_ids:
        media_items = db.query(Media).filter(
            Media.id.in_(album_data.media_ids),
            Media.owner_id == current_user.id
        ).all()
        
        for media in media_items:
            new_album.media_items.append(media)
        
        new_album.media_count = len(media_items)
        
        # Set first media as cover
        if media_items:
            new_album.cover_media_id = media_items[0].id
    
    db.commit()
    db.refresh(new_album)
    
    # Build response
    cover_url = None
    if new_album.cover_media:
        cover_url = f"{backend_url}/uploads/{Path(new_album.cover_media.stored_path).name}"
    
    return AlbumSummary(
        id=new_album.id,
        title=new_album.title,
        theme_tag=new_album.theme_tag,
        cover_url=cover_url,
        media_count=new_album.media_count,
        description=new_album.description,
        is_auto_generated=False,
        created_at=new_album.created_at,
        updated_at=new_album.updated_at
    )


@router.post("/create-from-prompt", response_model=AlbumDetail)
async def create_album_from_prompt(
    album_data: CreateAlbumFromPromptRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create an album from a natural language prompt.
    
    This uses AI to:
    1. Search for photos matching the prompt
    2. Generate a title if not provided
    3. Create an album with matched photos
    
    Examples:
    - "all photos with dogs"
    - "sunset beach pictures"
    - "photos of my family from last summer"
    - "indoor shots with people smiling"
    """
    backend_url = get_backend_url(request)
    
    try:
        # Use search service to find matching photos
        search_service = SearchService(db)
        
        # Search for matching media using hybrid search
        results = search_service.hybrid_search(
            query=album_data.prompt,
            user_id=current_user.id,
            limit=100  # Get up to 100 matching photos
        )
        
        if not results:
            raise HTTPException(
                status_code=404, 
                detail="No photos found matching your description. Try a different prompt."
            )
        
        # Extract media IDs from results
        media_ids = [r["media"].id for r in results]
        
        # Generate title if not provided
        if not album_data.title:
            # Simple title generation from prompt
            title = album_data.prompt.strip().title()
            if len(title) > 50:
                title = title[:47] + "..."
        else:
            title = album_data.title
        
        # Create the album
        theme_tag = title.lower().replace(' ', '_')[:50]
        
        new_album = Album(
            owner_id=current_user.id,
            title=title,
            theme_tag=theme_tag,
            description=f"Photos matching: {album_data.prompt}",
            is_auto_generated=0,  # User-created via prompt
            media_count=len(media_ids)
        )
        
        db.add(new_album)
        db.flush()
        
        # Add media to album
        media_items = db.query(Media).filter(
            Media.id.in_(media_ids),
            Media.owner_id == current_user.id
        ).all()
        
        for media in media_items:
            new_album.media_items.append(media)
        
        # Set first media as cover
        if media_items:
            new_album.cover_media_id = media_items[0].id
        
        db.commit()
        db.refresh(new_album)
        
        # Build full response with media
        media_list = []
        for media in media_items:
            media_list.append(MediaInAlbum(
                id=media.id,
                filename=media.filename,
                file_url=f"{backend_url}/uploads/{Path(media.stored_path).name}",
                caption=media.caption,
                tags=media.tags,
                has_people=media.has_people or False,
                created_at=media.created_at
            ))
        
        # Build response
        cover_url = None
        if new_album.cover_media:
            cover_url = f"{backend_url}/uploads/{Path(new_album.cover_media.stored_path).name}"
        
        return AlbumDetail(
            id=new_album.id,
            title=new_album.title,
            theme_tag=new_album.theme_tag,
            description=new_album.description,
            cover_url=cover_url,
            media_count=new_album.media_count,
            is_auto_generated=False,
            created_at=new_album.created_at,
            media_items=media_list
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create album from prompt: {str(e)}"
        )


@router.put("/{album_id}")
async def update_album(
    album_id: int,
    album_data: CreateAlbumRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update album title or add/remove media.
    """
    album = db.query(Album).filter(
        Album.id == album_id,
        Album.owner_id == current_user.id
    ).first()
    
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Update title
    if album_data.title:
        album.title = album_data.title
    
    # Update media if provided
    if album_data.media_ids is not None:
        # Clear existing
        album.media_items.delete()
        
        # Add new media
        media_items = db.query(Media).filter(
            Media.id.in_(album_data.media_ids),
            Media.owner_id == current_user.id
        ).all()
        
        for media in media_items:
            album.media_items.append(media)
        
        album.media_count = len(media_items)
    
    db.commit()
    
    return {"message": "Album updated successfully"}


@router.post("/{album_id}/add-photos")
async def add_photos_to_album(
    album_id: int,
    photos_data: AddPhotosRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add photos to an existing album.
    
    Args:
        album_id: Album ID
        photos_data: List of media IDs to add
    """
    album = db.query(Album).filter(
        Album.id == album_id,
        Album.owner_id == current_user.id
    ).first()
    
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Use album service to add photos
    album_service = SmartAlbumService(db)
    added_count = album_service.add_media_to_album(album, photos_data.media_ids)
    
    db.refresh(album)
    
    return {
        "message": f"Added {added_count} photos to album",
        "total_photos": album.media_count
    }


@router.delete("/{album_id}")
async def delete_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an album (photos remain in library).
    """
    album = db.query(Album).filter(
        Album.id == album_id,
        Album.owner_id == current_user.id
    ).first()
    
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    db.delete(album)
    db.commit()
    
    return {"message": "Album deleted successfully"}


@router.get("/suggestions/", response_model=List[AlbumSuggestion])
async def get_album_suggestions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get suggestions for new albums based on unorganized photos.
    """
    album_service = SmartAlbumService(db)
    suggestions = album_service.get_album_suggestions(current_user.id)
    
    return [AlbumSuggestion(**s) for s in suggestions]


@router.post("/{album_id}/regenerate-description")
async def regenerate_description(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Regenerate AI description for an album.
    """
    album = db.query(Album).filter(
        Album.id == album_id,
        Album.owner_id == current_user.id
    ).first()
    
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    album_service = SmartAlbumService(db)
    success = album_service.update_album_descriptions(album_id)
    
    if success:
        return {"message": "Description regenerated", "description": album.description}
    else:
        raise HTTPException(status_code=500, detail="Failed to regenerate description")


@router.post("/rebuild")
async def rebuild_all_albums(
    force: bool = Query(False, description="Force rebuild even if albums exist"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Rebuild all smart albums from scratch based on current media library.
    
    This will:
    - Delete all auto-generated albums
    - Scan all media for tags
    - Create new albums based on current themes
    """
    if force:
        # Delete existing auto-generated albums
        db.query(Album).filter(
            Album.owner_id == current_user.id,
            Album.is_auto_generated == 1
        ).delete()
        db.commit()
    
    # Get all processed media
    media_items = db.query(Media).filter(
        Media.owner_id == current_user.id,
        Media.status == ProcessingStatus.DONE
    ).all()
    
    # Assign each to albums
    album_service = SmartAlbumService(db)
    total_assigned = 0
    
    for media in media_items:
        albums = album_service.assign_to_albums(media)
        total_assigned += len(albums)
    
    # Get final album count
    album_count = db.query(func.count(Album.id)).filter(
        Album.owner_id == current_user.id
    ).scalar()
    
    return {
        "message": "Albums rebuilt successfully",
        "total_albums": album_count,
        "photos_processed": len(media_items),
        "assignments_made": total_assigned
    }
