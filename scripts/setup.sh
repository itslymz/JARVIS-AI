#!/bin/bash
# Setup script for JARVIS-AI

set -e

echo "=== JARVIS-AI Setup ==="
echo ""

# Create .env if not exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env created. Please configure with your settings."
else
    echo "✓ .env already exists."
fi

echo ""
echo "=== Docker Setup ==="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "✗ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✓ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "✗ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker Compose is installed"

echo ""
echo "=== Starting Services ==="

# Start services
docker-compose up -d

echo "✓ Services started"

echo ""
echo "=== Waiting for Services ==="

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
for i in {1..30}; do
    if docker exec jarvis-postgres pg_isready -U jarvis_user &> /dev/null; then
        echo "✓ PostgreSQL is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "✗ PostgreSQL failed to start"
        exit 1
    fi
    sleep 1
done

# Wait for Redis
echo "Waiting for Redis..."
for i in {1..30}; do
    if docker exec jarvis-redis redis-cli ping &> /dev/null; then
        echo "✓ Redis is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "✗ Redis failed to start"
        exit 1
    fi
    sleep 1
done

# Wait for Qdrant
echo "Waiting for Qdrant..."
for i in {1..30}; do
    if curl -s http://localhost:6333/health &> /dev/null; then
        echo "✓ Qdrant is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "✗ Qdrant failed to start"
        exit 1
    fi
    sleep 1
done

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Services are running:"
echo "  Frontend: http://localhost:3000"
echo "  Backend: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo "  Grafana: http://localhost:3001 (admin/admin)"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"
echo ""
