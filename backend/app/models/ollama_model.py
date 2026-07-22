"""Ollama local model integration."""

from typing import List, Dict, Any, Optional
import httpx
from app.config import settings
from app.models.base import BaseModel


class OllamaModel(BaseModel):
    """Ollama local model integration.
    
    Connects to a local Ollama instance for running open-source models.
    """

    def __init__(self, model: str = "mistral"):
        """Initialize Ollama model.
        
        Args:
            model: Model name (mistral, neural-chat, etc.)
        """
        self.model = model
        self.base_url = settings.OLLAMA_BASE_URL
        self.client = httpx.AsyncClient()

    async def generate(
        self,
        prompt: str,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate response using Ollama.
        
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

            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "stream": False,
                },
                timeout=60.0,
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "")
            return ""
        except Exception as e:
            print(f"Ollama generation error: {e}")
            return ""

    async def is_available(self) -> bool:
        """Check if Ollama is available.
        
        Returns:
            True if available
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/api/tags",
                timeout=5.0,
            )
            return response.status_code == 200
        except Exception:
            return False

    def get_name(self) -> str:
        """Get model name."""
        return self.model

    def get_provider(self) -> str:
        """Get provider name."""
        return "Ollama"
