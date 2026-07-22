# Development Guide

## Setting Up Development Environment

### Backend Development

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run backend**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Development

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Run frontend**
   ```bash
   npm run dev
   ```

## Code Quality

### Running Linters

```bash
cd backend

# Black (code formatting)
black app/

# Ruff (linting)
ruff check app/

# MyPy (type checking)
mypy app/
```

### Running Tests

```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

## Project Structure

### Backend

- `app/main.py` - FastAPI application entry point
- `app/config.py` - Configuration management
- `app/core/` - Core business logic
  - `auth.py` - Authentication utilities
  - `database.py` - Database connection
  - `cache.py` - Redis cache
  - `vector_db.py` - Qdrant integration
- `app/api/` - API routes
- `app/models/` - Database models and AI integrations
- `app/memory/` - Memory systems
- `app/voice/` - Voice capabilities
- `app/middleware/` - Custom middleware
- `app/schemas/` - Pydantic schemas

### Frontend

- `src/pages/` - Next.js pages/routes
- `src/components/` - React components
- `src/hooks/` - Custom hooks
- `src/services/` - API client services
- `src/types/` - TypeScript types
- `src/styles/` - CSS/Tailwind styles

## Making Changes

### Adding a New API Endpoint

1. Create route file in `app/api/`
2. Define Pydantic schemas in `app/schemas/`
3. Create database models if needed
4. Add tests in `tests/`
5. Include router in `app/main.py`

Example:

```python
# app/api/example.py
from fastapi import APIRouter
from app.schemas.base import ExampleResponse

router = APIRouter()

@router.get("/example", response_model=ExampleResponse)
async def get_example() -> ExampleResponse:
    """Get example."""
    return ExampleResponse(id=1, name="example")
```

### Adding a New Memory Type

1. Create module in `app/memory/`
2. Implement memory interface
3. Add to `app/memory/__init__.py`
4. Add tests

### Adding Database Models

1. Define model in `app/models/database.py`
2. Create migration:
   ```bash
   alembic revision --autogenerate -m "Add new model"
   alembic upgrade head
   ```
3. Create Pydantic schema in `app/schemas/`

## Git Workflow

1. Create feature branch
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make changes and commit
   ```bash
   git add .
   git commit -m "Add my feature"
   ```

3. Push and create pull request
   ```bash
   git push origin feature/my-feature
   ```

## Debugging

### Backend Debugging

Use print statements or Python debugger:

```python
import pdb; pdb.set_trace()
```

Or use VS Code debugger with launch configuration:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

### Frontend Debugging

Use React Developer Tools and browser DevTools.

## Common Issues

### Database connection refused

```bash
# Check if PostgreSQL container is running
docker ps | grep postgres

# Start it if not running
docker-compose up -d postgres
```

### Port already in use

```bash
# Find process using port
lsof -i :8000  # On Mac/Linux
netstat -ano | findstr :8000  # On Windows

# Kill the process or change port
```

## Performance Optimization

### Database

- Add indexes on frequently queried columns
- Use connection pooling
- Implement query caching with Redis

### Frontend

- Code splitting with dynamic imports
- Image optimization
- Lazy loading components

## Deployment

See SETUP.md for Docker deployment information.

For production:
1. Use environment variables for secrets
2. Enable HTTPS
3. Set up monitoring with Prometheus/Grafana
4. Configure backup strategies
5. Implement CI/CD pipeline
