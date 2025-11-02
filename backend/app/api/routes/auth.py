from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.database.session import get_db
from app.database.models_user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_current_user


router = APIRouter()


@router.post("/register")
def register(
    email: EmailStr = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Create a new user and return JWT token."""
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(email=email, hashed_password=hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create JWT token
    access_token = create_access_token(data={"sub": new_user.id})

    return {
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "name": new_user.email.split("@")[0]
        },
        "accessToken": access_token
    }


@router.post("/login")
def login(
    email: EmailStr = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Validate credentials and return JWT token."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": user.id})

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.email.split("@")[0]
        },
        "accessToken": access_token
    }


@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user info."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.email.split("@")[0]
    }


@router.post("/logout")
def logout():
    """Logout endpoint (token invalidation handled client-side)."""
    return {"message": "Logged out successfully"}
