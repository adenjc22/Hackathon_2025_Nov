from celery import Celery
from app.core.config import settings
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# The .env file is in the backend/ directory
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"Loaded .env from: {env_path}")
else:
    print(f" .env file not found at: {env_path}")

# Get Redis URL from environment or use default
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "legacy_album",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.ai_pipeline"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes max per task
    worker_prefetch_multiplier=1,
    # Windows compatibility - use solo pool instead of prefork
    worker_pool="solo",
)

if __name__ == "__main__":
    celery_app.start()
