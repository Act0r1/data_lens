.PHONY: up down build rebuild logs db backend frontend bash migrate migrate-generate clean \
	up-prod down-prod build-prod rebuild-prod logs-prod bash-prod migrate-prod clean-prod \
	dev-backend dev-frontend

COMPOSE = docker compose -f docker-compose.yml
COMPOSE_PROD = docker compose -f docker-compose.prod.yml

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build

rebuild:
	$(COMPOSE) up -d --build --force-recreate

logs:
	$(COMPOSE) logs -f

db:
	$(COMPOSE) up -d db

backend:
	$(COMPOSE) up -d --build db migrate backend

frontend:
	$(COMPOSE) up -d --build frontend proxy

bash:
	$(COMPOSE) exec backend bash

migrate:
	$(COMPOSE) run --rm migrate

migrate-generate:
	@test -n "$(msg)" || { echo 'Usage: make migrate-generate msg="your migration message"'; exit 1; }
	$(COMPOSE) run --rm backend alembic revision --autogenerate -m "$(msg)"

up-prod:
	$(COMPOSE_PROD) up -d --build

down-prod:
	$(COMPOSE_PROD) down

build-prod:
	$(COMPOSE_PROD) build

rebuild-prod:
	$(COMPOSE_PROD) up -d --build --force-recreate

logs-prod:
	$(COMPOSE_PROD) logs -f

bash-prod:
	$(COMPOSE_PROD) exec backend bash

migrate-prod:
	$(COMPOSE_PROD) run --rm migrate

dev-backend:
	cd backend && uv run uvicorn src.main:app --reload --port 8000

dev-frontend:
	cd frontend && pnpm dev

clean:
	$(COMPOSE) down -v

clean-prod:
	$(COMPOSE_PROD) down -v
