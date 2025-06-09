#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER
do
  sleep 1
done
echo "PostgreSQL is ready!"

# Apply database migrations
echo "Applying database migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 