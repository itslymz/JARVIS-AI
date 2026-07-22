"""Unit tests for authentication utilities."""

import pytest
from datetime import timedelta

from app.core.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_token,
)


def test_password_hashing():
    """Test password hashing and verification."""
    password = "test_password_123"
    hashed = get_password_hash(password)

    # Verify correct password
    assert verify_password(password, hashed)

    # Verify incorrect password
    assert not verify_password("wrong_password", hashed)


def test_token_creation():
    """Test JWT token creation."""
    data = {"sub": "testuser"}
    token = create_access_token(data)

    assert isinstance(token, str)
    assert len(token) > 0


def test_token_decode():
    """Test JWT token decoding."""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded = decode_token(token)

    assert decoded is not None
    assert decoded["sub"] == "testuser"


def test_invalid_token():
    """Test invalid token decoding."""
    invalid_token = "invalid.token.here"
    decoded = decode_token(invalid_token)

    assert decoded is None
