FROM python:3.11-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install uv and create venv
RUN pip install uv
RUN uv venv .venv

# Activate venv and install dependencies
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN uv pip install .

# Copy app code
COPY . .

ENV REDIS_HOST=inventory-db
ENV REDIS_PORT=6379
ENV BROKER_HOST=rabbitmq
ENV BROKER_PORT=5672

EXPOSE 5001
CMD ["python", "app.py"]
