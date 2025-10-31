"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


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

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173", "http://localhost:3000"]

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
        env_file = "../.env"
        case_sensitive = True


# Global settings instance
settings = Settings()
