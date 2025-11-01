"""
Gemini AI agent for generating solutions
"""
import google.generativeai as genai
from typing import Dict, Optional
import logging

from core.config import settings

logger = logging.getLogger(__name__)


class GeminiAgent:
    """Google Gemini API integration"""

    def __init__(self):
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize Gemini model"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # Use the correct free model name
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            logger.info("✅ Gemini model initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            self.model = None

    def generate_solution(
        self,
        query: str,
        context: Optional[str] = None,
        temperature: float = 0.3
    ) -> Dict:
        """
        Generate solution using Gemini

        Args:
            query: User's math question
            context: Additional context (from KB or web search)
            temperature: Model temperature (0-1)

        Returns:
            Dict with solution and metadata
        """
        if not self.model:
            return {
                'success': False,
                'solution': None,
                'error': 'Gemini model not initialized'
            }

        try:
            # Build prompt
            prompt = self._build_prompt(query, context)

            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature
                )
            )

            solution = response.text

            return {
                'success': True,
                'solution': solution,
                'error': None,
                'model': 'gemini-1.5-flash-latest',
                'temperature': temperature
            }

        except Exception as e:
            logger.error(f"Solution generation failed: {e}")
            return {
                'success': False,
                'solution': None,
                'error': str(e)
            }

    def _build_prompt(self, query: str, context: Optional[str] = None) -> str:
        """
        Build prompt for Gemini

        Args:
            query: User's question
            context: Additional context

        Returns:
            Formatted prompt
        """
        if context:
            prompt = f"""You are an expert mathematics tutor. Use the following context to help answer the question.

Context:
{context}

Question: {query}

Provide a clear, step-by-step solution that:
1. Breaks down the problem into manageable steps
2. Explains the reasoning for each step
3. Shows all calculations clearly
4. Provides the final answer

Format your response with clear step numbering and explanations."""
        else:
            prompt = f"""You are an expert mathematics tutor. A student asked: "{query}"

Please provide a clear, step-by-step solution that:
1. Breaks down the problem into manageable steps
2. Explains the reasoning for each step
3. Shows all calculations clearly
4. Provides the final answer

Format your response with clear step numbering and explanations."""

        return prompt

    def generate_with_kb(
        self,
        query: str,
        kb_item: Dict
    ) -> Dict:
        """
        Generate solution using knowledge base item as reference

        Args:
            query: User's question
            kb_item: Knowledge base item (similar question/solution)

        Returns:
            Dict with solution
        """
        context = f"""Similar Problem:
Question: {kb_item['question']}
Solution: {kb_item['solution']}
Answer: {kb_item['answer']}

Use this as a reference to solve the user's question, but adapt it appropriately."""

        return self.generate_solution(query, context)

    def generate_with_web(
        self,
        query: str,
        web_context: str
    ) -> Dict:
        """
        Generate solution using web search context

        Args:
            query: User's question
            web_context: Context from web search

        Returns:
            Dict with solution
        """
        context = f"""Web Search Results:
{web_context}

Use this information to help answer the question, citing sources when appropriate."""

        return self.generate_solution(query, context)

    def improve_solution(
        self,
        original_query: str,
        original_solution: str,
        feedback: str,
        improved_suggestion: Optional[str] = None
    ) -> Dict:
        """
        Generate improved solution based on feedback

        Args:
            original_query: Original question
            original_solution: Original solution
            feedback: User feedback
            improved_suggestion: User's suggested improvement

        Returns:
            Dict with improved solution
        """
        prompt = f"""You previously provided this solution:

Question: {original_query}
Your Solution:
{original_solution}

User Feedback: {feedback}
"""

        if improved_suggestion:
            prompt += f"\nUser's Suggested Improvement:\n{improved_suggestion}\n"

        prompt += """
Based on this feedback, provide an IMPROVED solution that addresses the concerns and incorporates the suggestions.
Make sure your improved solution is:
1. More clear and easy to understand
2. More detailed where needed
3. Addresses any mistakes pointed out
4. Better structured
"""

        try:
            response = self.model.generate_content(prompt)
            return {
                'success': True,
                'solution': response.text,
                'error': None,
                'improved': True
            }
        except Exception as e:
            logger.error(f"Failed to generate improved solution: {e}")
            return {
                'success': False,
                'solution': None,
                'error': str(e)
            }


# Global instance
gemini_agent = GeminiAgent()
