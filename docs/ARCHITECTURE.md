# Architecture Overview

## System Design

JARVIS-AI is built as a microservices architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                          │
│                        :3000                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Nginx Reverse Proxy                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────┴─────────┐
                    ▼                  ▼
         ┌──────────────────┐  ┌──────────────────┐
         │  FastAPI Backend │  │  WebSocket (WS)  │
         │     :8000        │  │                  │
         └────────┬─────────┘  └──────────────────┘
                  │
       ┌──────────┼──────────┬────────────┐
       ▼          ▼          ▼            ▼
   ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
   │  Auth  │ │ Chat   │ │ Memory │ │  Health  │
   │ Routes │ │ Routes │ │ Routes │ │          │
   └───┬────┘ └───┬────┘ └───┬────┘ └──────────┘
       │          │          │
       └──────────┼──────────┘
                  ▼
       ┌──────────────────────┐
       │   Core Services      │
       ├──────────────────────┤
       │ - AI Model Selector  │
       │ - Chat Manager       │
       │ - Memory Manager     │
       │ - Auth Manager       │
       └──────────┬───────────┘
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
 ┌─────────┐ ┌─────────┐ ┌──────────┐
 │   AI    │ │ Memory  │ │  Voice   │
 │ Engines │ │ Systems │ │ Systems  │
 └────┬────┘ └────┬────┘ └──────────┘
      │          │
      ▼          ▼
  ┌──────────────────────────┐
  │  Data & Vector Storage   │
  ├──────────────────────────┤
  │ - PostgreSQL (Structured)│
  │ - Qdrant (Semantic)      │
  │ - Redis (Cache)          │
  │ - RabbitMQ (Queue)       │
  └──────────────────────────┘
```

## Components

### Frontend Layer

- **Next.js React App**: Modern UI framework
- **TailwindCSS**: Styling
- **React Query**: Data fetching
- **Zustand**: State management
- **Socket.io**: Real-time communication

### API Layer

- **FastAPI**: Async web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **JWT**: Authentication

### Service Layer

#### Chat Service
- Message processing
- Conversation management
- AI model integration
- Response generation

#### Memory Service
- Short-term: Conversation context
- Long-term: Knowledge storage
- Semantic: Vector embeddings
- Procedural: Learned behaviors
- Preferences: User settings

#### Voice Service
- Speech recognition
- Text-to-speech
- Voice activity detection
- Audio processing

#### Authentication Service
- User registration
- Login/logout
- Token generation
- Permission checking

### Data Layer

#### PostgreSQL
- User accounts
- Conversations
- Messages
- Memories (metadata)
- Task history
- Audit logs

#### Qdrant
- Semantic memory embeddings
- Similarity search
- Vector clustering

#### Redis
- Session cache
- Token blacklist
- Rate limiting
- General caching

#### RabbitMQ
- Async task queue
- Message routing
- Event publishing

### AI Integration

#### Model Selector
- Automatic best model selection
- Fallback handling
- Provider configuration

#### Supported Models
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Ollama (Local open-source)
- Planned: Google Gemini, DeepSeek, Qwen

### Monitoring & Observability

- **Prometheus**: Metrics collection
- **Grafana**: Dashboards
- **Logging**: Structured JSON logs

## Data Flow

### Chat Message Flow

```
1. User sends message via Frontend
   ↓
2. API endpoint receives message
   ↓
3. Authentication middleware validates token
   ↓
4. Message stored in PostgreSQL
   ↓
5. Message added to short-term memory
   ↓
6. Relevant memories retrieved (semantic search)
   ↓
7. Prompt constructed with context
   ↓
8. AI model selected and called
   ↓
9. Response generated
   ↓
10. Response stored in PostgreSQL
   ↓
11. Response added to semantic memory
   ↓
12. Response sent to Frontend
   ↓
13. UI updated with message
```

## Memory Architecture

### Short-Term Memory
- Recent conversation context
- In-memory storage (configurable size)
- Automatically cleared on new session

### Long-Term Memory
- User knowledge and facts
- Persistent storage in PostgreSQL
- Importance scoring

### Semantic Memory
- Vector embeddings
- Similarity-based retrieval
- Stored in Qdrant

### Procedural Memory
- Learned workflows
- Success/failure rates
- In-memory cache

### Preferences Memory
- User settings
- Learned preferences
- Updated over time

## Authentication Flow

```
1. User submits login credentials
   ↓
2. Password verified against hash
   ↓
3. JWT token generated
   ↓
4. Token returned to client
   ↓
5. Client includes token in Authorization header
   ↓
6. Middleware validates token
   ↓
7. User ID extracted from token
   ↓
8. Request processed with user context
```

## Scalability Considerations

### Horizontal Scaling
- Stateless backend instances
- Load balancing with Nginx
- Shared database connections
- Redis for session state

### Caching Strategy
- Redis for frequent queries
- Memory-based short-term cache
- Semantic similarity caching

### Database Optimization
- Connection pooling
- Query indexing
- Lazy loading relationships
- Partitioning for large tables

## Security Architecture

### Authentication
- JWT tokens with expiration
- Refresh token rotation
- Secure password hashing (bcrypt)

### Authorization
- User-scoped data isolation
- Role-based access control (planned)
- Audit logging

### Data Protection
- HTTPS in production
- Environment variable secrets
- SQL injection prevention (ORM)
- CORS configuration

## Error Handling

### Global Error Handler Middleware
- Catches unhandled exceptions
- Returns standardized error responses
- Logs errors for debugging

### Graceful Degradation
- Model fallback chain
- Cache bypass on failure
- User-friendly error messages

## Future Enhancements

### Phase 2
- Computer automation capabilities
- Advanced vision (OCR, object detection)
- Web browsing and research
- Autonomous agents framework

### Phase 3
- Self-improvement engine
- Multi-agent coordination
- Plugin system
- Advanced memory management

### Phase 4
- Production hardening
- Enterprise features
- Advanced analytics
- Multi-tenant support
