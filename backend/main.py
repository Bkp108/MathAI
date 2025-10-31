"""
MathAI Backend - FastAPI Application Entry Point
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from core.config import settings
from core.database import init_db
from api.routes import router
from services.rag_engine import RAGEngine
from services.embeddings import EmbeddingService

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Global instances (initialized on startup)
rag_engine = None
embedding_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global rag_engine, embedding_service

    # Startup
    logger.info("🚀 Starting MathAI Backend...")

    try:
        # Initialize database
        init_db()
        logger.info("✅ Database initialized")

        # Initialize embedding service
        embedding_service = EmbeddingService()
        await embedding_service.initialize()
        logger.info("✅ Embedding service initialized")

        # Initialize RAG engine
        rag_engine = RAGEngine(embedding_service)
        await rag_engine.initialize()
        logger.info("✅ RAG engine initialized")

        logger.info("✅ MathAI Backend ready!")

    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

    yield

    # Shutdown
    logger.info("👋 Shutting down MathAI Backend...")


# Create FastAPI app
app = FastAPI(
    title="MathAI API",
    description="Intelligent Math Problem Solver with RAG and Web Search",
    version="1.0.0",
    lifespan=lifespan
)


# CORS Configuration - FIXED
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # Use property method
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routes
app.include_router(router, prefix="/api")


# Root endpoint
@app.get("/")
async def root():
    """Health check and API info"""
    return {
        "name": "MathAI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health"
    }


# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all uncaught exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG_MODE else "An error occurred"
        }
    )


# Make global instances available to routes
@app.middleware("http")
async def add_global_instances(request: Request, call_next):
    """Add global instances to request state"""
    request.state.rag_engine = rag_engine
    request.state.embedding_service = embedding_service
    response = await call_next(request)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG_MODE,
        log_level=settings.LOG_LEVEL.lower()
    )