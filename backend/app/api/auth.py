"""Authentication routes."""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from app.core.auth import create_access_token, get_password_hash, verify_password

router = APIRouter()


class RegisterRequest(BaseModel):
    """User registration request."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(default="", max_length=255)


class LoginRequest(BaseModel):
    """User login request."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.post("/register", response_model=dict[str, Any])
async def register(request: RegisterRequest) -> dict[str, Any]:
    """Register new user."""
    # TODO: Implement user registration
    return {
        "message": "User registration not yet implemented",
        "status": "pending",
    }


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    """Login user."""
    # TODO: Implement user login
    # For now return mock token
    access_token = create_access_token(
        data={"sub": request.username},
        expires_delta=timedelta(minutes=30),
    )
    return TokenResponse(
        access_token=access_token,
        expires_in=30 * 60,
    )


@router.post("/refresh")
async def refresh_token() -> TokenResponse:
    """Refresh access token."""
    # TODO: Implement token refresh
    access_token = create_access_token(data={"sub": "user"})
    return TokenResponse(
        access_token=access_token,
        expires_in=30 * 60,
    )


@router.post("/logout")
async def logout() -> dict[str, str]:
    """Logout user."""
    # TODO: Implement logout
    return {"message": "Logged out successfully"}
