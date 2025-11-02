# backend/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Legacy Album"
    debug: bool = True

    # your backend vars (add more as needed)
    database_url: str = "sqlite:///./legacy_album.db"
    secret_key: str = "change-me"
    allowed_origins: str = "http://localhost:5173"

    # tell Pydantic where to read and to ignore unknown keys (e.g. VITE_*)
    model_config = SettingsConfigDict(
        env_file="backend/.env",   # path relative to your cwd when you run uvicorn
        extra="ignore"
    )

settings = Settings()
