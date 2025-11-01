from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models_user import User
from fastapi import Form


from hashlib import sha256

router = APIRouter()

@router.post("/")
def register(email: str = Form(...),
            password: str = Form(...),
            db: Session = Depends(get_db)):
    
    # Check if user exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash password and save
    hashed_pw = sha256(password.encode()).hexdigest()
    new_user = User(email=email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "email": new_user.email}

