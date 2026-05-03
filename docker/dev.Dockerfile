FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  python3-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock langgraph.json ./

COPY src ./src

RUN uv sync --frozen --dev

ENV PYTHONPATH=/app/src:/app/src/genpb
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "python", "src/app/main.py"]
