import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # loads OPENAI_API_KEY into env — create_agent reads it automatically

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")  # e.g. http://localhost:8001 (hosted Docker)
MCP_SERVER_TRANSPORT = os.getenv("MCP_SERVER_TRANSPORT", "http").lower()

_DIR = str(Path(__file__).parent)


def _hosted_mcp_connection(base_url: str) -> dict:
    url = base_url.rstrip("/")

    if url.endswith("/sse"):
        return {"transport": "sse", "url": url}
    if url.endswith("/mcp"):
        return {"transport": "http", "url": url}

    if MCP_SERVER_TRANSPORT == "sse":
        return {"transport": "sse", "url": f"{url}/sse"}
    if MCP_SERVER_TRANSPORT in {"http", "streamable-http", "streamable_http"}:
        return {"transport": "http", "url": f"{url}/mcp"}

    raise ValueError("MCP_SERVER_TRANSPORT must be one of: http, streamable-http, sse")


if MCP_SERVER_URL:
    # Hosted MCP server (Docker / remote) over HTTP.
    MCP_CONFIG = {
        "asset-tools": _hosted_mcp_connection(MCP_SERVER_URL)
    }
else:
    if os.getenv("RENDER"):
        MCP_CONFIG = {}
    else:
        # Local development - launch MCP server as subprocess via stdio.
        MCP_CONFIG = {
            "asset-tools": {
                "transport": "stdio",
                "command": "uv",
                "args": ["--directory", _DIR, "run", "python", str(Path(__file__).parent / "mcp_server.py")],
                "cwd": _DIR,
                "env": {"API_BASE_URL": API_BASE_URL},
                "encoding": "utf-8",
                "encoding_error_handler": "strict",
                "session_kwargs": {},
            }
        }
