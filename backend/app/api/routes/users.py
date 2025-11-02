from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models_user import User
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/")
def list_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Return all users (requires authentication)."""
    users = db.query(User).all()
    result = [
        {"id": u.id, "email": u.email, "created_at": str(u.created_at)}
        for u in users
    ]

    return {"users": result}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.email.split("@")[0]
    }