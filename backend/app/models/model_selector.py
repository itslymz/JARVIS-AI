"""Model selector for automatic best model selection."""

from typing import List, Optional
from app.config import settings
from app.models.base import BaseModel
from app.models.openai_model import OpenAIModel
from app.models.anthropic_model import AnthropicModel
from app.models.ollama_model import OllamaModel


class ModelSelector:
    """Automatically selects the best available model for a task."""

    def __init__(self):
        """Initialize model selector."""
        self.models: List[BaseModel] = []
        self._initialize_models()

    def _initialize_models(self) -> None:
        """Initialize available models."""
        # Add OpenAI if API key available
        if settings.OPENAI_API_KEY:
            self.models.append(OpenAIModel(settings.OPENAI_MODEL))

        # Add Anthropic if API key available
        if settings.ANTHROPIC_API_KEY:
            self.models.append(AnthropicModel(settings.ANTHROPIC_MODEL))

        # Always add Ollama (local fallback)
        self.models.append(OllamaModel(settings.OLLAMA_MODEL))

    async def get_best_model(self) -> Optional[BaseModel]:
        """Get the best available model.
        
        Returns:
            Best available model or None
        """
        # Try to get default provider first
        for model in self.models:
            if model.get_provider().lower() == settings.DEFAULT_MODEL_PROVIDER.lower():
                if await model.is_available():
                    return model

        # Fall back to first available
        for model in self.models:
            if await model.is_available():
                return model

        return None

    async def get_model_by_provider(self, provider: str) -> Optional[BaseModel]:
        """Get model by provider name.
        
        Args:
            provider: Provider name
            
        Returns:
            Model or None
        """
        for model in self.models:
            if model.get_provider().lower() == provider.lower():
                if await model.is_available():
                    return model
        return None

    def get_available_models(self) -> List[str]:
        """Get list of available model providers.
        
        Returns:
            List of provider names
        """
        return [model.get_provider() for model in self.models]

    def get_model_info(self) -> dict:
        """Get information about available models.
        
        Returns:
            Dictionary with model info
        """
        return {
            "default_provider": settings.DEFAULT_MODEL_PROVIDER,
            "default_model": settings.DEFAULT_MODEL,
            "available_models": [
                {
                    "provider": model.get_provider(),
                    "name": model.get_name(),
                }
                for model in self.models
            ],
        }
