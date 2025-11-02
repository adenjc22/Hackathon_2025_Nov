"""
Search API Routes - Natural language search endpoints for Phase 4
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from pathlib import Path

from app.database.session import get_db
from app.services.search_service import SearchService
from app.utils.embeddings import embedding_service
from loguru import logger


router = APIRouter(tags=["Search"])


# Request/Response Models
class EmbeddingRequest(BaseModel):
    """Request model for generating embeddings"""
    text: str = Field(..., min_length=1, description="Text to embed")


class EmbeddingResponse(BaseModel):
    """Response model for embedding generation"""
    text: str
    embedding: List[float]
    dimension: int


class SearchFilters(BaseModel):
    """Optional filters for search queries"""
    has_people: Optional[bool] = Field(None, description="Filter by presence of people")
    date_from: Optional[datetime] = Field(None, description="Filter by start date")
    date_to: Optional[datetime] = Field(None, description="Filter by end date")
    tags: Optional[List[str]] = Field(None, description="Filter by specific tags")


class MediaSearchResult(BaseModel):
    """Single search result with media data and relevance score"""
    id: int
    filename: str
    caption: Optional[str]
    tags: Optional[List[str]]
    emotion: Optional[Dict[str, Any]]
    has_people: Optional[bool]
    file_url: str
    created_at: datetime
    score: float = Field(..., description="Relevance score (0-1)")
    match_type: str = Field(..., description="Type of match: semantic, text, or hybrid")
    
    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    """Response model for search queries"""
    query: str
    total_results: int
    results: List[MediaSearchResult]
    search_type: str = Field(..., description="Type of search performed")
    filters_applied: Optional[Dict[str, Any]] = None


class RecommendationResponse(BaseModel):
    """Response model for recommendations"""
    reference_media_id: int
    total_results: int
    results: List[MediaSearchResult]


# API Endpoints

@router.post("/embeddings", response_model=EmbeddingResponse)
async def generate_embedding(
    request: EmbeddingRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a vector embedding for the given text.
    
    This endpoint is useful for:
    - Testing the embedding service
    - Pre-computing embeddings client-side
    - Understanding how queries are vectorized
    """
    logger.info(f"Generating embedding for text: {request.text[:50]}...")
    
    embedding = embedding_service.generate_embedding(request.text)
    
    if not embedding:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate embedding. Check OpenAI API key."
        )
    
    return EmbeddingResponse(
        text=request.text,
        embedding=embedding,
        dimension=len(embedding)
    )


