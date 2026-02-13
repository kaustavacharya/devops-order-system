
# DevOps Order System

This project is a microservices-based order management system with DevOps best practices. Each service is isolated, uses its own virtual environment, and is containerized with Docker.

## Project Structure

- `order-service/`: Handles order processing ([Order Service README](order-service/README.md))
- `inventory-service/`: Manages inventory ([Inventory Service README](inventory-service/README.md))
- `gateway/`: NGINX gateway configuration
- `monitoring/`: Prometheus monitoring setup
- `docker-compose.yml`: Multi-service orchestration

## Setup

Each service uses [uv](https://github.com/astral-sh/uv) for dependency and environment management.

### Per-Service Setup

1. Navigate to the service directory:
   - `cd order-service` or `cd inventory-service`
2. Create a virtual environment:
   - `uv venv`
# DevOps CI/CD Hands-on Exercise — DevOps Order System

Purpose
- This repository is a hands‑on CI/CD exercise platform (not a microservices demo). It contains a small application and CI workflow designed to teach continuous integration, testing, build, and image-publish flows.

What this exercise covers
- Running unit tests with `pytest`.
- Running service tests locally with `docker compose`.
- Requiring tests to pass in CI before building/pushing images (`.github/workflows/ci-cd.yml`).
- Securing secrets (local `.env`, GitHub Secrets for CI).
- Observability basics: metrics, logs, and service checks.

Repository layout (short)
- `order-service/` — Flask-based order API + tests
- `inventory-service/` — inventory logic + tests (atomic reserve Lua script)
- `.github/workflows/ci-cd.yml` — CI pipeline (tests → build → push)
- `docker-compose.yml` — local stack for hands‑on testing
- `.env` (local only) — runtime variables (DO NOT commit)

Quickstart (local)
1. Create a local `.env` (example values; do not commit):
```dotenv
POSTGRES_USER=admin
POSTGRES_PASSWORD=change_me
POSTGRES_DB=orders
BROKER_HOST=rabbitmq
BROKER_PORT=5672
REDIS_HOST=inventory-db
DEFAULT_STOCK=100
```

2. Start the stack:
```powershell
docker compose up -d
```

3. Run unit tests per-service:
```powershell
cd order-service; pytest -q
cd ../inventory-service; pytest -q
```

4. Quick end‑to‑end check (create an order):
```powershell
Invoke-RestMethod -Uri http://localhost:8080/orders -Method Post `
  -Body (@{item='widget'; quantity=1} | ConvertTo-Json) -ContentType 'application/json'
```

5. Inspect runtime data:
```powershell
docker compose exec -e PGPASSWORD=%POSTGRES_PASSWORD% order-db \
  psql -U %POSTGRES_USER% -d %POSTGRES_DB% -c "SELECT * FROM orders;"

docker compose exec inventory-db redis-cli GET widget
```

CI / GitHub Actions
- Workflow: `.github/workflows/ci-cd.yml`.
- Flow: push → run tests for each service → build & push images (requires registry secrets).
- Set `DOCKER_HUB_USERNAME` and `DOCKER_HUB_ACCESS_TOKEN` in GitHub Secrets to enable image publish.

Notes & best practices
- Never commit secrets. Use `.env` locally (gitignored) and GitHub Secrets for CI.
- Redis is intentionally internal to the Compose network (no host `ports:` mapping) for secure defaults.
- If you change Postgres credentials, recreate volumes: `docker compose down -v` then `docker compose up -d`.
- Keep tests that need external services as integration tests; mock external dependencies when appropriate to keep CI fast.

Next steps / exercise ideas
- Add more unit tests and ensure CI fails when tests fail.
- Harden CI: add caching, linters, and dependency pinning.
- Add a deployment job (Kubernetes/ECS) to the workflow for full CI/CD.

Support
- Tail logs: `docker compose logs -f order-service inventory-service order-db rabbitmq`
- Check running containers: `docker compose ps`

This README is the canonical guide for this repository; per-service README files were removed to keep the exercise focused.
