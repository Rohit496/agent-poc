"""MCP server - exposes REST API as async tools for the LangGraph agent."""
import json
import os
from typing import AsyncIterator, Any
import httpx
from fastmcp import FastMCP
from fastmcp.server.lifespan import lifespan
from dotenv import load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
BASE_URL = API_BASE_URL if API_BASE_URL.startswith(("http://", "https://")) else f"http://{API_BASE_URL}"

_client: httpx.AsyncClient | None = None


@lifespan
async def httpx_lifespan(server: FastMCP) -> AsyncIterator[dict[str, Any]]:
    global _client
    _client = httpx.AsyncClient(timeout=10.0)
    try:
        yield {"client": _client}
    finally:
        await _client.aclose()
        _client = None


mcp = FastMCP("asset-tools", lifespan=httpx_lifespan)

from bumblebee_scanner import run_scan, result_to_dict, packages_to_list


async def _get(path: str, params: dict | None = None) -> str:
    client = _client or httpx.AsyncClient(timeout=10.0)
    try:
        r = await client.get(f"{BASE_URL}{path}", params=params)
        r.raise_for_status()
        return json.dumps(r.json())
    except httpx.HTTPStatusError as e:
        return json.dumps({"error": f"HTTP {e.response.status_code}: {e.response.text}"})
    except httpx.RequestError as e:
        return json.dumps({"error": str(e)})
    finally:
        if not _client:
            await client.aclose()


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


@mcp.tool()
async def scan_packages(
    profile: str = "baseline",
    root: str = "",
    ecosystem: str = "",
    max_duration: str = "60s",
) -> str:
    """Scan the local machine for installed packages and return a summary.

    Runs the Bumblebee package inventory scanner which detects packages
    across npm, PyPI, Go, RubyGems, Composer, MCP servers, editor extensions,
    and browser extensions.

    Args:
        profile: Scan profile — 'baseline' (user-level packages), 'project' (specific directory), or 'deep' (full home walk).
        root: Root path to scan. Required for 'project' profile (e.g. '/Users/rohit/myproject').
        ecosystem: Filter by ecosystem (e.g. 'npm', 'pypi', 'go'). Empty = all ecosystems.
        max_duration: Max scan duration (e.g. '30s', '2m'). Default '60s'.
    """
    result = await run_scan(
        profile=profile,
        root=root or None,
        ecosystem=ecosystem or None,
        max_duration=max_duration,
    )
    if result.error:
        return json.dumps({"error": result.error})
    return json.dumps(result_to_dict(result))


@mcp.tool()
async def scan_findings(
    profile: str = "baseline",
    root: str = "",
    ecosystem: str = "",
    max_duration: str = "60s",
) -> str:
    """Scan for known-malicious or compromised packages using the exposure catalog.

    Runs a Bumblebee scan with bundled threat intelligence catalogs and returns
    any findings (packages matching known supply-chain compromises).
    Zero findings is normal — it means no known-bad packages were detected.

    Args:
        profile: Scan profile — 'baseline', 'project', or 'deep'.
        root: Root path to scan. Required for 'project' profile.
        ecosystem: Filter by ecosystem. Empty = all.
        max_duration: Max scan duration. Default '60s'.
    """
    result = await run_scan(
        profile=profile,
        root=root or None,
        ecosystem=ecosystem or None,
        findings_only=True,
        max_duration=max_duration,
    )
    if result.error:
        return json.dumps({"error": result.error})
    return json.dumps(result_to_dict(result))


@mcp.tool()
async def list_packages(
    profile: str = "baseline",
    root: str = "",
    ecosystem: str = "",
    limit: str = "50",
    max_duration: str = "60s",
) -> str:
    """List installed packages found by the Bumblebee scanner.

    Returns individual package records with name, version, ecosystem, and metadata.
    Use the ecosystem filter to narrow results.

    Args:
        profile: Scan profile — 'baseline', 'project', or 'deep'.
        root: Root path to scan. Required for 'project' profile.
        ecosystem: Filter results to a single ecosystem (e.g. 'npm', 'pypi').
        limit: Max number of packages to return (default 50, max 500).
        max_duration: Max scan duration. Default '60s'.
    """
    try:
        lim = min(int(limit), 500)
    except ValueError:
        lim = 50

    result = await run_scan(
        profile=profile,
        root=root or None,
        ecosystem=ecosystem or None,
        max_duration=max_duration,
    )
    if result.error:
        return json.dumps({"error": result.error})

    packages = packages_to_list(result, limit=lim, ecosystem=ecosystem)
    return json.dumps({
        "total_found": len(result.packages),
        "returned": len(packages),
        "packages": packages,
    })


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
