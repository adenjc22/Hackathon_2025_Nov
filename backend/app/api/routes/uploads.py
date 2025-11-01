from fastapi import APIRouter, File, UploadFile
from typing import Dict

router = APIRouter()

@router.post("/image")
async def upload_image(file: UploadFile = File(...)) -> Dict[str, str]:
    """Test endpoint for file upload."""
    return {"filename": file.filename, "content_type": file.content_type}
