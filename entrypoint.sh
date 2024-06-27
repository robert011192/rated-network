#!/bin/sh

# Run migrations (if applicable, assuming alembic is set up)
alembic upgrade head

# Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000
