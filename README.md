# JARVIS-AI: Autonomous AI Operating System

**JARVIS** is a production-ready autonomous AI assistant inspired by Iron Man's JARVIS. It's an enterprise-grade operating system that manages tasks, remembers information, learns from experience, and continuously improves through modular upgrades.

## 🎯 Vision

JARVIS is NOT a chatbot. It is:
- An autonomous AI operating system
- Modular and scalable microservice architecture
- Production-ready and enterprise-grade
- Capable of understanding natural language
- Memory-aware with multiple memory layers
- Voice-enabled (continuous listening, NTT, speech recognition)
- Vision-capable (screen understanding, OCR, image analysis)
- Windows computer control
- Web browsing and research
- Autonomous agent creation
- Self-improving through an improvement engine
- Secure with sandboxing and permission systems

## 🏗️ Architecture

### Frontend
- **React** + **Next.js** for modern UI
- **TypeScript** for type safety
- **TailwindCSS** for styling

### Backend
- **Python** with **FastAPI** for async architecture
- **PostgreSQL** for structured data
- **Qdrant** for semantic/vector memory
- **Redis** for caching
- **RabbitMQ** for message queuing

### AI Models
Support for multiple providers:
- OpenAI
- Anthropic (Claude)
- Google Gemini
- DeepSeek
- Qwen
- Llama (via Ollama)
- Mistral
- LM Studio

### Infrastructure
- **Docker** + **Docker Compose** for containerization
- **JWT** + **OAuth2** for authentication
- **Prometheus** + **Grafana** for monitoring

## 📁 Project Structure

```
JARVIS-AI/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── config.py       # Configuration management
│   │   ├── dependencies.py # Dependency injection
│   │   ├── api/            # API routes
│   │   ├── core/           # Core business logic
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business services
│   │   ├── middleware/     # Middleware
│   │   └── utils/          # Utilities
│   ├── tests/              # Unit and integration tests
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Docker configuration
│   └── .env.example        # Environment variables template
│
├── frontend/               # Next.js React frontend
│   ├── src/
│   │   ├── pages/          # Next.js pages/routes
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API client services
│   │   ├── context/        # React context
│   │   ├── types/          # TypeScript types
│   │   ├── styles/         # TailwindCSS styles
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   ├── package.json        # Node dependencies
│   ├── tsconfig.json       # TypeScript config
│   ├── next.config.js      # Next.js config
│   ├── tailwind.config.js  # TailwindCSS config
│   ├── Dockerfile          # Docker configuration
│   └── .env.example        # Environment variables template
│
├── agents/                 # Autonomous agents
│   ├── base/               # Base agent classes
│   ├── research/           # Research agent
│   ├── programming/        # Programming agent
│   ├── writing/            # Writing agent
│   └── __init__.py
│
├── memory/                 # Memory system
│   ├── short_term.py       # Conversation memory
│   ├── long_term.py        # Knowledge memory
│   ├── semantic.py         # Semantic memory (Qdrant)
│   ├── procedural.py       # Procedural memory
│   ├── preferences.py      # User preferences
│   └── __init__.py
│
├── voice/                  # Voice system
│   ├── recognition.py      # Speech recognition
│   ├── synthesis.py        # Text-to-speech
│   ├── detection.py        # Voice activity detection
│   └── __init__.py
│
├── vision/                 # Vision system
│   ├── screen.py           # Screen capture and analysis
│   ├── ocr.py              # Optical character recognition
│   ├── detection.py        # Object detection
│   └── __init__.py
│
├── automation/             # Computer control
│   ├── windows.py          # Windows automation
│   ├── applications.py     # Application control
│   ├── keyboard.py         # Keyboard automation
│   ├── mouse.py            # Mouse automation
│   └── __init__.py
│
├── models/                 # AI model integrations
│   ├── base.py             # Base model interface
│   ├── openai_model.py     # OpenAI integration
│   ├── anthropic_model.py  # Anthropic integration
│   ├── ollama_model.py     # Ollama integration
│   ├── model_selector.py   # Model selection logic
│   └── __init__.py
│
├── plugins/                # Plugin system
│   ├── base.py             # Base plugin class
│   ├── registry.py         # Plugin registry
│   └── __init__.py
│
├── tools/                  # Tool calling framework
│   ├── base.py             # Base tool interface
│   ├── registry.py         # Tool registry
│   ├── python_exec.py      # Python execution
│   ├── shell_exec.py       # Shell execution
│   ├── git.py              # Git operations
│   ├── filesystem.py       # File operations
│   ├── web.py              # Web operations
│   └── __init__.py
│
├── docker/                 # Docker configurations
│   ├── docker-compose.yml  # Main compose file
│   └── nginx.conf          # Nginx reverse proxy
│
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── conftest.py         # Pytest configuration
│
├── docs/                   # Documentation
│   ├── API.md              # API documentation
│   ├── ARCHITECTURE.md     # Architecture guide
│   ├── SETUP.md            # Setup guide
│   └── DEVELOPMENT.md      # Development guide
│
├── scripts/                # Utility scripts
│   ├── setup.sh            # Setup script
│   ├── migrate.sh          # Database migration
│   └── seed.sh             # Database seeding
│
├── .env.example            # Environment template
├── docker-compose.yml      # Main Docker Compose
├── pyproject.toml          # Python project config
└── LICENSE
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- Python 3.11+
- Node.js 18+

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/itslymz/JARVIS-AI.git
   cd JARVIS-AI
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Setup (Development)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🔧 Configuration

See `.env.example` for all available configuration options:

```env
# FastAPI
FASTAPI_ENV=development
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/jarvis

# Redis
REDIS_URL=redis://localhost:6379

# Qdrant
QDRANT_URL=http://localhost:6333

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Models
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
OLLAMA_BASE_URL=http://localhost:11434

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Setup Instructions](docs/SETUP.md)
- [Development Guide](docs/DEVELOPMENT.md)

## 🧪 Testing

```bash
# Run backend tests
cd backend
pytest

# Run frontend tests
cd frontend
npm test
```

## 📦 Phase 1 Components

✅ Project Structure
✅ Docker Setup
✅ FastAPI Backend with Authentication
✅ React Frontend
✅ PostgreSQL Database
✅ Qdrant Vector Database
✅ Redis Cache
✅ Memory System
✅ Chat Interface
✅ Voice Input/Output (Infrastructure)
✅ Ollama Integration

## 🔐 Security

- JWT-based authentication
- OAuth2 support ready
- Environment variable secrets management
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with ORM
- Rate limiting ready

## 🛣️ Roadmap

### Phase 1 (Current)
- ✅ Project structure and Docker
- ✅ FastAPI + React foundation
- ✅ Authentication system
- ✅ Memory and chat interface
- ✅ Voice infrastructure

### Phase 2
- Computer automation (Windows control)
- Advanced vision (screen capture, OCR)
- Web browsing and research
- Autonomous agents framework

### Phase 3
- Improvement engine
- Plugin system
- Tool calling framework
- Advanced memory management

### Phase 4
- Self-improvement capabilities
- Multi-agent coordination
- Production hardening
- Enterprise features

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**itslymz** - Building the future of AI assistance

## 🤝 Contributing

Contributions are welcome! Please see DEVELOPMENT.md for guidelines.

---

**Built with ❤️ for autonomous intelligence**
