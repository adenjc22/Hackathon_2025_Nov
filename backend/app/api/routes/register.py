from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from users import User
from hashlib import sha256

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/")
def register(username: str, password: str, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password and save
    hashed_pw = sha256(password.encode()).hexdigest()
    new_user = User(username=username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "username": new_user.username}