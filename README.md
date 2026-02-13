
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
3. Install dependencies:
   - `uv pip install .` (if using pyproject.toml)
4. Lock dependencies:
   - `uv lock`

### Docker
Each service's Dockerfile uses only its own dependency files and does not share venvs or dependencies with other services.

### Why?
- No dependency conflicts between services
- Reproducible builds and deployments
- Easy local development and testing

---

Repeat the above steps for every new service you add.

## Running with Docker Compose

To start all services:

```bash
docker-compose up --build
```

## Monitoring

Prometheus is configured in the `monitoring/` folder. See `monitoring/prometheus.yml` for details.

## Gateway

NGINX configuration is in the `gateway/` folder. See `gateway/nginx.conf`.

---

For more details, see the README files in each service folder.
