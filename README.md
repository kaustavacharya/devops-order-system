# DevOps Order System

## Per-Service Virtual Environments with uv

Each service in this project is fully isolated and manages its own dependencies and virtual environment using [uv](https://github.com/astral-sh/uv).

### Setup for Each Service

1. **Navigate to the service directory:**
   - `cd order-service` or `cd inventory-service`
2. **Create a virtual environment:**
   - `uv venv`
3. **Install dependencies:**
   - `uv pip install .` (if using pyproject.toml)
   - or `uv pip install -r requirements.txt`
4. **Lock dependencies:**
   - `uv lock`

### Docker
Each service's Dockerfile uses only its own dependency files and does not share venvs or dependencies with other services.

### Why?
- No dependency conflicts between services
- Reproducible builds and deployments
- Easy local development and testing

---

Repeat the above steps for every new service you add.
