from fastapi import APIRouter
from app.schemas.common import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
def health():
    """Basic health-check endpoint."""
    return HealthResponse(status="ok", version="0.1.0")
