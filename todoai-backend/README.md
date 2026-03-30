# todoai-backend

Python monorepo for the todoai FastAPI backend.

## Structure

- `common/` — `todoai-common` package: SQLAlchemy models, Pydantic schemas, enums
- `api/` — `todoai-api` FastAPI application

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- PostgreSQL

## Setup

```bash
# Install all workspace packages
uv sync

# Configure environment
cp api/.env.example api/.env
# Edit api/.env with your values

# Create database
createdb todoai

# Generate migrations
cd api && uv run alembic revision --autogenerate -m "geneate migrations"

# Run migrations
cd api && uv run alembic upgrade head

# Start server
cd .. && uv run uvicorn todoai_api.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs
