# Order Service

This service handles order processing for the DevOps Order System.

## Setup

1. Navigate to this directory:
   - `cd order-service`
2. Create a virtual environment:
   - `uv venv`
3. Install dependencies:
   - `uv pip install .` (if using pyproject.toml)
4. Lock dependencies:
   - `uv lock`

## Running

- Start the service:
  - `uv pip install .`
  - `python main.py`

## Docker

- Build and run using Docker:
  - `docker build -t order-service .`
  - `docker run -p 8001:8001 order-service`

## Endpoints

- Main endpoint: `/order`

---

See the main project README for more details.