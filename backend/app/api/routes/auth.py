from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models_user import User

from app.core.security import hash_password, verify_password

from app.core.security import hash_password, verify_password
from app.schemas.users import UserCreate, UserLogin, UserOut


from hashlib import sha256



router = APIRouter()

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
            
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash password and save
    new_user = User(email=user_data.email,
                     hashed_password=hash_password(user_data.password))
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "email": new_user.email}

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
   user = db.query(User).filter(User.email == user_data.email).first()

   if not user or not verify_password(user_data.password, user.hashed_password):
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

   return {"message": "Login successful"}