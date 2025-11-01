"""
RAG Engine with Qdrant vector database
"""
import json
import logging
from typing import List, Dict, Optional
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

from core.config import settings
from core.schemas import KnowledgeBaseItem, SearchResponse
from services.embeddings import EmbeddingService

logger = logging.getLogger(__name__)


class RAGEngine:
    """Retrieval-Augmented Generation engine"""
    
    def __init__(self, embedding_service: EmbeddingService):
        self.embedding_service = embedding_service
        self.client = None
        self.collection_name = settings.QDRANT_COLLECTION
        self.knowledge_base = []
    
    async def initialize(self):
        """Initialize Qdrant and load knowledge base"""
        try:
            # Initialize Qdrant client
            if settings.QDRANT_MEMORY:
                self.client = QdrantClient(":memory:")
                logger.info("✅ Qdrant initialized (in-memory mode)")
            else:
                self.client = QdrantClient(path=settings.QDRANT_PATH)
                logger.info(f"✅ Qdrant initialized (persistent: {settings.QDRANT_PATH})")
            
            # Load knowledge base
            await self._load_knowledge_base()
            
            # Create collection and upload data
            await self._setup_collection()
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {e}")
            raise
    
    async def _load_knowledge_base(self):
        """Load knowledge base from JSON file"""
        kb_path = Path("data/math_knowledge_base.json")
        
        if not kb_path.exists():
            logger.warning(f"Knowledge base not found at {kb_path}")
            # Create default knowledge base
            self.knowledge_base = self._create_default_kb()
            # Save it
            kb_path.parent.mkdir(parents=True, exist_ok=True)
            with open(kb_path, 'w') as f:
                json.dump(self.knowledge_base, f, indent=2)
            logger.info("✅ Created default knowledge base")
        else:
            with open(kb_path, 'r') as f:
                self.knowledge_base = json.load(f)
            logger.info(f"✅ Loaded {len(self.knowledge_base)} problems from knowledge base")
    
    def _create_default_kb(self) -> List[Dict]:
        """Create a minimal default knowledge base"""
        return [
            {
                "id": "alg_001",
                "question": "Solve for x: 2x + 5 = 13",
                "solution": "Step 1: Subtract 5 from both sides\n2x = 8\n\nStep 2: Divide by 2\nx = 4",
                "answer": "x = 4",
                "topic": "Linear Equations",
                "difficulty": "easy"
            },
            {
                "id": "calc_001",
                "question": "Find the derivative of f(x) = x²",
                "solution": "Using the power rule:\nf'(x) = 2x^(2-1) = 2x",
                "answer": "f'(x) = 2x",
                "topic": "Derivatives",
                "difficulty": "easy"
            },
            {
                "id": "geom_001",
                "question": "Find the area of a circle with radius 5",
                "solution": "Using A = πr²:\nA = π × 5² = 25π ≈ 78.54",
                "answer": "25π or approximately 78.54",
                "topic": "Circle Area",
                "difficulty": "easy"
            }
        ]
    
    async def _setup_collection(self):
        """Create Qdrant collection and upload data"""
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            if exists:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return
            
            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIM,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"✅ Created collection: {self.collection_name}")
            
            # Create embeddings for all questions
            questions = [item['question'] for item in self.knowledge_base]
            embeddings = self.embedding_service.encode(questions, show_progress=False)
            
            # Upload to Qdrant
            points = []
            for idx, (item, embedding) in enumerate(zip(self.knowledge_base, embeddings)):
                point = PointStruct(
                    id=idx,
                    vector=embedding.tolist(),
                    payload={
                        "question": item['question'],
                        "solution": item['solution'],
                        "answer": item['answer'],
                        "topic": item['topic'],
                        "difficulty": item['difficulty'],
                        "doc_id": item['id']
                    }
                )
                points.append(point)
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"✅ Uploaded {len(points)} problems to Qdrant")
            
        except Exception as e:
            logger.error(f"Failed to setup collection: {e}")
            raise
    
    def search(
        self,
        query: str,
        top_k: int = None,
        score_threshold: float = None
    ) -> SearchResponse:
        """
        Search knowledge base for similar questions
        
        Args:
            query: User's question
            top_k: Number of results to return
            score_threshold: Minimum similarity score
            
        Returns:
            SearchResponse with matching items
        """
        if top_k is None:
            top_k = settings.KB_TOP_K
        if score_threshold is None:
            score_threshold = settings.KB_CONFIDENCE_THRESHOLD
        
        try:
            # Create embedding for query
            query_embedding = self.embedding_service.encode(query)
            
            # Use query_points instead of deprecated search
            search_results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding.tolist(),
                limit=top_k,
                with_payload=True
            ).points
            
            # Filter by score threshold and convert to schema
            results = []
            for result in search_results:
                if result.score >= score_threshold:
                    results.append(
                        KnowledgeBaseItem(
                            id=result.payload['doc_id'],
                            question=result.payload['question'],
                            solution=result.payload['solution'],
                            answer=result.payload['answer'],
                            topic=result.payload['topic'],
                            difficulty=result.payload['difficulty'],
                            score=result.score
                        )
                    )
            
            return SearchResponse(
                success=True,
                query=query,
                results=results,
                num_results=len(results)
            )
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return SearchResponse(
                success=False,
                query=query,
                results=[],
                num_results=0
            )
    
    def should_use_knowledge_base(
        self,
        query: str,
        confidence_threshold: float = None
    ) -> Dict:
        """
        Determine if knowledge base should be used or fall back to web search
        
        Args:
            query: User's question
            confidence_threshold: Minimum confidence to use KB
            
        Returns:
            Decision dict with use_kb, confidence, reason, best_match
        """
        if confidence_threshold is None:
            confidence_threshold = settings.KB_CONFIDENCE_THRESHOLD
        
        # Search knowledge base
        search_result = self.search(query, top_k=1, score_threshold=0.0)
        
        if not search_result.results:
            return {
                'use_kb': False,
                'confidence': 0.0,
                'reason': 'No matches found in knowledge base',
                'best_match': None,
                'source': 'web_search'
            }
        
        best_result = search_result.results[0]
        score = best_result.score
        
        if score >= confidence_threshold:
            return {
                'use_kb': True,
                'confidence': score,
                'reason': f'High confidence match (score: {score:.3f})',
                'best_match': best_result.dict(),
                'source': 'knowledge_base'
            }
        else:
            return {
                'use_kb': False,
                'confidence': score,
                'reason': f'Low confidence (score: {score:.3f}), using web search',
                'best_match': best_result.dict(),
                'source': 'web_search'
            }