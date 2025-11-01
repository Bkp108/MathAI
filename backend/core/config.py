"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os
import json
from pathlib import Path


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # API Keys
    GEMINI_API_KEY: str
    TAVILY_API_KEY: str

    # Database
    DATABASE_URL: str = "sqlite:///./data/feedback.db"

    # Qdrant
    QDRANT_MEMORY: bool = True
    QDRANT_PATH: str = "./data/qdrant_storage"
    QDRANT_COLLECTION: str = "math_problems"

    # Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384

    # RAG Configuration
    KB_CONFIDENCE_THRESHOLD: float = 0.5
    KB_TOP_K: int = 3
    WEB_SEARCH_MAX_RESULTS: int = 3

    # Server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    FRONTEND_PORT: int = 5173

    # CORS - Store as JSON string in env
    CORS_ORIGINS: str = '["http://localhost:5173","http://localhost:3000","http://127.0.0.1:5173"]'
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS JSON string to list"""
        try:
            return json.loads(self.CORS_ORIGINS)
        except json.JSONDecodeError:
            # Fallback: split by comma if not valid JSON
            return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]

    # Logging
    LOG_LEVEL: str = "INFO"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # Guardrails
    ENABLE_GUARDRAILS: bool = True
    MAX_QUERY_LENGTH: int = 500

    # Feedback
    ENABLE_FEEDBACK_LEARNING: bool = True
    MIN_POSITIVE_RATING: int = 4

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 30

    # Development
    DEBUG_MODE: bool = False
    SHOW_STACK_TRACES: bool = False

    class Config:
        # Look for .env file in parent directory (project root)
        env_file = "../.env"
        env_file_encoding = 'utf-8'
        case_sensitive = True
        # Allow extra fields (like VITE_API_URL) but ignore them
        extra = "ignore"


# Global settings instance
settings = Settings()