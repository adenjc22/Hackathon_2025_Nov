from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.database.session import get_db
from app.database.models_person import Person, FaceInstance


router = APIRouter(prefix="/people", tags=["People"])


# Schemas
class PersonBase(BaseModel):
    name: Optional[str] = None


class PersonCreate(PersonBase):
    face_id: str
    thumbnail_url: Optional[str] = None


class PersonUpdate(BaseModel):
    name: str


class FaceInstanceRead(BaseModel):
    id: int
    media_id: int
    face_rectangle: Optional[dict] = None
    confidence: Optional[float] = None
    
    class Config:
        from_attributes = True


class PersonRead(PersonBase):
    id: int
    face_id: str
    thumbnail_url: Optional[str] = None
    photo_count: int = 0  # Number of photos this person appears in
    created_at: datetime
    
    class Config:
        from_attributes = True


class PersonDetailRead(PersonRead):
    face_instances: List[FaceInstanceRead] = []
    
    class Config:
        from_attributes = True


# Routes
@router.get("/", response_model=List[PersonRead])
async def list_people(db: Session = Depends(get_db)):
    """Get all recognized people with photo counts."""
    people = db.query(Person).all()
    
    result = []
    for person in people:
        person_data = PersonRead.from_orm(person)
        person_data.photo_count = len(person.face_instances)
        result.append(person_data)
    
    return result


@router.get("/{person_id}", response_model=PersonDetailRead)
async def get_person(person_id: int, db: Session = Depends(get_db)):
    """Get a specific person with all their face instances."""
    person = db.query(Person).filter(Person.id == person_id).first()
    
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    return person


@router.patch("/{person_id}", response_model=PersonRead)
async def update_person_name(person_id: int, data: PersonUpdate, db: Session = Depends(get_db)):
    """Update a person's name."""
    person = db.query(Person).filter(Person.id == person_id).first()
    
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    person.name = data.name
    db.commit()
    db.refresh(person)
    
    person_data = PersonRead.from_orm(person)
    person_data.photo_count = len(person.face_instances)
    
    return person_data


@router.delete("/{person_id}")
async def delete_person(person_id: int, db: Session = Depends(get_db)):
    """Delete a person and all their face instances."""
    person = db.query(Person).filter(Person.id == person_id).first()
    
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # Delete all face instances
    db.query(FaceInstance).filter(FaceInstance.person_id == person_id).delete()
    
    # Delete person
    db.delete(person)
    db.commit()
    
    return {"message": "Person deleted successfully"}


@router.get("/{person_id}/photos", response_model=List[int])
async def get_person_photos(person_id: int, db: Session = Depends(get_db)):
    """Get all media IDs where this person appears."""
    person = db.query(Person).filter(Person.id == person_id).first()
    
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    media_ids = [fi.media_id for fi in person.face_instances]
    return media_ids


@router.post("/merge")
async def merge_people(person_id_1: int, person_id_2: int, db: Session = Depends(get_db)):
    """Merge two people (in case of duplicates)."""
    person1 = db.query(Person).filter(Person.id == person_id_1).first()
    person2 = db.query(Person).filter(Person.id == person_id_2).first()
    
    if not person1 or not person2:
        raise HTTPException(status_code=404, detail="One or both persons not found")
    
    # Move all face instances from person2 to person1
    db.query(FaceInstance).filter(FaceInstance.person_id == person_id_2).update(
        {"person_id": person_id_1}
    )
    
    # Delete person2
    db.delete(person2)
    db.commit()
    
    return {"message": f"Merged person {person_id_2} into {person_id_1}"}