@router.get("/search", response_model=SearchResponse)
async def search_media(
    query: str = Query(..., min_length=1, description="Natural language search query"),
    search_type: str = Query("hybrid", regex="^(semantic|text|hybrid)$", description="Search algorithm to use"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    has_people: Optional[bool] = Query(None, description="Filter by presence of people"),
    date_from: Optional[datetime] = Query(None, description="Filter by start date"),
    date_to: Optional[datetime] = Query(None, description="Filter by end date"),
    db: Session = Depends(get_db)
):
    """
    Search media using natural language queries.
    
    **Search Types:**
    - `semantic`: Vector similarity search using embeddings (most intelligent)
    - `text`: Traditional keyword search (fallback)
    - `hybrid`: Combines both methods (recommended, default)
    
    **Examples:**
    - "happy moments with friends"
    - "sunset at the beach"
    - "family dinner photos"
    - "pictures with people smiling"
    
    **Filters:**
    - `has_people`: true/false to filter photos with/without people
    - `date_from` / `date_to`: Filter by date range
    - `user_id`: Filter by owner (admin use)
    """
    logger.info(f"Search request: query='{query}', type={search_type}, limit={limit}")
    
    # Build filters dictionary
    filters = {}
    if has_people is not None:
        filters["has_people"] = has_people
    if date_from:
        filters["date_from"] = date_from
    if date_to:
        filters["date_to"] = date_to
    
    # Initialize search service
    search_service = SearchService(db)
    
    # Perform search based on type
    if search_type == "semantic":
        results = search_service.semantic_search(
            query=query,
            user_id=user_id,
            limit=limit,
            offset=offset,
            filters=filters if filters else None
        )
    elif search_type == "text":
        results = search_service.text_search(
            query=query,
            user_id=user_id,
            limit=limit,
            offset=offset,
            filters=filters if filters else None
        )
    else:  # hybrid
        results = search_service.hybrid_search(
            query=query,
            user_id=user_id,
            limit=limit,
            offset=offset,
            filters=filters if filters else None
        )
    
    # Format results
    formatted_results = []
    for result in results:
        media = result["media"]
        formatted_results.append(
            MediaSearchResult(
                id=media.id,
                filename=media.filename,
                caption=media.caption,
                tags=media.tags,
                emotion=media.emotion,
                has_people=media.has_people,
                file_url=f"/uploads/{Path(media.stored_path).name}",
                created_at=media.created_at,
                score=result["score"],
                match_type=result["match_type"]
            )
        )
    
    logger.info(f"Returning {len(formatted_results)} results for query: {query}")
    
    return SearchResponse(
        query=query,
        total_results=len(formatted_results),
        results=formatted_results,
        search_type=search_type,
        filters_applied=filters if filters else None
    )


@router.get("/search/similar/{media_id}", response_model=RecommendationResponse)
async def get_similar_media(
    media_id: int,
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results"),
    db: Session = Depends(get_db)
):
    """
    Get media items similar to a given photo.
    
    Uses vector similarity to find photos with similar:
    - Visual content
    - Captions and descriptions
    - Mood and emotions
    - Tags and themes
    
    Perfect for "More like this" features.
    """
    logger.info(f"Finding similar media to {media_id}")
    
    search_service = SearchService(db)
    results = search_service.get_recommendations(
        media_id=media_id,
        user_id=user_id,
        limit=limit
    )
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"Media {media_id} not found or has no embedding"
        )
    
    # Format results
    formatted_results = []
    for result in results:
        media = result["media"]
        formatted_results.append(
            MediaSearchResult(
                id=media.id,
                filename=media.filename,
                caption=media.caption,
                tags=media.tags,
                emotion=media.emotion,
                has_people=media.has_people,
                file_url=f"/uploads/{Path(media.stored_path).name}",
                created_at=media.created_at,
                score=result["score"],
                match_type=result["match_type"]
            )
        )
    
    return RecommendationResponse(
        reference_media_id=media_id,
        total_results=len(formatted_results),
        results=formatted_results
    )


@router.post("/search/reindex")
async def reindex_media(
    user_id: Optional[int] = Query(None, description="Reindex specific user's media only"),
    force: bool = Query(False, description="Force reindex even if embeddings exist"),
    db: Session = Depends(get_db)
):
    """
    Regenerate embeddings for existing media items.
    
    **Use cases:**
    - Initial setup after enabling search
    - After changing embedding models
    - Fixing missing embeddings
    
    **Parameters:**
    - `user_id`: Only reindex specific user's photos
    - `force`: Regenerate even if embeddings already exist
    
    ⚠️ Warning: This can be slow for large libraries!
    """
    from app.database.models_media import Media, ProcessingStatus
    
    logger.info(f"Starting reindex (user_id={user_id}, force={force})")
    
    # Build query
    query = db.query(Media).filter(Media.status == ProcessingStatus.DONE)
    
    if user_id is not None:
        query = query.filter(Media.owner_id == user_id)
    
    if not force:
        # Only reindex items without embeddings
        query = query.filter(Media.embedding.is_(None))
    
    media_items = query.all()
    
    if not media_items:
        return {
            "message": "No media items to reindex",
            "total": 0,
            "success": 0,
            "failed": 0
        }
    
    logger.info(f"Reindexing {len(media_items)} media items...")
    
    success_count = 0
    failed_count = 0
    
    for media in media_items:
        try:
            # Generate search text
            search_text = embedding_service.generate_search_text(media)
            media.search_text = search_text
            
            # Generate embedding
            embedding = embedding_service.generate_embedding(search_text)
            
            if embedding:
                media.embedding = embedding
                
                # Update has_people flag
                has_people = False
                if media.tags:
                    people_tags = ["person", "people", "man", "woman", "child", "face", "portrait"]
                    has_people = any(tag.lower() in people_tags for tag in media.tags)
                
                media.has_people = has_people
                
                success_count += 1
                logger.debug(f"Reindexed media {media.id}")
            else:
                failed_count += 1
                logger.warning(f"Failed to generate embedding for media {media.id}")
        
        except Exception as e:
            failed_count += 1
            logger.error(f"Error reindexing media {media.id}: {str(e)}")
    
    # Commit all changes
    db.commit()
    
    logger.info(f"Reindex complete: {success_count} success, {failed_count} failed")
    
    return {
        "message": "Reindexing complete",
        "total": len(media_items),
        "success": success_count,
        "failed": failed_count
    }
