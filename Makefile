# ─── Local Postgres (Docker) ───────────────────────────────────────────────
DB_CONTAINER  := todoai-postgres
DB_PORT       := 5432
DB_NAME       := todoai
DB_USER       := postgres
DB_PASSWORD   := postgres
LOCAL_DB_URL  := postgresql+psycopg://$(DB_USER):$(DB_PASSWORD)@localhost:$(DB_PORT)/$(DB_NAME)

ENV_FILE          := todoai-backend/api/.env
REMOTE_URL_BACKUP := .db-remote-url

BACKEND_DIR  := todoai-backend
API_DIR      := todoai-backend/api

FRONTEND_DIR := todoai-frontend

.PHONY: db-start db-stop db-status migrate-generate migrate-run server frontend help

# ─── Default target ────────────────────────────────────────────────────────
help:
	@printf "\nAvailable commands:\n\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@printf "\n"

# ─── db-start ──────────────────────────────────────────────────────────────
db-start: ## Start local Postgres in Docker and update .env DATABASE_URL
	@# Back up the currently active DATABASE_URL so we can restore it later
	@grep '^DATABASE_URL=' $(ENV_FILE) | sed 's/^DATABASE_URL=//' > $(REMOTE_URL_BACKUP)

	@# Create a new container on first run, otherwise just start the existing one
	@if docker ps -a --format '{{.Names}}' | grep -q '^$(DB_CONTAINER)$$'; then \
		docker start $(DB_CONTAINER); \
	else \
		echo "Creating container $(DB_CONTAINER)..."; \
		docker run -d \
			--name $(DB_CONTAINER) \
			-e POSTGRES_USER=$(DB_USER) \
			-e POSTGRES_PASSWORD=$(DB_PASSWORD) \
			-e POSTGRES_DB=$(DB_NAME) \
			-p $(DB_PORT):5432 \
			postgres:16; \
	fi

	@# Wait until Postgres is accepting connections
	@printf "Waiting for Postgres"
	@until docker exec $(DB_CONTAINER) pg_isready -U $(DB_USER) -q 2>/dev/null; do \
		printf '.'; sleep 1; \
	done
	@printf "\n"

	@# Swap DATABASE_URL in .env to the local instance
	@python3 -c "\
import re; \
content = open('$(ENV_FILE)').read(); \
content = re.sub(r'^DATABASE_URL=.*', 'DATABASE_URL=$(LOCAL_DB_URL)', content, flags=re.MULTILINE); \
open('$(ENV_FILE)', 'w').write(content)"

	@echo "✓ Postgres is up  →  localhost:$(DB_PORT)/$(DB_NAME)"
	@echo "✓ $(ENV_FILE) updated to use local database"

# ─── db-stop ───────────────────────────────────────────────────────────────
db-stop: ## Stop local Postgres and restore original DATABASE_URL in .env
	@docker stop $(DB_CONTAINER) 2>/dev/null \
		&& echo "Stopped $(DB_CONTAINER)" \
		|| echo "$(DB_CONTAINER) was not running"

	@# Restore DATABASE_URL from backup if it exists
	@if [ -f $(REMOTE_URL_BACKUP) ]; then \
		python3 - "$(ENV_FILE)" "$(REMOTE_URL_BACKUP)" <<'PYEOF'; \
import re, sys; \
env_file, backup_file = sys.argv[1], sys.argv[2]; \
remote_url = open(backup_file).read().strip(); \
content = open(env_file).read(); \
content = re.sub(r'^DATABASE_URL=.*', 'DATABASE_URL=' + remote_url, content, flags=re.MULTILINE); \
open(env_file, 'w').write(content) \
PYEOF \
		rm $(REMOTE_URL_BACKUP); \
		echo "✓ $(ENV_FILE) restored to previous DATABASE_URL"; \
	else \
		echo "⚠  No backup found — $(ENV_FILE) was not changed"; \
	fi

# ─── db-status ─────────────────────────────────────────────────────────────
db-status: ## Show the Postgres container status
	@docker ps -a --filter "name=^/$(DB_CONTAINER)$$" \
		--format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# ─── migrate-generate ──────────────────────────────────────────────────────
migrate-generate: ## Generate a new Alembic migration (prompts for name)
	@if [ -n "$(name)" ]; then \
		cd $(API_DIR) && uv run alembic revision --autogenerate -m "$(name)"; \
	else \
		read -p "Migration name: " m && cd $(API_DIR) && uv run alembic revision --autogenerate -m "$$m"; \
	fi

# ─── migrate-run ───────────────────────────────────────────────────────────
migrate-run: ## Apply all pending migrations (alembic upgrade head)
	cd $(API_DIR) && uv run alembic upgrade head

# ─── server ────────────────────────────────────────────────────────────────
server: ## Start the FastAPI dev server (port 8000, auto-reload)
	cd $(BACKEND_DIR) && uv run uvicorn todoai_api.main:app --reload --host 0.0.0.0 --port 8000

# ─── frontend ──────────────────────────────────────────────────────────────
frontend: ## Start the Next.js dev server (port 3000, auto-reload)
	cd $(FRONTEND_DIR) && npm run dev
