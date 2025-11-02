import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Legacy Album"
    debug: bool = True
    secret_key: str = "your-secret-key-change-this-in-production-min-32-chars"
    database_url: str = "sqlite:///./legacy_album.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hackathon.db")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    AZURE_FACE_KEY: str = os.getenv("AZURE_FACE_KEY", "")
    AZURE_FACE_ENDPOINT: str = os.getenv("AZURE_FACE_ENDPOINT", "")
    
    AZURE_COMPUTER_VISION_KEY: str = os.getenv("AZURE_COMPUTER_VISION_KEY", "")
    AZURE_COMPUTER_VISION_ENDPOINT: str = os.getenv("AZURE_COMPUTER_VISION_ENDPOINT", "")
    
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_MIME_TYPES: list = os.getenv(
        "ALLOWED_MIME_TYPES", 
        "image/jpeg,image/png"
    ).split(",")

    UPLOAD_DIR: Path = Path("uploads")

    @classmethod
    def validate_ai_keys(cls) -> dict:
        """Check which AI service keys are configured"""
        return {
            "azure_face": bool(cls.AZURE_FACE_KEY and cls.AZURE_FACE_ENDPOINT),
            "azure_vision": bool(cls.AZURE_COMPUTER_VISION_KEY and cls.AZURE_COMPUTER_VISION_ENDPOINT),
        }
    
    @classmethod
    def get_available_services(cls) -> list:
        """Get list of available AI services"""
        validation = cls.validate_ai_keys()
        return [service for service, available in validation.items() if available]

settings = Settings()
