#!/bin/bash
# Database migration script

set -e

echo "=== Database Migration ==="

cd backend

# Check if alembic is available
if ! command -v alembic &> /dev/null; then
    echo "Installing Alembic..."
    pip install alembic
fi

echo "Running migrations..."
alembic upgrade head

echo "✓ Migrations complete"
