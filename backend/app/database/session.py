from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


# SQLite file stored in project root
DATABASE_URL = "sqlite:///./legacy_album.db"

# Engine connects SQLAlchemy to SQLite
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is used by model classes to define tables
Base = declarative_base()

from contextlib import contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
