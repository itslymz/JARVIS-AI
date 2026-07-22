"""Pydantic schemas for API requests/responses."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update schema."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Message Schemas
class MessageRequest(BaseModel):
    """Message request schema."""
    content: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[int] = None


class MessageResponse(BaseModel):
    """Message response schema."""
    id: int
    role: str
    content: str
    created_at: datetime
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None

    class Config:
        from_attributes = True


# Conversation Schemas
class ConversationBase(BaseModel):
    """Base conversation schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    model: str = "ollama"


class ConversationCreate(ConversationBase):
    """Conversation creation schema."""
    pass


class ConversationResponse(ConversationBase):
    """Conversation response schema."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    archived: bool
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True


# Memory Schemas
class MemoryRequest(BaseModel):
    """Memory storage request schema."""
    content: str = Field(..., min_length=1)
    memory_type: str = Field(..., regex="^(short_term|long_term|semantic|procedural|preferences|task_history|project)$")
    importance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    metadata: Optional[dict] = None


class MemoryResponse(BaseModel):
    """Memory response schema."""
    id: int
    content: str
    memory_type: str
    importance_score: float
    metadata: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MemoryRetrievalRequest(BaseModel):
    """Memory retrieval request schema."""
    query: str = Field(..., min_length=1)
    memory_type: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=100)


# User Preferences Schemas
class UserPreferencesResponse(BaseModel):
    """User preferences response schema."""
    id: int
    preferred_model: str
    preferred_language: str
    voice_enabled: bool
    voice_wake_word: str
    temperature: float
    max_tokens: int
    theme: str
    notifications_enabled: bool

    class Config:
        from_attributes = True


class UserPreferencesUpdate(BaseModel):
    """User preferences update schema."""
    preferred_model: Optional[str] = None
    preferred_language: Optional[str] = None
    voice_enabled: Optional[bool] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    theme: Optional[str] = None


# Task History Schemas
class TaskHistoryResponse(BaseModel):
    """Task history response schema."""
    id: int
    task_name: str
    task_description: Optional[str] = None
    status: str
    result: Optional[str] = None
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Auth Schemas
class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token data schema."""
    sub: Optional[str] = None
    exp: Optional[int] = None
