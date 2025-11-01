"""
Intelligent routing between knowledge base and web search
"""
from typing import Dict
import logging

from core.schemas import ChatRequest, ChatResponse, RoutingDecision, SourceType
from services.rag_engine import RAGEngine
from services.web_search import WebSearchService
from services.gemini_agent import GeminiAgent
from services.guardrails import GuardrailsSystem

logger = logging.getLogger(__name__)


class RoutingService:
    """Routes queries to appropriate source and generates responses"""
    
    def __init__(
        self,
        rag_engine: RAGEngine,
        web_search: WebSearchService,
        gemini_agent: GeminiAgent,
        guardrails: GuardrailsSystem
    ):
        self.rag_engine = rag_engine
        self.web_search = web_search
        self.gemini_agent = gemini_agent
        self.guardrails = guardrails
    
    async def process_query(self, request: ChatRequest) -> ChatResponse:
        """
        Process user query with intelligent routing
        
        Args:
            request: ChatRequest with user's message
            
        Returns:
            ChatResponse with solution
        """
        query = request.message
        
        # Step 1: Input Guardrails
        guardrail_check = self.guardrails.check_input_guardrail(query)
        
        # Convert Pydantic model to dict if needed
        if hasattr(guardrail_check, 'dict'):
            guardrail_dict = guardrail_check.dict()
        elif hasattr(guardrail_check, 'model_dump'):
            guardrail_dict = guardrail_check.model_dump()
        else:
            guardrail_dict = guardrail_check
        
        if not guardrail_dict['allowed']:
            logger.warning(f"Query blocked: {guardrail_dict['reason']}")
            return ChatResponse(
                success=False,
                query=query,
                solution=None,
                blocked=True,
                error=guardrail_dict['reason']
            )
        
        # Step 2: Sanitize input
        query = self.guardrails.sanitize_input(query)
        
        # Step 3: Routing Decision
        routing_decision = self.rag_engine.should_use_knowledge_base(query)
        
        logger.info(f"Routing: {routing_decision['source']} (confidence: {routing_decision['confidence']:.3f})")
        
        # Step 4: Generate solution based on routing
        if routing_decision['use_kb']:
            # Use knowledge base
            result = await self._generate_from_kb(query, routing_decision['best_match'])
        else:
            # Use web search
            result = await self._generate_from_web(query)
        
        # Step 5: Output Guardrails
        if result['success'] and result.get('solution'):
            output_check = self.guardrails.check_output_guardrail(result['solution'])
            
            # Convert to dict if needed
            if hasattr(output_check, 'dict'):
                output_dict = output_check.dict()
            elif hasattr(output_check, 'model_dump'):
                output_dict = output_check.model_dump()
            else:
                output_dict = output_check
                
            if not output_dict['allowed']:
                logger.warning("Response blocked by output guardrails")
                return ChatResponse(
                    success=False,
                    query=query,
                    solution=None,
                    blocked=True,
                    error="Output validation failed"
                )
        
        # Step 6: Build response
        routing_info = RoutingDecision(
            use_kb=routing_decision['use_kb'],
            confidence=routing_decision['confidence'],
            reason=routing_decision['reason'],
            source=SourceType(routing_decision['source'])
        )
        
        if result['success']:
            return ChatResponse(
                success=True,
                query=query,
                solution=result['solution'],
                routing=routing_info,
                metadata={
                    'model': result.get('model', 'unknown'),
                    'source': routing_decision['source'],
                    'confidence': routing_decision['confidence']
                },
                blocked=False
            )
        else:
            return ChatResponse(
                success=False,
                query=query,
                solution=None,
                routing=routing_info,
                error=result.get('error', 'Unknown error'),
                blocked=False
            )
    
    async def _generate_from_kb(self, query: str, kb_item: Dict) -> Dict:
        """Generate solution using knowledge base"""
        logger.info(f"Generating from KB: {kb_item['question'][:50]}...")
        
        try:
            result = self.gemini_agent.generate_with_kb(query, kb_item)
            return result
        except Exception as e:
            logger.error(f"KB generation failed: {e}")
            return {
                'success': False,
                'solution': None,
                'error': str(e)
            }
    
    async def _generate_from_web(self, query: str) -> Dict:
        """Generate solution using web search"""
        logger.info(f"Generating from web search...")
        
        try:
            # Perform web search
            search_result = self.web_search.search_with_retry(query)
            
            if not search_result.success:
                # Fallback to direct LLM
                logger.warning("Web search failed, using direct LLM")
                return self.gemini_agent.generate_solution(query)
            
            # Extract context
            context = self.web_search.extract_context(search_result)
            
            # Generate solution with context
            result = self.gemini_agent.generate_with_web(query, context)
            
            return result
            
        except Exception as e:
            logger.error(f"Web generation failed: {e}")
            # Fallback to direct LLM
            return self.gemini_agent.generate_solution(query)