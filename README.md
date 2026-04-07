# TodoAI

AI-powered task scheduling app — Next.js frontend + FastAPI backend + PostgreSQL.

## Project Structure

```
task_scheduling/
├── todoai-frontend/   # Next.js 15, TypeScript, Tailwind, CopilotKit AI chat
├── todoai-backend/    # Python uv workspace
│   ├── api/           # FastAPI app + Alembic migrations
│   ├── ai/            # LangChain / Anthropic streaming
│   └── common/        # Shared SQLAlchemy models & Pydantic schemas
└── Makefile           # All dev commands
```

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Node.js | 20+ | https://nodejs.org |
| Python | 3.12+ | https://python.org |
| uv | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Docker | latest | https://docs.docker.com/get-docker/ |

## Quick Start

### 1. Clone and configure

```bash
git clone <repo-url>
cd task_scheduling
```

**Backend** — copy and fill in `todoai-backend/api/.env`:
```bash
cp todoai-backend/api/.env.example todoai-backend/api/.env
```

**Frontend** — copy and fill in `todoai-frontend/.env.local`:
```bash
cp todoai-frontend/.env.local.example todoai-frontend/.env.local
```

### 2. Install dependencies

```bash
# Backend (installs all workspace packages)
cd todoai-backend && uv sync && cd ..

# Frontend
cd todoai-frontend && npm install && cd ..
```

### 3. Start the database

```bash
make db-start       # pulls postgres:16, starts container, updates .env automatically
make migrate-run    # applies all Alembic migrations
```

### 4. Start the servers

Open two terminals:

```bash
make server     # FastAPI on http://localhost:8000
make frontend   # Next.js on http://localhost:3000
```

API docs: http://localhost:8000/docs

---

## All Make Commands

```
make help               List all commands

# Database
make db-start           Start local Postgres (Docker) + update DATABASE_URL in .env
make db-stop            Stop local Postgres + restore previous DATABASE_URL
make db-status          Show container status

# Migrations
make migrate-generate   Generate a new Alembic migration (prompts for name)
make migrate-run        Apply all pending migrations (upgrade head)

# Servers
make server             Start FastAPI dev server  (port 8000)
make frontend           Start Next.js dev server  (port 3000)
```

---

## Environment Variables

### Backend — `todoai-backend/api/.env`

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string — auto-managed by `make db-start/db-stop` |
| `SECRET_KEY` | JWT signing secret (`openssl rand -hex 32`) |
| `ALGORITHM` | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `ANTHROPIC_API_KEY` | Anthropic API key for AI features |

### Frontend — `todoai-frontend/.env.local`

| Variable | Description |
|---|---|
| `NEXTAUTH_URL` | App URL (`http://localhost:3000`) |
| `NEXTAUTH_SECRET` | Random secret (`openssl rand -hex 32`) |
| `AUTH_GOOGLE_ID` | Google OAuth client ID |
| `AUTH_GOOGLE_SECRET` | Google OAuth client secret |
| `NEXT_PUBLIC_API_URL` | Backend base URL (`http://localhost:8000/api/v1`) |
| `ANTHROPIC_API_KEY` | Anthropic API key (used by the CopilotKit chat endpoint) |

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com) → APIs & Services → Credentials
2. Create an OAuth 2.0 Client ID (Web application)
3. Add to **Authorized redirect URIs**:
   - `http://localhost:3000/api/auth/callback/google`
4. Copy the Client ID and Secret into both `.env` files
