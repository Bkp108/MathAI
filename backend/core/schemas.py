"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ========== Enums ==========

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class SourceType(str, Enum):
    KNOWLEDGE_BASE = "knowledge_base"
    WEB_SEARCH = "web_search"
    DIRECT_LLM = "direct_llm"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


# ========== Chat Schemas ==========

class ChatRequest(BaseModel):
    """Chat request from user"""
    message: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = None
    use_feedback_learning: bool = True
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class Message(BaseModel):
    """Individual chat message"""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None


class RoutingDecision(BaseModel):
    """Routing decision details"""
    use_kb: bool
    confidence: float
    reason: str
    source: SourceType


class ChatResponse(BaseModel):
    """Chat response to user"""
    success: bool
    message: str
    query: str
    solution: Optional[str] = None
    routing: Optional[RoutingDecision] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    blocked: bool = False


# ========== Feedback Schemas ==========

class FeedbackRequest(BaseModel):
    """Feedback submission"""
    query: str
    solution: str
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None
    improved_solution: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError("Rating must be between 1 and 5")
        return v


class FeedbackResponse(BaseModel):
    """Feedback submission response"""
    success: bool
    message: str
    feedback_id: Optional[int] = None


class FeedbackStats(BaseModel):
    """Feedback statistics"""
    total_feedback: int
    average_rating: float
    rating_distribution: Dict[int, int]
    recent_feedback: List[Dict[str, Any]]


# ========== Knowledge Base Schemas ==========

class KnowledgeBaseItem(BaseModel):
    """Knowledge base entry"""
    id: str
    question: str
    solution: str
    answer: str
    topic: str
    difficulty: DifficultyLevel
    score: Optional[float] = None


class SearchRequest(BaseModel):
    """Search request"""
    query: str = Field(..., min_length=1)
    top_k: int = Field(3, ge=1, le=10)
    score_threshold: float = Field(0.5, ge=0.0, le=1.0)


class SearchResponse(BaseModel):
    """Search response"""
    success: bool
    query: str
    results: List[KnowledgeBaseItem]
    num_results: int


# ========== Web Search Schemas ==========

class WebSearchResult(BaseModel):
    """Individual web search result"""
    title: str
    url: str
    content: str
    score: Optional[float] = None


class WebSearchResponse(BaseModel):
    """Web search response"""
    success: bool
    query: str
    answer: Optional[str] = None
    results: List[WebSearchResult]
    num_results: int
    error: Optional[str] = None


# ========== Analytics Schemas ==========

class AnalyticsRequest(BaseModel):
    """Analytics request"""
    days: int = Field(7, ge=1, le=90)


class AnalyticsResponse(BaseModel):
    """Analytics response"""
    period_days: int
    total_queries: int
    total_feedback: int
    average_rating: float
    rating_distribution: Dict[int, int]
    events: Dict[str, int]
    top_topics: List[Dict[str, Any]]


# ========== System Schemas ==========

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
    services: Dict[str, bool]


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


# ========== Guardrails Schemas ==========

class GuardrailCheckResult(BaseModel):
    """Guardrail check result"""
    allowed: bool
    reason: str
    category: Optional[str] = None


# ========== Session Schemas ==========

class SessionInfo(BaseModel):
    """Session information"""
    session_id: str
    created_at: datetime
    message_count: int
    last_activity: datetime