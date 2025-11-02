"""
Embedding Service - Generate vector embeddings using OpenAI
for semantic search capabilities.
"""

import os
from typing import List, Optional
from loguru import logger
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class EmbeddingService:
    """Service for generating text embeddings using OpenAI."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not set - embeddings will not work")
        
        if self.api_key:
            openai.api_key = self.api_key
        # Using text-embedding-3-small for cost efficiency
        # Dimension: 1536 (default for text-embedding-3-small)
        self.model = "text-embedding-3-small"
        self.dimension = 1536
    
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate an embedding vector for the given text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector (1536 dimensions)
            or None if generation fails
        """
        if not self.api_key:
            logger.error("Cannot generate embedding - OPENAI_API_KEY not set")
            return None
        
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return None
        
        try:
            # Call OpenAI embeddings API
            response = openai.embeddings.create(
                model=self.model,
                input=text.strip()
            )
            
            # Extract embedding vector
            embedding = response.data[0].embedding
            
            logger.debug(f"Generated embedding with {len(embedding)} dimensions")
            return embedding
            
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            return None
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        Generate embeddings for multiple texts in a single API call.
        More efficient for processing multiple items.
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            List of embedding vectors (or None for failed items)
        """
        if not self.api_key:
            logger.error("Cannot generate embeddings - OPENAI_API_KEY not set")
            return [None] * len(texts)
        
        if not texts:
            return []
        
        # Filter out empty texts but remember their positions
        text_map = {}
        valid_texts = []
        
        for i, text in enumerate(texts):
            if text and text.strip():
                text_map[len(valid_texts)] = i
                valid_texts.append(text.strip())
        
        if not valid_texts:
            logger.warning("No valid texts provided for batch embedding")
            return [None] * len(texts)
        
        try:
            # Call OpenAI embeddings API with batch
            response = openai.embeddings.create(
                model=self.model,
                input=valid_texts
            )
            
            # Initialize result array with None
            results = [None] * len(texts)
            
            # Map embeddings back to original positions
            for i, embedding_data in enumerate(response.data):
                original_index = text_map[i]
                results[original_index] = embedding_data.embedding
            
            logger.info(f"Generated {len(valid_texts)} embeddings in batch")
            return results
            
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {str(e)}")
            return [None] * len(texts)
    
    def generate_search_text(self, media_item) -> str:
        """
        Generate searchable text from a media item's AI-generated data.
        Combines caption, tags, and emotion data into a single searchable string.
        
        Args:
            media_item: Media database model instance
            
        Returns:
            Combined text suitable for embedding
        """
        parts = []
        
        # Add caption (primary source)
        if media_item.caption:
            parts.append(media_item.caption)
        
        # Add tags
        if media_item.tags and isinstance(media_item.tags, list):
            tag_text = ", ".join(media_item.tags)
            parts.append(f"Tags: {tag_text}")
        
        # Add emotion data
        if media_item.emotion and isinstance(media_item.emotion, dict):
            if "dominant_emotion" in media_item.emotion:
                parts.append(f"Mood: {media_item.emotion['dominant_emotion']}")
            elif "note" not in media_item.emotion:
                # If there are actual emotions (not just a note)
                emotion_names = [k for k in media_item.emotion.keys() if k != "note"]
                if emotion_names:
                    parts.append(f"Emotions: {', '.join(emotion_names)}")
        
        # Combine all parts
        search_text = " | ".join(parts)
        
        if not search_text:
            search_text = "A photo"
        
        return search_text


# Singleton instance
embedding_service = EmbeddingService()
