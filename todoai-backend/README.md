# todoai-backend

Python uv workspace — FastAPI backend for the TodoAI task scheduling app.

## Structure

```
todoai-backend/
├── api/        # FastAPI application + Alembic migrations
├── ai/         # LangChain / Anthropic streaming (todoai-ai package)
└── common/     # Shared SQLAlchemy models, Pydantic schemas, enums (todoai-common)
```

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- PostgreSQL (or use `make db-start` from the repo root to run it in Docker)

## Setup

### 1. Install workspace packages

```bash
uv sync
```

This installs `todoai-api`, `todoai-ai`, and `todoai-common` together with all their dependencies.

### 2. Configure environment

```bash
cp api/.env.example api/.env
# Edit api/.env with your values
```

> **Tip:** If you use `make db-start` from the repo root, `DATABASE_URL` in `api/.env` is updated automatically.

### 3. Run migrations

```bash
# From repo root (recommended)
make migrate-run

# Or directly
cd api && uv run alembic upgrade head
```

### 4. Start the server

```bash
# From repo root (recommended)
make server

# Or directly
uv run uvicorn todoai_api.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

---

## Make Commands (run from repo root)

| Command | Description |
|---|---|
| `make db-start` | Start local Postgres in Docker + auto-update `DATABASE_URL` |
| `make db-stop` | Stop Postgres + restore previous `DATABASE_URL` |
| `make db-status` | Show container status |
| `make migrate-generate` | Generate a new migration (prompts for name) |
| `make migrate-run` | Apply all pending migrations |
| `make server` | Start FastAPI dev server on port 8000 |

---

## Environment Variables — `api/.env`

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | Yes | PostgreSQL connection string — auto-managed by `make db-start/db-stop` |
| `SECRET_KEY` | Yes | JWT signing secret — generate with `openssl rand -hex 32` |
| `ALGORITHM` | No | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Access token TTL (default: `15`) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | No | Refresh token TTL (default: `30`) |
| `GOOGLE_CLIENT_ID` | Yes | Google OAuth client ID |
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for AI streaming features |

## Stack

- **FastAPI** 0.115+ with async SQLAlchemy
- **uv** workspace (monorepo with `common`, `ai`, `api` packages)
- **Alembic** for database migrations
- **LangChain Anthropic** (`claude-sonnet-4`) for streaming AI responses
- **PostgreSQL** via `psycopg` (v3)
- **JWT** auth with Google OAuth (issued by backend, consumed by frontend via NextAuth)
