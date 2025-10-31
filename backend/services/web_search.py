"""
Web search using Tavily API (MCP pattern)
"""
from tavily import TavilyClient
from typing import Dict, List
import logging

from core.config import settings
from core.schemas import WebSearchResponse, WebSearchResult

logger = logging.getLogger(__name__)


class WebSearchService:
    """Web search using Tavily API"""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Tavily client"""
        try:
            self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)
            logger.info("✅ Tavily client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Tavily: {e}")
            self.client = None
    
    def search(
        self,
        query: str,
        max_results: int = None
    ) -> WebSearchResponse:
        """
        Perform web search using Tavily
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            WebSearchResponse with results
        """
        if max_results is None:
            max_results = settings.WEB_SEARCH_MAX_RESULTS
        
        if not self.client:
            return WebSearchResponse(
                success=False,
                query=query,
                answer=None,
                results=[],
                num_results=0,
                error="Tavily client not initialized"
            )
        
        try:
            # Perform search
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_answer=True
            )
            
            # Convert to schema
            results = []
            for result in response.get('results', []):
                results.append(
                    WebSearchResult(
                        title=result.get('title', 'No title'),
                        url=result.get('url', ''),
                        content=result.get('content', '')[:500],  # Limit content
                        score=result.get('score')
                    )
                )
            
            return WebSearchResponse(
                success=True,
                query=query,
                answer=response.get('answer', ''),
                results=results,
                num_results=len(results),
                error=None
            )
            
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return WebSearchResponse(
                success=False,
                query=query,
                answer=None,
                results=[],
                num_results=0,
                error=str(e)
            )
    
    def search_with_retry(
        self,
        query: str,
        max_retries: int = 2
    ) -> WebSearchResponse:
        """
        Web search with retry logic
        
        Args:
            query: Search query
            max_retries: Maximum retry attempts
            
        Returns:
            WebSearchResponse
        """
        for attempt in range(max_retries):
            try:
                result = self.search(query)
                if result.success:
                    return result
                
                if attempt < max_retries - 1:
                    logger.info(f"Retry attempt {attempt + 1} for query: {query[:50]}")
                    
            except Exception as e:
                if attempt == max_retries - 1:
                    return WebSearchResponse(
                        success=False,
                        query=query,
                        answer=None,
                        results=[],
                        num_results=0,
                        error=f"All retry attempts failed: {str(e)}"
                    )
        
        return WebSearchResponse(
            success=False,
            query=query,
            answer=None,
            results=[],
            num_results=0,
            error="Search failed after all retries"
        )
    
    def extract_context(self, search_response: WebSearchResponse) -> str:
        """
        Extract formatted context from search results
        
        Args:
            search_response: WebSearchResponse object
            
        Returns:
            Formatted context string
        """
        if not search_response.success:
            return f"Search failed: {search_response.error}"
        
        if search_response.num_results == 0:
            return "No relevant information found on the web."
        
        context_parts = []
        
        # Add AI-generated answer if available
        if search_response.answer:
            context_parts.append(f"Summary: {search_response.answer}\n")
        
        # Add individual results
        for i, result in enumerate(search_response.results, 1):
            context_parts.append(f"\nSource {i}: {result.title}")
            context_parts.append(f"Content: {result.content}")
            context_parts.append(f"URL: {result.url}\n")
        
        return "\n".join(context_parts)


# Global instance
web_search = WebSearchService()