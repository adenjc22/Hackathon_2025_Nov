"""
Azure Computer Vision API integration for image analysis.
Extracts tags, descriptions, and scene information from images.
"""

import os
import requests
from typing import Dict, List, Optional
from loguru import logger


class AzureVisionAPI:
    """Handles Azure Computer Vision API calls for image analysis."""
    
    def __init__(self):
        self.api_key = os.getenv("AZURE_VISION_KEY")
        self.endpoint = os.getenv("AZURE_VISION_ENDPOINT")
        
        if not self.api_key or not self.endpoint:
            logger.warning("Azure Vision API credentials not configured")
        
        # Remove trailing slash from endpoint if present
        if self.endpoint and self.endpoint.endswith("/"):
            self.endpoint = self.endpoint[:-1]
    
    def analyze_image(self, image_url: str) -> Dict:
        """
        Analyze an image using Azure Computer Vision API.
        
        Args:
            image_url: Public URL of the image to analyze
            
        Returns:
            Dictionary containing tags, description, and metadata
        """
        if not self.api_key or not self.endpoint:
            logger.error("Azure Vision API not configured")
            return {
                "tags": [],
                "description": None,
                "error": "Azure Vision API not configured"
            }
        
        try:
            # Build the analyze endpoint
            analyze_url = f"{self.endpoint}/vision/v3.2/analyze"
            
            # Define visual features to extract
            params = {
                "visualFeatures": "Tags,Description,Categories,Color,Objects",
                "details": "Landmarks",
                "language": "en"
            }
            
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            body = {
                "url": image_url
            }
            
            logger.info(f"Analyzing image with Azure Vision: {image_url}")
            response = requests.post(
                analyze_url,
                params=params,
                headers=headers,
                json=body,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Extract tags
            tags = [tag["name"] for tag in data.get("tags", [])]
            
            # Extract description
            descriptions = data.get("description", {}).get("captions", [])
            description = descriptions[0]["text"] if descriptions else None
            
            # Extract categories
            categories = [cat["name"] for cat in data.get("categories", [])]
            
            # Extract color info
            color_info = data.get("color", {})
            dominant_colors = color_info.get("dominantColors", [])
            
            # Extract objects
            objects = [obj["object"] for obj in data.get("objects", [])]
            
            result = {
                "tags": tags[:10],  # Top 10 tags
                "description": description,
                "categories": categories,
                "dominant_colors": dominant_colors,
                "objects": objects,
                "raw_response": data
            }
            
            logger.info(f"Successfully analyzed image: {len(tags)} tags found")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Azure Vision API request failed: {str(e)}")
            return {
                "tags": [],
                "description": None,
                "error": f"API request failed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error in Azure Vision analysis: {str(e)}")
            return {
                "tags": [],
                "description": None,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def analyze_image_from_file(self, file_path: str) -> Dict:
        """
        Analyze an image file using Azure Computer Vision API.
        
        Args:
            file_path: Local path to the image file
            
        Returns:
            Dictionary containing tags, description, and metadata
        """
        if not self.api_key or not self.endpoint:
            logger.error("Azure Vision API not configured")
            return {
                "tags": [],
                "description": None,
                "error": "Azure Vision API not configured"
            }
        
        try:
            analyze_url = f"{self.endpoint}/vision/v3.2/analyze"
            
            params = {
                "visualFeatures": "Tags,Description,Categories,Color,Objects",
                "details": "Landmarks",
                "language": "en"
            }
            
            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key,
                "Content-Type": "application/octet-stream"
            }
            
            with open(file_path, "rb") as image_file:
                image_data = image_file.read()
            
            logger.info(f"Analyzing local image with Azure Vision: {file_path}")
            response = requests.post(
                analyze_url,
                params=params,
                headers=headers,
                data=image_data,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Extract same information as URL method
            tags = [tag["name"] for tag in data.get("tags", [])]
            descriptions = data.get("description", {}).get("captions", [])
            description = descriptions[0]["text"] if descriptions else None
            categories = [cat["name"] for cat in data.get("categories", [])]
            color_info = data.get("color", {})
            dominant_colors = color_info.get("dominantColors", [])
            objects = [obj["object"] for obj in data.get("objects", [])]
            
            result = {
                "tags": tags[:10],
                "description": description,
                "categories": categories,
                "dominant_colors": dominant_colors,
                "objects": objects,
                "raw_response": data
            }
            
            logger.info(f"Successfully analyzed image: {len(tags)} tags found")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing image file: {str(e)}")
            return {
                "tags": [],
                "description": None,
                "error": f"Error: {str(e)}"
            }


# Singleton instance
azure_vision = AzureVisionAPI()
