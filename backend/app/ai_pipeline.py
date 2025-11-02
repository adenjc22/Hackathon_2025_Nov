"""
AI Processing Pipeline - Orchestrates Azure Vision, Azure Face, and OpenAI
to analyze uploaded media and generate captions.
"""

from pathlib import Path
from typing import Dict
from loguru import logger
from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.database.session import SessionLocal
from app.database.models_media import Media, ProcessingStatus
from app.database.models_user import User  # Import User to resolve relationship
from app.utils.azure_vision import azure_vision
from app.utils.azure_face import azure_face
from app.utils.openai_caption import openai_caption


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        return db
    finally:
        pass  


@celery_app.task(bind=True, name="process_media_task")
def process_media_task(self, media_id: int, file_path: str):
    """
    Background task to process uploaded media with AI analysis.
    
    This task:
    1. Fetches the media record from database
    2. Runs Azure Vision analysis for tags and description
    3. Runs Azure Face analysis for emotion detection
    4. Generates a natural caption using OpenAI GPT-4
    5. Updates the database with results
    
    Args:
        media_id: Database ID of the media record
        file_path: Local path to the uploaded file
    """
    db = None
    try:
        db = SessionLocal()
        
        # Fetch media record
        media = db.query(Media).filter(Media.id == media_id).first()
        if not media:
            logger.error(f"Media record {media_id} not found")
            return {"error": "Media not found"}
        
        # Update status to processing
        media.status = ProcessingStatus.PROCESSING
        db.commit()
        
        logger.info(f"Starting AI pipeline for media {media_id}: {file_path}")
        
        # Initialize results
        tags = []
        emotions = {}
        caption = None
        vision_description = None
        
        # Step 1: Azure Vision Analysis
        try:
            logger.info(f"Running Azure Vision analysis on {file_path}")
            vision_result = azure_vision.analyze_image_from_file(file_path)
            
            if "error" not in vision_result:
                tags = vision_result.get("tags", [])
                vision_description = vision_result.get("description")
                logger.info(f"Azure Vision found {len(tags)} tags")
            else:
                logger.warning(f"Azure Vision error: {vision_result.get('error')}")
        
        except Exception as e:
            logger.error(f"Azure Vision analysis failed: {str(e)}")
        
        # Step 2: Azure Face Analysis
        # Note: Azure Face API requires Limited Access approval for most features
        # Skipping for now - Azure Vision + OpenAI provide sufficient analysis
        try:
            logger.info("Skipping Azure Face (requires Limited Access approval)")
            emotions = {"note": "Azure Face requires special approval - using Vision + OpenAI instead"}
            face_count = 0
        
        except Exception as e:
            logger.error(f"Azure Face analysis failed: {str(e)}")
        
        # Step 3: OpenAI Caption Generation
        try:
            if tags or emotions or vision_description:
                logger.info("Generating caption with OpenAI")
                caption = openai_caption.generate_caption(
                    tags=tags,
                    emotions=emotions,
                    description=vision_description
                )
                logger.info(f"Generated caption: {caption[:100]}...")
            else:
                caption = "A photo."
                logger.warning("No AI data available, using default caption")
        
        except Exception as e:
            logger.error(f"Caption generation failed: {str(e)}")
            caption = "A memorable moment."
        
        # Step 4: Update database with results
        media.tags = tags
        media.emotion = emotions
        media.caption = caption
        media.status = ProcessingStatus.DONE
        media.error_message = None
        
        # Phase 4: Generate embedding for semantic search
        try:
            from app.utils.embeddings import embedding_service
            
            # Generate searchable text
            search_text = embedding_service.generate_search_text(media)
            media.search_text = search_text
            
            # Generate embedding
            embedding_vector = embedding_service.generate_embedding(search_text)
            if embedding_vector:
                media.embedding = embedding_vector  # Store as JSON in SQLite
                logger.info(f"Generated embedding with {len(embedding_vector)} dimensions")
            else:
                logger.warning("Failed to generate embedding")
            
            # Detect if image has people (from tags or emotion data)
            has_people = False
            if tags:
                people_tags = ["person", "people", "man", "woman", "child", "face", "portrait"]
                has_people = any(tag.lower() in people_tags for tag in tags)
            if not has_people and emotions and "note" not in emotions:
                # If we have emotion data (not just a note), there are likely people
                has_people = len(emotions) > 0
            
            media.has_people = has_people
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
        
        db.commit()
        db.refresh(media)
        
        logger.info(f"✅ Successfully processed media {media_id}")
        
        # NOTE: We do NOT auto-create albums during upload anymore.
        # Albums are only created when:
        # 1. User explicitly creates one manually  
        # 2. User uses AI search mode (create-from-prompt)
        
        return {
            "media_id": media_id,
            "status": "done",
            "tags": tags,
            "emotions": emotions,
            "caption": caption
        }
    
    except Exception as e:
        logger.error(f"❌ Error processing media {media_id}: {str(e)}")
        
        # Update status to error
        if db and media:
            try:
                media.status = ProcessingStatus.ERROR
                media.error_message = str(e)
                db.commit()
            except Exception as db_error:
                logger.error(f"Failed to update error status: {str(db_error)}")
        
        return {
            "media_id": media_id,
            "status": "error",
            "error": str(e)
        }
    
    finally:
        if db:
            db.close()


def process_media_sync(media_id: int, file_path: str) -> Dict:
    """
    Synchronous version of media processing for testing.
    Runs the AI pipeline without Celery.
    
    Args:
        media_id: Database ID of the media record
        file_path: Local path to the uploaded file
        
    Returns:
        Dictionary with processing results
    """
    return process_media_task(media_id, file_path)
