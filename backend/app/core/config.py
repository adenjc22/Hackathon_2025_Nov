from pydantic_settings import BaseSettings, SettingsConfigDict

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

settings = Settings()
