from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models_user import User
from hashlib import sha256
from fastapi import Form


router = APIRouter()

@router.post("/")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_pw = sha256(password.encode()).hexdigest()
    user = db.query(User).filter(User.email == email, User.hashed_password == hashed_pw).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return {"message": "Login successful", "email": user.email}