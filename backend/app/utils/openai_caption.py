"""
OpenAI GPT-4 integration for generating natural language captions.
Combines vision tags and emotion data to create descriptive captions.
"""

import os
from typing import Dict, List, Optional
from openai import OpenAI
from loguru import logger


class OpenAICaptionGenerator:
    """Handles OpenAI API calls for generating image captions."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            logger.warning("OpenAI API key not configured")
    
    def generate_caption(
        self, 
        tags: List[str], 
        emotions: Dict[str, float],
        description: Optional[str] = None
    ) -> str:
        """
        Generate a natural language caption using GPT-4.
        
        Args:
            tags: List of image tags from Azure Vision
            emotions: Dictionary of emotions from Azure Face
            description: Optional description from Azure Vision
            
        Returns:
            Generated caption string
        """
        if not self.client:
            logger.error("OpenAI API not configured")
            return "Unable to generate caption: API not configured"
        
        try:
            # Build context from available data
            context_parts = []
            
            if description:
                context_parts.append(f"Image description: {description}")
            
            if tags:
                tags_str = ", ".join(tags[:10])  # Top 10 tags
                context_parts.append(f"Detected elements: {tags_str}")
            
            if emotions:
                # Find dominant emotion
                dominant_emotion = max(emotions, key=emotions.get) if emotions else None
                if dominant_emotion and emotions[dominant_emotion] > 0.3:
                    emotion_score = emotions[dominant_emotion]
                    context_parts.append(
                        f"Detected emotion: {dominant_emotion} ({emotion_score:.0%} confidence)"
                    )
            
            if not context_parts:
                return "A moment captured in time."
            
            context = "\n".join(context_parts)
            
            # Create prompt for GPT-4
            prompt = f"""Based on the following image analysis, create a natural, engaging caption (2-3 sentences max) that describes what's happening in the photo. Be descriptive but concise, and incorporate the emotional context if present.
            {context} Generate a caption that sounds natural and human-like, as if you're describing the photo to a friend. Focus on the story or moment being captured."""
            
            logger.info("Generating caption with OpenAI GPT-4")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a creative photo caption writer who creates engaging, natural-sounding descriptions of images. Your captions are warm, descriptive, and capture the essence of the moment."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=150,
                temperature=0.7,
                n=1
            )
            
            caption = response.choices[0].message.content.strip()
            logger.info(f"Successfully generated caption: {caption[:50]}...")
            
            return caption
            
        except Exception as e:
            logger.error(f"Error generating caption with OpenAI: {str(e)}")
            
            # Fallback: create basic caption from tags
            if tags:
                return f"A photo featuring {', '.join(tags[:3])}."
            elif description:
                return description
            else:
                return "A memorable moment."
    
    def generate_caption_simple(self, tags: List[str]) -> str:
        """
        Generate a simple caption from tags without API call.
        Useful as a fallback or for testing.
        
        Args:
            tags: List of image tags
            
        Returns:
            Simple caption string
        """
        if not tags:
            return "A photo."
        
        if len(tags) == 1:
            return f"A photo of {tags[0]}."
        elif len(tags) == 2:
            return f"A photo of {tags[0]} and {tags[1]}."
        else:
            main_tags = tags[:3]
            return f"A photo featuring {', '.join(main_tags[:-1])}, and {main_tags[-1]}."


# Singleton instance
openai_caption = OpenAICaptionGenerator()
