"""Bumblebee MCP tools — exposes package scanning to the LangGraph agent.

These tools are registered on the existing FastMCP server so the AI agent
can trigger scans and query package inventory via natural language.
"""

import json
from bumblebee_scanner import run_scan, result_to_dict, packages_to_list


async def scan_packages(
    profile: str = "baseline",
    root: str = "",
    ecosystem: str = "",
    max_duration: str = "60s",
) -> str:
    """Scan the local machine for installed packages and return a summary.

    This runs the Bumblebee package inventory scanner which detects packages
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

    data = result_to_dict(result)
    return json.dumps(data)


async def scan_findings(
    profile: str = "baseline",
    root: str = "",
    ecosystem: str = "",
    max_duration: str = "60s",
) -> str:
    """Scan for known-malicious or compromised packages using the exposure catalog.

    Runs a Bumblebee scan with the bundled threat intelligence catalogs and
    returns any findings (packages matching known supply-chain compromises).
    Zero findings is normal and means no known-bad packages were detected.

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

    data = result_to_dict(result)
    return json.dumps(data)


async def list_packages(
    profile: str = "baseline",
    root: str = "",
    ecosystem: str = "",
    limit: str = "50",
    max_duration: str = "60s",
) -> str:
    """List installed packages found by the scanner.

    Returns a list of individual package records with name, version, ecosystem,
    and metadata. Use the ecosystem filter to narrow results.

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


def register_scan_tools(mcp_server):
    """Register all scan tools on a FastMCP server instance."""
    mcp_server.tool()(scan_packages)
    mcp_server.tool()(scan_findings)
    mcp_server.tool()(list_packages)
