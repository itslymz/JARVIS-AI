"""API documentation."""

# JARVIS-AI API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer {token}
```

## Endpoints

### Authentication

#### Register User

```
POST /auth/register
```

Request:
```json
{
  "username": "jarvis_user",
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

Response:
```json
{
  "id": 1,
  "username": "jarvis_user",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### Login

```
POST /auth/login
```

Request:
```json
{
  "username": "jarvis_user",
  "password": "securepassword"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Chat

#### Send Message

```
POST /chat/message
```

Request:
```json
{
  "content": "What's the weather?",
  "conversation_id": 1
}
```

Response:
```json
{
  "id": 1,
  "role": "assistant",
  "content": "I don't have access to real-time weather data, but...",
  "timestamp": "2024-01-01T00:00:00Z",
  "tokens_used": 150,
  "model_used": "ollama"
}
```

#### List Conversations

```
GET /chat/conversations
```

Response:
```json
[
  {
    "id": 1,
    "title": "First Conversation",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "archived": false
  }
]
```

#### Create Conversation

```
POST /chat/conversations
```

Request:
```json
{
  "title": "My First Chat",
  "model": "ollama"
}
```

### Memory

#### Store Memory

```
POST /memory/store
```

Request:
```json
{
  "content": "User prefers dark mode interface",
  "memory_type": "preferences",
  "importance_score": 0.8,
  "metadata": {"category": "ui"}
}
```

Response:
```json
{
  "id": 1,
  "content": "User prefers dark mode interface",
  "memory_type": "preferences",
  "importance_score": 0.8,
  "metadata": {"category": "ui"},
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### Retrieve Memories

```
GET /memory/retrieve?query=dark+mode
```

Response:
```json
[
  {
    "id": 1,
    "content": "User prefers dark mode interface",
    "memory_type": "preferences",
    "importance_score": 0.8,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### List Memories

```
GET /memory/list?memory_type=preferences&limit=10
```

### Health Check

```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "service": "jarvis-backend",
  "version": "0.1.0"
}
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error description"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad request
- `401`: Unauthorized
- `404`: Not found
- `500`: Server error

## Rate Limiting

Rate limiting will be implemented in Phase 2.

## Pagination

Endpoints supporting pagination use `limit` and `offset` parameters.
