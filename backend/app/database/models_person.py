from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime, func
from sqlalchemy.orm import relationship
from app.database.session import Base


class Person(Base):
    """Represents a unique person identified through facial recognition."""
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  # User-assigned name
    face_id = Column(String, unique=True, nullable=False)  # Azure Face persistent ID
    thumbnail_url = Column(String, nullable=True)  # Best/first photo of this person
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", backref="persons")
    face_instances = relationship("FaceInstance", back_populates="person")


class FaceInstance(Base):
    """Links a detected face in a photo to a Person."""
    __tablename__ = "face_instances"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False)
    
    # Face detection details from Azure
    face_rectangle = Column(JSON, nullable=True)  # {top, left, width, height}
    face_attributes = Column(JSON, nullable=True)  # emotion, age, gender, etc.
    confidence = Column(Float, nullable=True)  # Similarity confidence
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    person = relationship("Person", back_populates="face_instances")
    media = relationship("Media", backref="faces")
