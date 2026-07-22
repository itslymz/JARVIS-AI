"""OpenAI model integration."""

from typing import List, Dict, Any, Optional
import openai
from app.config import settings
from app.models.base import BaseModel


class OpenAIModel(BaseModel):
    """OpenAI GPT integration."""

    def __init__(self, model: str = "gpt-4"):
        """Initialize OpenAI model.
        
        Args:
            model: Model name (gpt-4, gpt-3.5-turbo)
        """
        self.model = model
        openai.api_key = settings.OPENAI_API_KEY

    async def generate(
        self,
        prompt: str,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate response using OpenAI.
        
        Args:
            prompt: Input prompt
            messages: Conversation history
            temperature: Model temperature
            max_tokens: Maximum tokens
            
        Returns:
            Generated response
        """
        try:
            if messages is None:
                messages = [{"role": "user", "content": prompt}]
            else:
                messages.append({"role": "user", "content": prompt})

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI generation error: {e}")
            return ""

    async def is_available(self) -> bool:
        """Check if OpenAI API is available.
        
        Returns:
            True if available
        """
        return bool(settings.OPENAI_API_KEY)

    def get_name(self) -> str:
        """Get model name."""
        return self.model

    def get_provider(self) -> str:
        """Get provider name."""
        return "OpenAI"
