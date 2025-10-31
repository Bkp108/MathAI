"""
API Routes for MathAI
"""
from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Optional
import logging
from datetime import datetime
import uuid

from core.schemas import (
    ChatRequest, ChatResponse,
    FeedbackRequest, FeedbackResponse, FeedbackStats,
    SearchRequest, SearchResponse,
    AnalyticsRequest, AnalyticsResponse,
    HealthResponse
)
from core.database import db
from services.routing import RoutingService
from services.guardrails import guardrails
from services.web_search import web_search
from services.gemini_agent import gemini_agent

logger = logging.getLogger(__name__)

router = APIRouter()


def get_routing_service(request: Request) -> RoutingService:
    """Dependency to get routing service from request state"""
    return RoutingService(
        rag_engine=request.state.rag_engine,
        web_search=web_search,
        gemini_agent=gemini_agent,
        guardrails=guardrails
    )


# ========== Health & Status ==========

@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    """Health check endpoint"""
    services_status = {
        "rag_engine": request.state.rag_engine is not None,
        "embedding_service": request.state.embedding_service is not None,
        "gemini": gemini_agent.model is not None,
        "web_search": web_search.client is not None,
        "database": True  # Database is always available (SQLite)
    }
    
    return HealthResponse(
        status="healthy" if all(services_status.values()) else "degraded",
        version="1.0.0",
        timestamp=datetime.now(),
        services=services_status
    )


# ========== Chat Endpoints ==========

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    routing_service: RoutingService = Depends(get_routing_service)
):
    """
    Main chat endpoint - process user query and return solution
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Log user message
        db.save_message(
            session_id=session_id,
            role="user",
            content=request.message,
            metadata={"use_feedback_learning": request.use_feedback_learning}
        )
        
        # Log analytics event
        db.log_event(
            event_type="query",
            event_data={"query_length": len(request.message)},
            session_id=session_id
        )
        
        # Process query
        response = await routing_service.process_query(request)
        
        # Log assistant message
        if response.success:
            db.save_message(
                session_id=session_id,
                role="assistant",
                content=response.solution,
                metadata={
                    "source": response.routing.source.value if response.routing else "unknown",
                    "confidence": response.routing.confidence if response.routing else 0.0
                }
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/history")
async def get_chat_history(
    session_id: str,
    limit: int = 50
):
    """Get chat history for a session"""
    try:
        history = db.get_chat_history(session_id, limit)
        return {
            "success": True,
            "session_id": session_id,
            "messages": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"Failed to get chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== Feedback Endpoints ==========

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackRequest):
    """Submit feedback for a solution"""
    try:
        feedback_id = db.save_feedback(
            query=feedback.query,
            solution=feedback.solution,
            rating=feedback.rating,
            comment=feedback.comment,
            improved_solution=feedback.improved_solution,
            model_used="gemini-pro",
            source="unknown",  # Could be enhanced to track source
            confidence=None
        )
        
        # Log analytics event
        db.log_event(
            event_type="feedback_submitted",
            event_data={
                "rating": feedback.rating,
                "has_comment": feedback.comment is not None,
                "has_improvement": feedback.improved_solution is not None
            }
        )
        
        return FeedbackResponse(
            success=True,
            message="Feedback submitted successfully",
            feedback_id=feedback_id
        )
        
    except Exception as e:
        logger.error(f"Failed to submit feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feedback/stats", response_model=FeedbackStats)
async def get_feedback_stats():
    """Get feedback statistics"""
    try:
        stats = db.get_feedback_stats()
        return FeedbackStats(**stats)
    except Exception as e:
        logger.error(f"Failed to get feedback stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feedback/positive")
async def get_positive_feedback(min_rating: int = 4):
    """Get positive feedback for learning"""
    try:
        feedback = db.get_positive_feedback(min_rating)
        return {
            "success": True,
            "count": len(feedback),
            "feedback": feedback
        }
    except Exception as e:
        logger.error(f"Failed to get positive feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== Knowledge Base Endpoints ==========

@router.post("/kb/search", response_model=SearchResponse)
async def search_knowledge_base(
    search: SearchRequest,
    request: Request
):
    """Search knowledge base directly"""
    try:
        rag_engine = request.state.rag_engine
        if not rag_engine:
            raise HTTPException(status_code=503, detail="RAG engine not available")
        
        result = rag_engine.search(
            query=search.query,
            top_k=search.top_k,
            score_threshold=search.score_threshold
        )
        
        return result
        
    except Exception as e:
        logger.error(f"KB search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kb/stats")
async def get_kb_stats(request: Request):
    """Get knowledge base statistics"""
    try:
        rag_engine = request.state.rag_engine
        if not rag_engine:
            raise HTTPException(status_code=503, detail="RAG engine not available")
        
        return {
            "success": True,
            "total_problems": len(rag_engine.knowledge_base),
            "collection_name": rag_engine.collection_name,
            "topics": list(set(item['topic'] for item in rag_engine.knowledge_base)),
            "difficulties": list(set(item['difficulty'] for item in rag_engine.knowledge_base))
        }
        
    except Exception as e:
        logger.error(f"Failed to get KB stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== Web Search Endpoint ==========

@router.post("/web/search")
async def perform_web_search(search: SearchRequest):
    """Perform web search directly"""
    try:
        result = web_search.search_with_retry(search.query)
        return result
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== Analytics Endpoints ==========

@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(days: int = 7):
    """Get analytics for last N days"""
    try:
        analytics = db.get_analytics(days)
        feedback_stats = db.get_feedback_stats()
        
        return AnalyticsResponse(
            period_days=days,
            total_queries=analytics['total_queries'],
            total_feedback=feedback_stats['total_feedback'],
            average_rating=feedback_stats['average_rating'],
            rating_distribution=feedback_stats['rating_distribution'],
            events=analytics['events'],
            top_topics=[]  # Could be enhanced
        )
        
    except Exception as e:
        logger.error(f"Failed to get analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== Utility Endpoints ==========

@router.post("/improve")
async def improve_solution(
    query: str,
    solution: str,
    feedback: str,
    improved_suggestion: Optional[str] = None
):
    """Generate improved solution based on feedback"""
    try:
        result = gemini_agent.improve_solution(
            original_query=query,
            original_solution=solution,
            feedback=feedback,
            improved_suggestion=improved_suggestion
        )
        
        if result['success']:
            return {
                "success": True,
                "improved_solution": result['solution']
            }
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Failed to improve solution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "name": "MathAI API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat",
            "feedback": "/api/feedback",
            "search": "/api/kb/search",
            "analytics": "/api/analytics",
            "docs": "/docs"
        }
    }