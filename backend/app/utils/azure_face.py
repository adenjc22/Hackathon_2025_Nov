"""
Azure Face API integration for face detection and emotion analysis.

Microsoft has restricted access to most Azure Face API features (emotion detection, 
age, gender, smile, facial attributes) through their "Limited Access" policy as part 
of Responsible AI initiatives. These features require special approval through an 
application process at https://aka.ms/facerecognition.

We originally planned to use full-scale emotion detection with detailed facial analysis,
but this was not permitted without the Limited Access approval. For this hackathon demo,
we are skipping Face API features and relying on Azure Computer Vision + OpenAI GPT-4 
for comprehensive image analysis and caption generation instead.

If approved in the future, this module can be re-enabled to provide:
- Emotion detection (happiness, sadness, anger, fear, surprise, etc.)
- Age and gender estimation
- Smile intensity and facial hair detection
- Accessories and glasses detection
"""

import os
import requests
from typing import Dict, List, Optional
from loguru import logger
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class AzureFaceAPI:
    """Handles Azure Face API calls for face detection and smile analysis."""
    
    def __init__(self):
        self.api_key = os.getenv("AZURE_FACE_KEY")
        self.endpoint = os.getenv("AZURE_FACE_ENDPOINT")
        
        if not self.api_key or not self.endpoint:
            logger.warning("Azure Face API credentials not configured")
        
        # Remove trailing slash from endpoint if present
        if self.endpoint and self.endpoint.endswith("/"):
            self.endpoint = self.endpoint[:-1]
    
    def detect_emotion(self, image_url: str) -> Dict:
        """
        Detect faces and analyze mood based on smile intensity.
        
        Args:
            image_url: Public URL of the image to analyze
            
        Returns:
            Dictionary containing detected faces and mood indicators
        """
        if not self.api_key or not self.endpoint:
            logger.error("Azure Face API not configured")
            return {
                "faces": [],
                "emotions": {},
                "error": "Azure Face API not configured"
            }
        
        try:
            detect_url = f"{self.endpoint}/face/v1.0/detect"
            
            # Only request attributes that don't require Limited Access
            params = {
                "returnFaceId": "true",
                "returnFaceLandmarks": "false",
                "returnFaceAttributes": "smile,glasses,accessories"
            }
            
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            body = {
                "url": image_url
            }
            
            logger.info(f"Detecting faces: {image_url}")
            response = requests.post(
                detect_url,
                params=params,
                headers=headers,
                json=body,
                timeout=30
            )
            
            response.raise_for_status()
            faces = response.json()
            
            if not faces:
                logger.info("No faces detected in image")
                return {
                    "faces": [],
                    "emotions": {},
                    "face_count": 0
                }
            
            # Process faces and derive mood from smile
            face_details = []
            smile_values = []
            
            for face in faces:
                attributes = face.get("faceAttributes", {})
                smile_value = attributes.get("smile", 0)
                
                # Derive mood from smile intensity
                if smile_value > 0.6:
                    mood = "happy"
                elif smile_value > 0.3:
                    mood = "pleasant"
                else:
                    mood = "neutral"
                
                face_info = {
                    "smile": smile_value,
                    "mood": mood,
                    "glasses": attributes.get("glasses"),
                    "accessories": attributes.get("accessories", [])
                }
                
                face_details.append(face_info)
                smile_values.append(smile_value)
            
            # Calculate average smile across all faces
            avg_smile = sum(smile_values) / len(smile_values) if smile_values else 0
            
            # Determine overall mood
            if avg_smile > 0.6:
                overall_mood = "joyful"
            elif avg_smile > 0.3:
                overall_mood = "cheerful"
            else:
                overall_mood = "calm"
            
            # Format emotions dict to be compatible with existing code
            emotions = {
                "smile_intensity": avg_smile,
                "overall_mood": overall_mood,
                "happiness": avg_smile,  # Map smile to happiness for compatibility
            }
            
            result = {
                "faces": face_details,
                "emotions": emotions,
                "dominant_emotion": overall_mood,
                "face_count": len(faces),
            }
            
            logger.info(f"Successfully detected {len(faces)} face(s), mood: {overall_mood}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Azure Face API request failed: {str(e)}")
            return {
                "faces": [],
                "emotions": {},
                "error": f"API request failed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error in Azure Face detection: {str(e)}")
            return {
                "faces": [],
                "emotions": {},
                "error": f"Unexpected error: {str(e)}"
            }
    
    def detect_emotion_from_file(self, file_path: str) -> Dict:
        """
        Detect faces and analyze mood from a local image file.
        
        Args:
            file_path: Local path to the image file
            
        Returns:
            Dictionary containing detected faces and mood indicators
        """
        if not self.api_key or not self.endpoint:
            logger.error("Azure Face API not configured")
            return {
                "faces": [],
                "emotions": {},
                "error": "Azure Face API not configured"
            }
        
        try:
            detect_url = f"{self.endpoint}/face/v1.0/detect"
            
            # Only request attributes that don't require Limited Access
            params = {
                "returnFaceId": "true",
                "returnFaceLandmarks": "false",
                "returnFaceAttributes": "smile,glasses,accessories"
            }
            
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Content-Type": "application/octet-stream"
            }
            
            with open(file_path, "rb") as image_file:
                image_data = image_file.read()
            
            logger.info(f"Detecting faces in local image: {file_path}")
            response = requests.post(
                detect_url,
                params=params,
                headers=headers,
                data=image_data,
                timeout=30
            )
            
            response.raise_for_status()
            faces = response.json()
            
            if not faces:
                return {
                    "faces": [],
                    "emotions": {},
                    "face_count": 0
                }
            
            # Process faces and derive mood from smile
            face_details = []
            smile_values = []
            
            for face in faces:
                attributes = face.get("faceAttributes", {})
                smile_value = attributes.get("smile", 0)
                
                # Derive mood from smile intensity
                if smile_value > 0.6:
                    mood = "happy"
                elif smile_value > 0.3:
                    mood = "pleasant"
                else:
                    mood = "neutral"
                
                face_info = {
                    "smile": smile_value,
                    "mood": mood,
                    "glasses": attributes.get("glasses"),
                    "accessories": attributes.get("accessories", [])
                }
                
                face_details.append(face_info)
                smile_values.append(smile_value)
            
            # Calculate average smile across all faces
            avg_smile = sum(smile_values) / len(smile_values) if smile_values else 0
            
            # Determine overall mood
            if avg_smile > 0.6:
                overall_mood = "joyful"
            elif avg_smile > 0.3:
                overall_mood = "cheerful"
            else:
                overall_mood = "calm"
            
            # Format emotions dict to be compatible with existing code
            emotions = {
                "smile_intensity": avg_smile,
                "overall_mood": overall_mood,
                "happiness": avg_smile,  # Map smile to happiness for compatibility
            }
            
            result = {
                "faces": face_details,
                "emotions": emotions,
                "dominant_emotion": overall_mood,
                "face_count": len(faces),
            }
            
            logger.info(f"Successfully detected {len(faces)} face(s), mood: {overall_mood}")
            return result
            
        except Exception as e:
            logger.error(f"Error detecting faces in file: {str(e)}")
            return {
                "faces": [],
                "emotions": {},
                "error": f"Error: {str(e)}"
            }


# Singleton instance
azure_face = AzureFaceAPI()
