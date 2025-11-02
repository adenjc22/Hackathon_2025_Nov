from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON, func
from sqlalchemy.orm import relationship

from app.database.session import Base


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False, unique=True)
    mime_type = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    metadata_json = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    owner = relationship("User", backref="media_items")