from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(prefix="/ai-config", tags=["AI Configuration"])


@router.get("/status")
async def get_ai_config_status():
    """
    Check which AI services are configured with valid API keys.
    Public endpoint - no authentication required for checking config.
    """
    validation = settings.validate_ai_keys()
    available_services = [service for service, available in validation.items() if available]
    
    return {
        "services": validation,
        "available": available_services,
        "count": len(available_services),
        "message": f"{len(available_services)} AI service(s) configured"
    }
