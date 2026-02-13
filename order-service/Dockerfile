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
RUN uv pip install pytest prometheus_client

# Copy app code
COPY . .


EXPOSE 5000

# Test stage (default command runs tests if TEST is set)
ARG TEST=false
CMD if [ "$TEST" = "true" ]; then pytest test_app.py; else python app.py; fi
