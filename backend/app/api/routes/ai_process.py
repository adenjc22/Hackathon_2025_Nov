from fastapi import APIRouter, Depends, HTTPException
from pathlib import Path
from app.services.ai_pipeline import ai_pipeline
from app.database.session import SessionLocal
from app.database.models_media import Media
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Processing"])


@router.post("/process/{media_id}")
async def process_media(
    media_id: int,
    current_user = Depends(get_current_user)
):
    db = SessionLocal()
    try:
        # Get media record
        media = db.query(Media).filter(Media.id == media_id).first()
        if not media:
            raise HTTPException(status_code=404, detail="Media not found")
        
        # Check if user owns this media
        if media.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Get file path
        file_path = Path(media.stored_path)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found on disk")
        
        # Process with AI pipeline
        results = ai_pipeline.process_image(media_id, file_path)
        
        return {
            "message": "AI processing complete",
            "media_id": media_id,
            "results": results
        }
        
    finally:
        db.close()


@router.get("/results/{media_id}")
async def get_ai_results(
    media_id: int,
    current_user = Depends(get_current_user)
):
    """Get AI analysis results for a media file"""
    db = SessionLocal()
    try:
        media = db.query(Media).filter(Media.id == media_id).first()
        if not media:
            raise HTTPException(status_code=404, detail="Media not found")
        
        if media.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        import json
        metadata = json.loads(media.metadata_json) if media.metadata_json else {}
        
        return {
            "media_id": media_id,
            "status": media.status,
            "ai_analysis": metadata.get('ai_analysis', {}),
            "file_name": media.file_name
        }
        
    finally:
        db.close()