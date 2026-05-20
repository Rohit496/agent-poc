#!/usr/bin/env sh
set -eu

uv run uvicorn main:app --host 127.0.0.1 --port 8000 &

export API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"
export MCP_TRANSPORT="${MCP_TRANSPORT:-http}"
export MCP_HOST="${MCP_HOST:-0.0.0.0}"
export MCP_PORT="${PORT:-7860}"
export MCP_PATH="${MCP_PATH:-/mcp}"

exec uv run python mcp_server.py
