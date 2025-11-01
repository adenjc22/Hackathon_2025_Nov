from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from users import User
from hashlib import sha256

router = APIRouter()

@router.post("/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    hashed_pw = sha256(password.encode()).hexdigest()
    user = db.query(User).filter(User.username == username, User.password == hashed_pw).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return {"message": "Login successful", "username": user.username}