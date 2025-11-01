from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.database.models_user import User

router = APIRouter()

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    """Return all users in the database (test route)."""
    users = db.query(User).all()
    result = [
        {"id": u.id, "email": u.email, "created_at": str(u.created_at)}
        for u in users
    ]

    return {"users": result}