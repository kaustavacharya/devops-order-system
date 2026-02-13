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

ENV DB_HOST=order-db
ENV DB_NAME=orders
ENV DB_USER=admin
ENV DB_PASSWORD=password123
ENV DB_PORT=5432
ENV BROKER_HOST=rabbitmq
ENV BROKER_PORT=5672

EXPOSE 5000
CMD ["python", "app.py"]
