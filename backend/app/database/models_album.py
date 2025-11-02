"""
Album Model - AI-Generated Smart Albums
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Table, func
from sqlalchemy.orm import relationship

from app.database.session import Base


# Association table for many-to-many relationship between albums and media
album_media = Table(
    'album_media',
    Base.metadata,
    Column('album_id', Integer, ForeignKey('albums.id'), primary_key=True),
    Column('media_id', Integer, ForeignKey('media.id'), primary_key=True)
)


class Album(Base):
    """
    Smart Album Model - Automatically created based on AI tags and themes
    """
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Album metadata
    title = Column(String, nullable=False)  # e.g., "Beach", "Friends", "Nature"
    theme_tag = Column(String, nullable=False, index=True)  # The dominant tag/theme (lowercase)
    description = Column(Text, nullable=True)  # AI-generated album summary
    
    # Album appearance
    cover_media_id = Column(Integer, ForeignKey("media.id"), nullable=True)  # Representative cover image
    
    # Auto-generation metadata
    is_auto_generated = Column(Integer, default=1)  # 1 for auto, 0 for manual
    media_count = Column(Integer, default=0)  # Cached count for performance
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    owner = relationship("User", backref="albums")
    cover_media = relationship("Media", foreign_keys=[cover_media_id])
    media_items = relationship(
        "Media",
        secondary=album_media,
        backref="albums",
        lazy='dynamic'
    )

    def __repr__(self):
        return f"<Album(id={self.id}, title='{self.title}', theme='{self.theme_tag}', count={self.media_count})>"
