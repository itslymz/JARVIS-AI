"""Application configuration."""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    API_TITLE: str = "JARVIS-AI"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "Autonomous AI Operating System"
    FASTAPI_ENV: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = (
        "postgresql://jarvis_user:jarvis_password@localhost:5432/jarvis_db"
    )
    DATABASE_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_EXPIRE: int = 3600

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""
    QDRANT_COLLECTION_NAME: str = "jarvis_memories"
    QDRANT_VECTOR_SIZE: int = 1536

    # JWT
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Trusted hosts
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    HTTPS_ONLY: bool = False
    SECURE_COOKIES: bool = False

    # AI Models
    DEFAULT_MODEL_PROVIDER: str = "ollama"
    DEFAULT_MODEL: str = "mistral"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"

    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_QUEUE_NAME: str = "jarvis_tasks"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE: str = "logs/jarvis.log"

    # Voice Configuration
    VOICE_WAKE_WORD: str = "jarvis"
    VOICE_RECOGNITION_LANGUAGE: str = "en-US"
    VOICE_TTS_PROVIDER: str = "pyttsx3"
    VOICE_ENABLE_CONTINUOUS_LISTENING: bool = False

    # Feature Flags
    ENABLE_VOICE: bool = True
    ENABLE_VISION: bool = False
    ENABLE_AUTOMATION: bool = False
    ENABLE_AGENTS: bool = False
    ENABLE_PLUGINS: bool = False

    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    PROMETHEUS_PORT: int = 8001

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
