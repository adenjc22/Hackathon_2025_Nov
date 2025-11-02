from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON, Text, Enum, func, Boolean
from sqlalchemy.orm import relationship
import enum

from app.database.session import Base


class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    ERROR = "error"


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False, unique=True)
    mime_type = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    
    # AI Processing fields
    status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING, nullable=False)
    tags = Column(JSON, nullable=True)  # List of tags from Azure Vision
    emotion = Column(JSON, nullable=True)  # Emotion data from Azure Face
    caption = Column(Text, nullable=True)  # Generated caption from OpenAI
    error_message = Column(Text, nullable=True)  # Error details if status=ERROR
    
    # Phase 4: Semantic Search fields
    embedding = Column(JSON, nullable=True)  # Vector embedding for semantic search (stored as JSON for SQLite)
    search_text = Column(Text, nullable=True)  # Combined searchable text
    has_people = Column(Boolean, default=False, nullable=True)  # Whether image contains people

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    owner = relationship("User", backref="media_items")