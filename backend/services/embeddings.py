"""
Embedding service using SentenceTransformers
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import logging

from core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Manages text embeddings for RAG"""
    
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.model = None
        self.dimension = settings.EMBEDDING_DIM
    
    async def initialize(self):
        """Load embedding model"""
        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        logger.info(f"✅ Embedding model loaded (dim: {self.dimension})")
    
    def encode(
        self,
        texts: Union[str, List[str]],
        batch_size: int = 32,
        show_progress: bool = False
    ) -> np.ndarray:
        """
        Encode text(s) into embeddings
        
        Args:
            texts: Single text or list of texts
            batch_size: Batch size for encoding
            show_progress: Show progress bar
            
        Returns:
            numpy array of embeddings
        """
        if not self.model:
            raise RuntimeError("Model not initialized. Call initialize() first.")
        
        # Convert single text to list
        is_single = isinstance(texts, str)
        if is_single:
            texts = [texts]
        
        # Encode
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        # Return single embedding if input was single text
        if is_single:
            return embeddings[0]
        
        return embeddings
    
    def similarity(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray
    ) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0-1)
        """
        # Normalize vectors
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        
        # Clip to [0, 1] range
        return float(np.clip(similarity, 0, 1))
    
    def batch_similarity(
        self,
        query_embedding: np.ndarray,
        embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Calculate similarity between query and multiple embeddings
        
        Args:
            query_embedding: Query embedding vector
            embeddings: Array of embedding vectors
            
        Returns:
            Array of similarity scores
        """
        # Normalize query
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        
        # Normalize all embeddings
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings_norm = embeddings / np.maximum(norms, 1e-10)
        
        # Calculate similarities
        similarities = np.dot(embeddings_norm, query_norm)
        
        return np.clip(similarities, 0, 1)