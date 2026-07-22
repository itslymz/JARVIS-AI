"""Anthropic Claude model integration."""

from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from app.config import settings
from app.models.base import BaseModel


class AnthropicModel(BaseModel):
    """Anthropic Claude integration."""

    def __init__(self, model: str = "claude-3-opus-20240229"):
        """Initialize Anthropic model.
        
        Args:
            model: Model name
        """
        self.model = model
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def generate(
        self,
        prompt: str,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate response using Claude.
        
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

            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=messages,
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic generation error: {e}")
            return ""

    async def is_available(self) -> bool:
        """Check if Anthropic API is available.
        
        Returns:
            True if available
        """
        return bool(settings.ANTHROPIC_API_KEY)

    def get_name(self) -> str:
        """Get model name."""
        return self.model

    def get_provider(self) -> str:
        """Get provider name."""
        return "Anthropic"
