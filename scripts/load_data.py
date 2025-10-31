"""
Load knowledge base and initialize RAG system
"""
import sys
import asyncio
from pathlib import Path
import json

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.embeddings import EmbeddingService
from backend.services.rag_engine import RAGEngine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Load knowledge base and initialize RAG"""
    logger.info("🔄 Loading knowledge base...")
    
    try:
        # Ensure data directory exists
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Check if knowledge base exists
        kb_path = data_dir / "math_knowledge_base.json"
        if not kb_path.exists():
            logger.info("📝 Knowledge base not found, using default")
        
        # Initialize embedding service
        logger.info("🔄 Initializing embedding service...")
        embedding_service = EmbeddingService()
        await embedding_service.initialize()
        logger.info("✅ Embedding service ready")
        
        # Initialize RAG engine
        logger.info("🔄 Initializing RAG engine...")
        rag_engine = RAGEngine(embedding_service)
        await rag_engine.initialize()
        logger.info("✅ RAG engine ready")
        
        # Test search
        logger.info("\n🧪 Testing RAG system...")
        test_query = "Solve for x: 2x + 5 = 13"
        result = rag_engine.search(test_query, top_k=3)
        
        logger.info(f"✅ Search test passed")
        logger.info(f"   Query: {test_query}")
        logger.info(f"   Found: {result.num_results} results")
        
        if result.results:
            best = result.results[0]
            logger.info(f"   Best match: {best.question[:50]}...")
            logger.info(f"   Score: {best.score:.3f}")
        
        logger.info("\n✅ Knowledge base loaded successfully!")
        logger.info(f"   Total problems: {len(rag_engine.knowledge_base)}")
        logger.info(f"   Collection: {rag_engine.collection_name}")
        
    except Exception as e:
        logger.error(f"❌ Loading failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())