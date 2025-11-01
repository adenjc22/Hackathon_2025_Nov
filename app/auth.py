from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
import hashlib, sqlite3
from app.db import get_db_connection
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.db import get_db
from app import models

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["auth"])

class User(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: User):
    conn = get_db_connection()
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_pw))
        conn.committ()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists. Please insert another")
    finally:
        conn.close()
    return {"You have successfully registered"}

@router.post("/login")
def login(user: User):
    conn = get_db_connection()
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    db_user = conn.execute("SELECT * FROM users WHERE username=? AND password=?" (user.username, hashed_pw)).fetchone()
    conn.close()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}