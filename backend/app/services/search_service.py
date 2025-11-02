"""
Search Service - Implements semantic search using embeddings
and hybrid search combining vector similarity with filters.
"""

from typing import List, Optional, Dict, Any
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
import json
import math

from app.database.models_media import Media, ProcessingStatus
from app.utils.embeddings import embedding_service


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Similarity score between -1 and 1 (higher is more similar)
    """
    if not vec1 or not vec2:
        return 0.0
    
    if len(vec1) != len(vec2):
        return 0.0
    
    # Dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # Magnitudes
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    # Cosine similarity
    similarity = dot_product / (magnitude1 * magnitude2)
    return similarity


class SearchService:
    """Service for semantic and hybrid search of media items."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def semantic_search(
        self,
        query: str,
        user_id: Optional[int] = None,
        limit: int = 20,
        offset: int = 0,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search using natural language query.
        
        Args:
            query: Natural language search query
            user_id: Filter by user (None for all users)
            limit: Maximum number of results
            offset: Pagination offset
            filters: Optional filters (has_people, mood, date_range)
            
        Returns:
            List of media items with similarity scores
        """
        if not query or not query.strip():
            logger.warning("Empty search query provided")
            return []
        
        # Generate embedding for the query
        query_embedding = embedding_service.generate_embedding(query)
        
        if not query_embedding:
            logger.error("Failed to generate query embedding")
            # Fallback to text search
            return self.text_search(query, user_id, limit, offset, filters)
        
        # Build base query with filters
        base_query = self.db.query(Media).filter(
            Media.status == ProcessingStatus.DONE,
            Media.embedding.isnot(None)  # Only items with embeddings
        )
        
        # Apply user filter
        if user_id is not None:
            base_query = base_query.filter(Media.owner_id == user_id)
        
        # Apply additional filters
        if filters:
            base_query = self._apply_filters(base_query, filters)
        
        # Fetch candidates
        candidates = base_query.all()
        
        if not candidates:
            logger.info("No candidates found for semantic search")
            return []
        
        # Calculate similarity scores
        results = []
        for media in candidates:
            try:
                # Parse embedding from JSON
                if isinstance(media.embedding, str):
                    media_embedding = json.loads(media.embedding)
                else:
                    media_embedding = media.embedding
                
                # Calculate similarity
                similarity = cosine_similarity(query_embedding, media_embedding)
                
                results.append({
                    "media": media,
                    "score": similarity,
                    "match_type": "semantic"
                })
                
            except Exception as e:
                logger.error(f"Error processing media {media.id}: {str(e)}")
                continue
        
        # Sort by similarity score (descending)
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Apply pagination
        paginated_results = results[offset:offset + limit]
        
        logger.info(f"Semantic search returned {len(paginated_results)} results")
        return paginated_results
    
    def text_search(
        self,
        query: str,
        user_id: Optional[int] = None,
        limit: int = 20,
        offset: int = 0,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fallback text-based search using LIKE queries.
        Used when embeddings are not available.
        
        Args:
            query: Search query
            user_id: Filter by user
            limit: Maximum results
            offset: Pagination offset
            filters: Additional filters
            
        Returns:
            List of media items
        """
        # Build base query
        base_query = self.db.query(Media).filter(
            Media.status == ProcessingStatus.DONE
        )
        
        # Apply user filter
        if user_id is not None:
            base_query = base_query.filter(Media.owner_id == user_id)
        
        # Apply text search
        search_pattern = f"%{query}%"
        base_query = base_query.filter(
            or_(
                func.lower(Media.caption).like(func.lower(search_pattern)),
                func.lower(Media.search_text).like(func.lower(search_pattern))
            )
        )
        
        # Apply additional filters
        if filters:
            base_query = self._apply_filters(base_query, filters)
        
        # Order by most recent
        base_query = base_query.order_by(Media.created_at.desc())
        
        # Pagination
        results = base_query.limit(limit).offset(offset).all()
        
        # Format results
        formatted_results = [
            {
                "media": media,
                "score": 0.5,  # Fixed score for text search
                "match_type": "text"
            }
            for media in results
        ]
        
        logger.info(f"Text search returned {len(formatted_results)} results")
        return formatted_results
    
    def hybrid_search(
        self,
        query: str,
        user_id: Optional[int] = None,
        limit: int = 20,
        offset: int = 0,
        filters: Optional[Dict[str, Any]] = None,
        semantic_weight: float = 0.7,
        text_weight: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Hybrid search combining semantic and text-based search.
        
        Args:
            query: Search query
            user_id: Filter by user
            limit: Maximum results
            offset: Pagination offset
            filters: Additional filters
            semantic_weight: Weight for semantic similarity (0-1)
            text_weight: Weight for text match (0-1)
            
        Returns:
            Combined and ranked results
        """
        # Get semantic results
        semantic_results = self.semantic_search(
            query, user_id, limit * 2, 0, filters  # Get more candidates
        )
        
        # Get text results
        text_results = self.text_search(
            query, user_id, limit * 2, 0, filters
        )
        
        # Combine results
        combined = {}
        
        # Add semantic results
        for result in semantic_results:
            media_id = result["media"].id
            combined[media_id] = {
                "media": result["media"],
                "semantic_score": result["score"],
                "text_score": 0.0
            }
        
        # Add/merge text results
        for result in text_results:
            media_id = result["media"].id
            if media_id in combined:
                combined[media_id]["text_score"] = result["score"]
            else:
                combined[media_id] = {
                    "media": result["media"],
                    "semantic_score": 0.0,
                    "text_score": result["score"]
                }
        
        # Calculate hybrid scores
        hybrid_results = []
        for media_id, data in combined.items():
            hybrid_score = (
                semantic_weight * data["semantic_score"] +
                text_weight * data["text_score"]
            )
            
            hybrid_results.append({
                "media": data["media"],
                "score": hybrid_score,
                "match_type": "hybrid",
                "semantic_score": data["semantic_score"],
                "text_score": data["text_score"]
            })
        
        # Sort by hybrid score
        hybrid_results.sort(key=lambda x: x["score"], reverse=True)
        
        # Apply pagination
        paginated_results = hybrid_results[offset:offset + limit]
        
        logger.info(f"Hybrid search returned {len(paginated_results)} results")
        return paginated_results
    
    def _apply_filters(self, query, filters: Dict[str, Any]):
        """
        Apply additional filters to the query.
        
        Args:
            query: SQLAlchemy query object
            filters: Dictionary of filters
            
        Returns:
            Modified query
        """
        # Filter by has_people
        if "has_people" in filters:
            query = query.filter(Media.has_people == filters["has_people"])
        
        # Filter by date range
        if "date_from" in filters:
            query = query.filter(Media.created_at >= filters["date_from"])
        
        if "date_to" in filters:
            query = query.filter(Media.created_at <= filters["date_to"])
        
        # Filter by tags (if tags contain specific keywords)
        if "tags" in filters and filters["tags"]:
            tag_filters = []
            for tag in filters["tags"]:
                # JSON search in SQLite (checking if tag exists in JSON array)
                tag_filters.append(
                    func.json_extract(Media.tags, '$').like(f'%{tag}%')
                )
            if tag_filters:
                query = query.filter(or_(*tag_filters))
        
        return query
    
    def get_recommendations(
        self,
        media_id: int,
        user_id: Optional[int] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get similar media items based on a given media item.
        
        Args:
            media_id: ID of the reference media
            user_id: Filter by user
            limit: Maximum results
            
        Returns:
            List of similar media items
        """
        # Get reference media
        reference = self.db.query(Media).filter(Media.id == media_id).first()
        
        if not reference or not reference.embedding:
            logger.warning(f"Media {media_id} not found or has no embedding")
            return []
        
        # Parse reference embedding
        if isinstance(reference.embedding, str):
            reference_embedding = json.loads(reference.embedding)
        else:
            reference_embedding = reference.embedding
        
        # Get candidates
        base_query = self.db.query(Media).filter(
            Media.status == ProcessingStatus.DONE,
            Media.embedding.isnot(None),
            Media.id != media_id  # Exclude the reference itself
        )
        
        if user_id is not None:
            base_query = base_query.filter(Media.owner_id == user_id)
        
        candidates = base_query.all()
        
        # Calculate similarities
        results = []
        for media in candidates:
            try:
                if isinstance(media.embedding, str):
                    media_embedding = json.loads(media.embedding)
                else:
                    media_embedding = media.embedding
                
                similarity = cosine_similarity(reference_embedding, media_embedding)
                
                results.append({
                    "media": media,
                    "score": similarity,
                    "match_type": "similar"
                })
                
            except Exception as e:
                logger.error(f"Error processing media {media.id}: {str(e)}")
                continue
        
        # Sort and limit
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:limit]
        
        logger.info(f"Found {len(results)} similar items to media {media_id}")
        return results
