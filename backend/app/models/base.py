"""Base model interface."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseModel(ABC):
    """Base interface for all AI models."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate response from model.
        
        Args:
            prompt: Input prompt
            messages: Conversation history
            temperature: Model temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response
        """
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if model is available.
        
        Returns:
            True if model can be used
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Get model name.
        
        Returns:
            Model name
        """
        pass

    @abstractmethod
    def get_provider(self) -> str:
        """Get provider name.
        
        Returns:
            Provider name
        """
        pass
