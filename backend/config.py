import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # loads OPENAI_API_KEY into env — create_agent reads it automatically

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

_DIR = str(Path(__file__).parent)

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
