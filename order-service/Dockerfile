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


EXPOSE 5000
CMD ["python", "app.py"]
