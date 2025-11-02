import requests
from typing import Dict, List, Optional
from pathlib import Path
from app.core.config import settings

class AzureFaceService:
    def __init__(self):
        self.key = settings.AZURE_FACE_KEY
        self.endpoint = settings.AZURE_FACE_ENDPOINT
        self.detect_url = f"{self.endpoint}/face/v1.0/detect"

        if not self.key or not self.endpoint:
            raise ValueError("Azure Face API credentials not configured")
    
    def detect_faces(
        self, 
        image_path: Path,
        return_face_attributes: Optional[List[str]] = None
    ) -> List[Dict]:
        """Detect faces in an image and return face attributes."""
        if return_face_attributes is None:
            return_face_attributes = ['emotion', 'age', 'gender', 'smile']

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Content-Type': 'application/octet-stream'
        }

        params = {
            'returnFaceId': 'true',
            'returnFaceAttributes': ','.join(return_face_attributes),
            'returnFaceLandmarks': 'false'
        }

        try:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

            response = requests.post(
                self.detect_url,
                headers=headers,
                params=params,
                data=image_data,
                timeout=30
            )
            response.raise_for_status()

            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Azure Face API error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")    
            raise

    def analyze_emotions(self, image_path: Path) -> Dict:
        faces = self.detect_faces(image_path, return_face_attributes=['emotion'])
        
        if not faces:
            return {
                'face_count': 0,
                'dominant_emotion': 'none',
                'emotions': {},
                'faces': []
            }
        
        # Aggregate emotions across all faces
        all_emotions = {}
        for face in faces:
            emotions = face.get('faceAttributes', {}).get('emotion', {})
            for emotion, score in emotions.items():
                all_emotions[emotion] = all_emotions.get(emotion, 0) + score
        
        # Calculate average emotions
        face_count = len(faces)
        avg_emotions = {k: v / face_count for k, v in all_emotions.items()}
        
        # Find dominant emotion
        dominant_emotion = max(avg_emotions.items(), key=lambda x: x[1])[0] if avg_emotions else 'neutral'
        
        return {
            'face_count': face_count,
            'dominant_emotion': dominant_emotion,
            'emotions': avg_emotions,
            'faces': faces
        }
    
    def get_face_attributes(self, image_path: Path) -> Dict:
        faces = self.detect_faces(
            image_path, 
            return_face_attributes=['emotion', 'age', 'gender', 'smile', 'glasses']
        )
        
        if not faces:
            return {
                'face_count': 0,
                'faces': []
            }
        
        # Extract and format face attributes
        face_data = []
        for face in faces:
            attrs = face.get('faceAttributes', {})
            emotions = attrs.get('emotion', {})
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else 'neutral'
            
            face_data.append({
                'age': attrs.get('age'),
                'gender': attrs.get('gender'),
                'smile': attrs.get('smile', 0),
                'glasses': attrs.get('glasses', 'NoGlasses'),
                'emotions': emotions,
                'dominant_emotion': dominant_emotion
            })
        
        return {
            'face_count': len(faces),
            'faces': face_data
        }
    
azure_face_service = AzureFaceService() if settings.AZURE_FACE_KEY else None
