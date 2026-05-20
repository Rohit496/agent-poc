FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
COPY backend/pyproject.toml backend/pyproject.toml
RUN uv sync --locked --no-dev --package backend --no-install-project

COPY backend backend
COPY scripts/start-hf-space.sh scripts/start-hf-space.sh
RUN chmod +x scripts/start-hf-space.sh
RUN uv sync --locked --no-dev --package backend

WORKDIR /app/backend

ENV API_BASE_URL=http://127.0.0.1:8000
ENV MCP_TRANSPORT=http
ENV MCP_HOST=0.0.0.0
ENV MCP_PATH=/mcp

EXPOSE 7860

CMD ["/app/scripts/start-hf-space.sh"]
