"""
Smart Album Service - Automatically organize photos into themed albums
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from collections import Counter
from loguru import logger

from app.database.models_album import Album
from app.database.models_media import Media, ProcessingStatus


class SmartAlbumService:
    """
    Service for creating and managing AI-generated smart albums.
    
    Automatically groups photos by:
    - Common tags (nature, outdoor, food, etc.)
    - People detection
    - Dominant themes
    """
    
    # Minimum photos required to create an album
    MIN_PHOTOS_FOR_ALBUM = 2
    
    # Maximum number of auto-generated albums per user
    MAX_AUTO_ALBUMS = 30
    
    # Tag priority weights (higher = more likely to create album)
    TAG_PRIORITIES = {
        'people': 100,
        'person': 100,
        'nature': 90,
        'outdoor': 85,
        'indoor': 80,
        'food': 85,
        'travel': 90,
        'beach': 85,
        'mountain': 85,
        'city': 80,
        'celebration': 90,
        'party': 90,
        'family': 95,
        'friends': 95,
        'wedding': 95,
        'birthday': 95,
    }
    
    # Tags to exclude from album creation (too generic)
    EXCLUDED_TAGS = {
        'photo', 'image', 'picture', 'photography',
        'color', 'colors', 'light', 'dark',
        'view', 'scene', 'background'
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def assign_to_albums(self, media: Media) -> List[Album]:
        """
        Automatically assign a media item to appropriate albums.
        Creates new albums if needed.
        
        IMPORTANT: Only creates albums, does NOT add photos to them.
        Photos must be manually added to albums by user.
        
        Args:
            media: Media item with AI-processed tags
            
        Returns:
            List of albums created (but media NOT added to them)
        """
        if not media.tags or media.status != ProcessingStatus.DONE:
            logger.debug(f"Media {media.id} not ready for album assignment")
            return []
        
        created_albums = []
        
        # Get top 3 most relevant tags 
        top_tags = self._get_top_tags(media.tags, max_tags=3)
        
        logger.info(f"Processing media {media.id} with top 3 tags: {top_tags}")
        
        # Special case: People album (if has people)
        if media.has_people and 'people' not in top_tags:
            people_album = self._get_or_create_album(
                owner_id=media.owner_id,
                theme_tag='people',
                title='People'
            )
            if people_album:
                created_albums.append(people_album)
        
        # Create albums for top 3 tags only
        for tag in top_tags:
            tag_lower = tag.lower().strip()
            
            # Skip excluded tags
            if tag_lower in self.EXCLUDED_TAGS:
                continue
            
            # Skip very short tags
            if len(tag_lower) < 3:
                continue
            
            # Get or create album for this tag (but don't add media)
            album = self._get_or_create_album(
                owner_id=media.owner_id,
                theme_tag=tag_lower,
                title=tag.title()  # Capitalize
            )
            
            if album:
                created_albums.append(album)
        
        self.db.commit()
        
        logger.info(f"Created/ensured {len(created_albums)} albums for media {media.id} (photos NOT auto-added)")
        return created_albums
    
    def _get_top_tags(self, tags: List[str], max_tags: int = 3) -> List[str]:
        """
        Get top N most relevant tags based on priority weights.
        
        Args:
            tags: List of all tags
            max_tags: Maximum number of tags to return
            
        Returns:
            List of top N tags
        """
        # Score each tag
        scored_tags = []
        for tag in tags:
            tag_lower = tag.lower().strip()
            priority = self.TAG_PRIORITIES.get(tag_lower, 50)  # Default priority 50
            scored_tags.append((tag, priority))
        
        # Sort by priority (highest first)
        scored_tags.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N tags
        return [tag for tag, _ in scored_tags[:max_tags]]
    
    def add_media_to_album(self, album: Album, media_ids: List[int]) -> int:
        """
        Manually add media items to an album.
        
        Args:
            album: Album to add photos to
            media_ids: List of media IDs to add
            
        Returns:
            Number of photos added
        """
        added_count = 0
        
        # Get media items that belong to the album owner
        media_items = self.db.query(Media).filter(
            Media.id.in_(media_ids),
            Media.owner_id == album.owner_id
        ).all()
        
        # Add each media to album if not already present
        for media in media_items:
            if media not in album.media_items.all():
                album.media_items.append(media)
                added_count += 1
        
        # Update album metadata
        album.media_count = album.media_items.count()
        
        # Set cover if not set and we have media
        if not album.cover_media_id and media_items:
            album.cover_media_id = media_items[0].id
        
        self.db.commit()
        
        logger.info(f"Added {added_count} photos to album {album.id}")
        return added_count
    
    def _get_or_create_album(
        self,
        owner_id: int,
        theme_tag: str,
        title: str
    ) -> Optional[Album]:
        """
        Get existing album or create new one for a theme.
        
        Args:
            owner_id: User ID
            theme_tag: Tag/theme identifier (lowercase)
            title: Display title for album
            
        Returns:
            Album instance or None if limit reached
        """
        # Check if album exists
        existing = self.db.query(Album).filter(
            Album.owner_id == owner_id,
            Album.theme_tag == theme_tag
        ).first()
        
        if existing:
            return existing
        
        # Check if we've hit the max albums limit
        user_album_count = self.db.query(func.count(Album.id)).filter(
            Album.owner_id == owner_id,
            Album.is_auto_generated == 1
        ).scalar()
        
        if user_album_count >= self.MAX_AUTO_ALBUMS:
            logger.warning(f"User {owner_id} has reached max albums limit")
            return None
        
        # Create new album
        new_album = Album(
            owner_id=owner_id,
            title=title,
            theme_tag=theme_tag,
            is_auto_generated=1,
            media_count=0
        )
        
        self.db.add(new_album)
        self.db.flush()  # Get ID without committing
        
        logger.info(f"Created new album: {title} (theme: {theme_tag})")
        return new_album
    
    def update_album_descriptions(self, album_id: int) -> bool:
        """
        Generate AI summary for an album based on its media captions.
        
        Args:
            album_id: Album to update
            
        Returns:
            True if successful
        """
        album = self.db.query(Album).filter(Album.id == album_id).first()
        if not album:
            return False
        
        # Get all captions from album's media
        media_items = album.media_items.limit(20).all()  # Sample up to 20
        captions = [m.caption for m in media_items if m.caption]
        
        if not captions:
            album.description = f"Collection of {album.title.lower()} photos"
        else:
            # Generate summary from captions
            album.description = self._generate_album_summary(
                album.title,
                captions,
                album.media_count
            )
        
        self.db.commit()
        return True
    
    def _generate_album_summary(
        self,
        title: str,
        captions: List[str],
        count: int
    ) -> str:
        """
        Generate a natural description for an album.
        
        Args:
            title: Album title
            captions: Sample captions from photos
            count: Total photo count
            
        Returns:
            Generated description
        """
        # Extract common themes from captions
        words = []
        for caption in captions[:10]:  # Sample
            words.extend(caption.lower().split())
        
        # Find most common meaningful words
        common_words = Counter(words).most_common(5)
        themes = [word for word, _ in common_words 
                 if len(word) > 4 and word not in {'with', 'this', 'that', 'from', 'have', 'will'}]
        
        # Build description
        if themes:
            theme_str = ', '.join(themes[:3])
            return f"{count} photos capturing {title.lower()} moments featuring {theme_str}"
        else:
            return f"Collection of {count} {title.lower()} photos"
    
    def merge_similar_albums(self, owner_id: int) -> int:
        """
        Merge albums with similar themes (e.g., "outdoor" + "nature").
        
        Args:
            owner_id: User to optimize albums for
            
        Returns:
            Number of albums merged
        """
        # Get all auto-generated albums
        albums = self.db.query(Album).filter(
            Album.owner_id == owner_id,
            Album.is_auto_generated == 1
        ).all()
        
        # TODO: Implement similarity detection and merging
        # This would use tag similarity or embedding similarity
        # For now, return 0 (not implemented)
        
        return 0
    
    def get_album_suggestions(self, owner_id: int) -> List[Dict[str, Any]]:
        """
        Suggest potential new albums based on unorganized photos.
        
        Args:
            owner_id: User ID
            
        Returns:
            List of suggested album themes
        """
        # Get all processed media
        media_items = self.db.query(Media).filter(
            Media.owner_id == owner_id,
            Media.status == ProcessingStatus.DONE,
            Media.tags.isnot(None)
        ).all()
        
       
        existing_themes = {a.theme_tag for a in self.db.query(Album.theme_tag).filter(
            Album.owner_id == owner_id
        ).all()}
        
        tag_counts = Counter()
        for item in media_items:
            if item.tags:
                for tag in item.tags:
                    tag_lower = tag.lower()
                    if tag_lower not in existing_themes and tag_lower not in self.EXCLUDED_TAGS:
                        tag_counts[tag_lower] += 1
        
        # Return suggestions with enough photos
        suggestions = []
        for tag, count in tag_counts.most_common(10):
            if count >= self.MIN_PHOTOS_FOR_ALBUM:
                suggestions.append({
                    'theme': tag,
                    'title': tag.title(),
                    'photo_count': count
                })
        
        return suggestions
