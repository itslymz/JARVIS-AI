"""Documentation setup instructions."""

# JARVIS-AI Phase 1 Setup Guide

## Prerequisites

- Docker & Docker Compose
- Git
- Python 3.11+ (for development)
- Node.js 18+ (for frontend development)

## Quick Start with Docker

### 1. Clone Repository

```bash
git clone https://github.com/itslymz/JARVIS-AI.git
cd JARVIS-AI
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- Set API keys if using cloud models (OpenAI, Anthropic)
- Configure database URL (defaults to Docker setup)
- Set JWT secret key

### 3. Start with Docker Compose

```bash
docker-compose up --build
```

This will start:
- **Backend** (FastAPI): http://localhost:8000
- **Frontend** (React): http://localhost:3000
- **PostgreSQL**: port 5432
- **Redis**: port 6379
- **Qdrant**: http://localhost:6333
- **RabbitMQ**: http://localhost:5672 (management: 15672)
- **Ollama**: http://localhost:11434
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

### 4. Initialize Ollama Models

In a new terminal:

```bash
docker exec jarvis-ollama ollama pull mistral
docker exec jarvis-ollama ollama pull neural-chat
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000/api/v1/
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001
- **RabbitMQ**: http://localhost:15672 (guest/guest)

## Development Setup (Manual)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

## Database Migrations

Migrations are handled automatically through SQLAlchemy on startup.

To create new migrations:

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## API Documentation

Once the backend is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL container
docker logs jarvis-postgres

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

### Redis Connection Issues

```bash
# Test Redis connection
docker exec jarvis-redis redis-cli ping
```

### Qdrant Issues

```bash
# Check Qdrant health
curl http://localhost:6333/health
```

### Ollama Not Available

```bash
# Check Ollama status
docker logs jarvis-ollama

# Ensure models are pulled
docker exec jarvis-ollama ollama list
```

## Configuration

All configuration is done through environment variables. See `.env.example` for all options.

### Key Variables

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# Redis
REDIS_URL=redis://host:port/db

# Qdrant
QDRANT_URL=http://localhost:6333

# AI Models
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OLLAMA_BASE_URL=http://localhost:11434

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
```

## Project Structure

```
JARVIS-AI/
├── backend/           # FastAPI backend
├── frontend/          # React/Next.js frontend
├── docker/            # Docker configurations
├── docker-compose.yml # Main compose file
└── README.md          # Project documentation
```

## Next Steps (Phase 2)

- Computer automation (Windows control)
- Advanced vision (screen capture, OCR)
- Web browsing
- Autonomous agents
- Plugin system

## Support

For issues and questions, please open an issue on GitHub.
