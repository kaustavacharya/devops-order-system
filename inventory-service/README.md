# Inventory Service

This service manages inventory operations for the DevOps Order System.

## Setup

1. Navigate to this directory:
   - `cd inventory-service`
2. Create a virtual environment:
   - `uv venv`
3. Install dependencies:
   - `uv pip install .` (if using pyproject.toml)
4. Lock dependencies:
   - `uv lock`

## Running

- Start the service:
  - `uv pip install .`
  - `python app.py`

## Docker

- Build and run using Docker:
  - `docker build -t inventory-service .`
  - `docker run -p 8000:8000 inventory-service`

## Endpoints

- Main endpoint: `/inventory`

---

See the main project README for more details.