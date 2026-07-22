"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "jarvis-backend"


def test_auth_login():
    """Test login endpoint."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "testpass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_chat_message():
    """Test chat message endpoint."""
    response = client.post(
        "/api/v1/chat/message",
        json={"content": "Hello JARVIS", "conversation_id": None},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "assistant"
    assert "content" in data


def test_memory_store():
    """Test memory storage endpoint."""
    response = client.post(
        "/api/v1/memory/store",
        json={
            "content": "Test memory",
            "memory_type": "long_term",
            "importance_score": 0.8,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test memory"
    assert data["memory_type"] == "long_term"
