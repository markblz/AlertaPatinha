.PHONY: up down build restart ps logs logs.backend logs.web logs.db shell psql \
        migrate migration test test-yours lint format typecheck imports check \
        web-add web-deps web-build web-typecheck api-contract health gen-secrets

# Host UID/GID so the backend container can write bind-mounted files
# (alembic revisions) as you, not root.
export UID := $(shell id -u)
export GID := $(shell id -g)

DC := docker compose

# ── Stack ──────────────────────────────────────────────────────────────────

up:
	$(DC) up -d

down:
	$(DC) down

build:
	$(DC) build

restart:
	$(DC) up -d --build backend web

ps:
	$(DC) ps

logs:
	$(DC) logs -f --tail=200

logs.backend:
	$(DC) logs -f --tail=200 backend

logs.web:
	$(DC) logs -f --tail=200 web

logs.db:
	$(DC) logs -f --tail=200 postgres

shell:
	$(DC) exec backend bash

psql:
	$(DC) exec postgres sh -c 'psql -U $$POSTGRES_USER -d $$POSTGRES_DB'

health:
	@curl -fsS http://localhost:$${HOST_BACKEND_PORT:-8100}/api/v1/health/ready && echo

# ── Database ───────────────────────────────────────────────────────────────

migrate:
	$(DC) exec backend alembic upgrade head

# usage: make migration MSG="observations: create relato tables"
migration:
	@test -n "$(MSG)" || (echo 'MSG is required: make migration MSG="..."' && exit 1)
	$(DC) exec backend alembic revision --autogenerate -m "$(MSG)"

# ── Quality gates (run on the host with uv; CI runs the same) ─────────────

test:
	cd apps/backend && uv run pytest -q

# 🧠 the owner-implemented core logic only (no database needed)
test-yours:
	cd apps/backend && uv run pytest -q tests/geo tests/observations

lint:
	cd apps/backend && uv run ruff check . && uv run ruff format --check .

format:
	cd apps/backend && uv run ruff format . && uv run ruff check --fix .

typecheck:
	cd apps/backend && uv run mypy api src

imports:
	cd apps/backend && uv run lint-imports

check: lint typecheck imports test

# ── Frontend deps: ALWAYS inside the container (musl vs glibc) ─────────────

# usage: make web-add PKG="pmtiles"   (dev deps: PKG="-D vitest")
web-add:
	@test -n "$(PKG)" || (echo 'PKG is required: make web-add PKG="name"' && exit 1)
	$(DC) exec web pnpm add $(PKG)
	@# pnpm rewrites these as the container's root; hand them back to you.
	$(DC) exec web chown $(UID):$(GID) package.json pnpm-lock.yaml

web-deps:
	$(DC) exec web pnpm install --frozen-lockfile

web-build:
	$(DC) exec web pnpm build

web-typecheck:
	$(DC) exec web pnpm typecheck && $(DC) exec web pnpm check:arch

# ── API contract: backend OpenAPI → typed client (web now, native app later) ─
# openapi-typescript needs TypeScript's JS API, gone in TS 7: run it isolated
# with TS 6 instead of adding a second TypeScript to the project.
api-contract:
	cd apps/backend && uv run python -m api.export_openapi > ../frontend/core/api/openapi.json
	$(DC) exec -u $(UID):$(GID) -e HOME=/tmp web pnpm dlx \
		--package=openapi-typescript@7.13.0 --package=typescript@6.0.3 \
		openapi-typescript core/api/openapi.json -o core/api/schema.d.ts

# ── Secrets ────────────────────────────────────────────────────────────────

gen-secrets:
	@echo "POSTGRES_PASSWORD=$$(openssl rand -hex 24)"
	@echo "CENTRIFUGO_HMAC_SECRET=$$(openssl rand -hex 32)"
	@echo "CENTRIFUGO_API_KEY=$$(openssl rand -hex 32)"
