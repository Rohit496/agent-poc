"""MCP server - exposes REST API as async tools for the LangGraph agent."""
import json
import os
import httpx
from fastmcp import FastMCP
from dotenv import load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

load_dotenv()
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

mcp = FastMCP("asset-tools")


async def _get(path: str, params: dict | None = None) -> str:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(f"{BASE_URL}{path}", params=params)
            r.raise_for_status()
            return json.dumps(r.json())
    except httpx.HTTPStatusError as e:
        return json.dumps({"error": f"HTTP {e.response.status_code}: {e.response.text}"})
    except httpx.RequestError as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def get_assets(party_number: str, asset_type: str = "", status: str = "") -> str:
    """Get all assets for a party number with optional filters.

    Args:
        party_number: Party number e.g. P-10042
        asset_type: Optional — 'server' or 'hardware'
        status: Optional — 'active', 'inactive', or 'maintenance'
    """
    params = {k: v for k, v in {"asset_type": asset_type, "status": status}.items() if v}
    return await _get(f"/api/parties/{party_number}/assets", params)


@mcp.tool()
async def get_asset_detail(party_number: str, asset_id: str) -> str:
    """Get details of a single asset.

    Args:
        party_number: Party number e.g. P-10042
        asset_id: Asset ID e.g. A-001
    """
    return await _get(f"/api/parties/{party_number}/assets/{asset_id}")


@mcp.tool()
async def search_assets(party_number: str, q: str = "", asset_type: str = "", status: str = "") -> str:
    """Search assets by keyword with optional filters.

    Args:
        party_number: Party number e.g. P-10042
        q: Free-text search across name, model, location, manufacturer
        asset_type: Optional — 'server' or 'hardware'
        status: Optional — 'active', 'inactive', or 'maintenance'
    """
    params = {"party_number": party_number}
    for k, v in {"q": q, "asset_type": asset_type, "status": status}.items():
        if v:
            params[k] = v
    return await _get("/api/assets/search", params)


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "service": "asset-tools"})


def _run() -> None:
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()

    if transport == "stdio":
        mcp.run()
        return

    if transport not in {"http", "streamable-http", "sse"}:
        raise ValueError(
            "MCP_TRANSPORT must be one of: stdio, http, streamable-http, sse"
        )

    default_path = "/sse" if transport == "sse" else "/mcp"
    mcp.run(
        transport=transport,
        host=os.getenv("MCP_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_PORT", os.getenv("PORT", "8001"))),
        path=os.getenv("MCP_PATH", default_path),
    )


if __name__ == "__main__":
    _run()
