"""
Input/Output guardrails for safety and quality control
"""
import re
from typing import Dict
import logging

from core.config import settings
from core.schemas import GuardrailCheckResult

logger = logging.getLogger(__name__)


class GuardrailsSystem:
    """Implements input and output validation"""
    
    def __init__(self):
        self.enabled = settings.ENABLE_GUARDRAILS
        
        # Math-related keywords
        self.math_keywords = [
            'solve', 'calculate', 'compute', 'find', 'derive', 'integrate',
            'differentiate', 'equation', 'formula', 'theorem', 'proof',
            'algebra', 'calculus', 'geometry', 'trigonometry', 'statistics',
            'probability', 'number', 'function', 'graph', 'matrix', 'vector',
            'derivative', 'integral', 'limit', 'series', 'polynomial',
            'factor', 'simplify', 'expand', 'evaluate', 'plot', 'area',
            'volume', 'perimeter', 'radius', 'diameter', 'angle', 'triangle',
            'circle', 'square', 'sum', 'product', 'quotient', 'root'
        ]
        
        # Inappropriate content keywords
        self.inappropriate_keywords = [
            'hack', 'crack', 'cheat', 'steal', 'illegal', 'weapon', 'drug',
            'violence', 'violent', 'harm', 'kill', 'murder', 'abuse',
            'exploit', 'malware', 'virus', 'bomb', 'terrorist'
        ]
    
    def check_input_guardrail(self, query: str) -> GuardrailCheckResult:
        """
        Check if input query is safe and appropriate
        
        Args:
            query: User's input query
            
        Returns:
            GuardrailCheckResult with allowed status and reason
        """
        if not self.enabled:
            return GuardrailCheckResult(
                allowed=True,
                reason="Guardrails disabled",
                category="bypass"
            )
        
        query_lower = query.lower().strip()
        
        # Check length
        if len(query) > settings.MAX_QUERY_LENGTH:
            return GuardrailCheckResult(
                allowed=False,
                reason=f"Query too long (max {settings.MAX_QUERY_LENGTH} characters)",
                category="length"
            )
        
        # Check for empty query
        if not query_lower:
            return GuardrailCheckResult(
                allowed=False,
                reason="Query cannot be empty",
                category="empty"
            )
        
        # Check for inappropriate content
        for keyword in self.inappropriate_keywords:
            if keyword in query_lower:
                logger.warning(f"Blocked inappropriate query: {query[:50]}...")
                return GuardrailCheckResult(
                    allowed=False,
                    reason="Content policy violation. This system only handles mathematics questions.",
                    category="inappropriate"
                )
        
        # Check if query is math-related
        is_math = self._is_math_related(query_lower)
        
        if not is_math:
            return GuardrailCheckResult(
                allowed=False,
                reason="Please ask a mathematics question. This system specializes in math problems.",
                category="non_math"
            )
        
        return GuardrailCheckResult(
            allowed=True,
            reason="Query is valid",
            category="mathematics"
        )
    
    def check_output_guardrail(self, response: str) -> GuardrailCheckResult:
        """
        Check if output response is safe and appropriate
        
        Args:
            response: AI-generated response
            
        Returns:
            GuardrailCheckResult with allowed status
        """
        if not self.enabled:
            return GuardrailCheckResult(
                allowed=True,
                reason="Guardrails disabled"
            )
        
        response_lower = response.lower()
        
        # Check for inappropriate content in response
        for keyword in self.inappropriate_keywords:
            if keyword in response_lower:
                logger.warning(f"Blocked inappropriate response")
                return GuardrailCheckResult(
                    allowed=False,
                    reason="Response contains inappropriate content"
                )
        
        # Check response quality
        has_steps = 'step' in response_lower or '1.' in response or '2.' in response
        has_explanation = len(response) > 50
        has_math_content = any(kw in response_lower for kw in ['equation', 'formula', 'solution', 'answer'])
        
        if has_steps or (has_explanation and has_math_content):
            return GuardrailCheckResult(
                allowed=True,
                reason="Response is educational and appropriate"
            )
        
        # If response is too short or lacks structure
        if len(response) < 30:
            return GuardrailCheckResult(
                allowed=True,  # Still allow, but note it could be better
                reason="Response could be more detailed"
            )
        
        return GuardrailCheckResult(
            allowed=True,
            reason="Response is valid"
        )
    
    def _is_math_related(self, query: str) -> bool:
        """
        Check if query is related to mathematics
        
        Args:
            query: Lowercase query string
            
        Returns:
            True if query appears to be math-related
        """
        # Check for math keywords
        has_math_keyword = any(keyword in query for keyword in self.math_keywords)
        
        # Check for numbers
        has_numbers = bool(re.search(r'\d', query))
        
        # Check for mathematical symbols
        math_symbols = r'[+\-*/=^√∫∑∏<>≤≥≠±∞πθφ°]'
        has_math_symbols = bool(re.search(math_symbols, query))
        
        # Check for mathematical expressions
        # e.g., "x^2", "2x", "sin(x)", etc.
        math_patterns = [
            r'[a-z]\^?\d',  # x2, x^2
            r'\d[a-z]',      # 2x
            r'sin|cos|tan|log|ln|exp',  # trig/log functions
            r'\([^)]*[a-z][^)]*\)',  # expressions in parentheses
            r'[a-z]\s*=\s*\d',  # x = 5
        ]
        has_math_pattern = any(re.search(pattern, query) for pattern in math_patterns)
        
        # Question indicators for math
        math_question_words = ['what', 'how', 'find', 'solve', 'calculate', 'prove', 'show']
        has_question = any(word in query for word in math_question_words)
        
        # Scoring system
        score = 0
        if has_math_keyword: score += 2
        if has_numbers: score += 1
        if has_math_symbols: score += 2
        if has_math_pattern: score += 2
        if has_question and (has_numbers or has_math_keyword): score += 1
        
        # Need at least score of 2 to consider it math-related
        return score >= 2
    
    def sanitize_input(self, query: str) -> str:
        """
        Sanitize and clean input query
        
        Args:
            query: Raw input query
            
        Returns:
            Cleaned query
        """
        # Remove excessive whitespace
        query = ' '.join(query.split())
        
        # Remove potentially dangerous characters (SQL injection, etc.)
        # But keep mathematical symbols
        query = re.sub(r'[<>\"\'`]', '', query)
        
        # Limit length
        if len(query) > settings.MAX_QUERY_LENGTH:
            query = query[:settings.MAX_QUERY_LENGTH]
        
        return query.strip()


# Global instance
guardrails = GuardrailsSystem()