"""
AI Pipeline for processing media files with various AI services
"""
from pathlib import Path
from typing import Dict, Optional
from app.services.azure_face import azure_face_service
from app.database.models_media import Media
from app.database.session import SessionLocal
import json


class AIPipeline:
    """Orchestrates AI analysis for uploaded media"""
    
    def __init__(self):
        self.azure_face = azure_face_service
    
    def process_image(self, media_id: int, file_path: Path) -> Dict:
        """
        Process an image through the AI pipeline.
        
        Steps:
        1. Emotion detection (Azure Face API)
        2. Tagging & captioning (future: Azure Computer Vision)
        3. Update database with results
        
        Args:
            media_id: Database ID of the media record
            file_path: Path to the uploaded image file
        
        Returns:
            Dictionary with all analysis results
        """
        results = {
            'media_id': media_id,
            'emotions': None,
            'tags': [],
            'caption': None,
            'error': None
        }
        
        try:
            # Step 1: Emotion detection with Azure Face API
            if self.azure_face:
                print(f"Analyzing emotions for media {media_id}...")
                emotion_data = self.azure_face.analyze_emotions(file_path)
                results['emotions'] = emotion_data
                
                # Extract tags from emotion analysis
                if emotion_data['face_count'] > 0:
                    results['tags'].append(f"{emotion_data['face_count']} face(s)")
                    results['tags'].append(emotion_data['dominant_emotion'])
            
            # Step 2: Update database with results
            self._update_media_record(media_id, results)
            
            print(f"✅ Successfully processed media {media_id}")
            return results
            
        except Exception as e:
            print(f"❌ Error processing media {media_id}: {e}")
            results['error'] = str(e)
            self._update_media_record(media_id, results, status='error')
            return results
    
    def _update_media_record(
        self, 
        media_id: int, 
        results: Dict,
        status: str = 'done'
    ):
        """Update the media record in the database with AI results"""
        db = SessionLocal()
        try:
            media = db.query(Media).filter(Media.id == media_id).first()
            if not media:
                print(f"Media {media_id} not found in database")
                return
            
            # Update status
            media.status = status
            
            # Store AI results in metadata_json
            metadata = json.loads(media.metadata_json) if media.metadata_json else {}
            metadata['ai_analysis'] = {
                'emotions': results.get('emotions'),
                'tags': results.get('tags', []),
                'caption': results.get('caption'),
                'error': results.get('error')
            }
            media.metadata_json = json.dumps(metadata)
            
            db.commit()
            print(f"Updated media {media_id} with AI results")
            
        except Exception as e:
            print(f"Error updating media record: {e}")
            db.rollback()
        finally:
            db.close()


# Create singleton instance
ai_pipeline = AIPipeline()