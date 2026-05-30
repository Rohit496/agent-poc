"""Bumblebee scan REST API routes — mounted on the existing FastAPI app.

Endpoints:
    POST /api/scan              — trigger a new scan
    GET  /api/scan/ecosystems   — list supported ecosystems
    GET  /api/scan/profiles     — list scan profiles
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional
from bumblebee_scanner import run_scan, result_to_dict, packages_to_list

router = APIRouter(prefix="/api/scan", tags=["bumblebee"])


# ── Request / Response models ────────────────────────────────────────────────

class ScanRequest(BaseModel):
    profile: str = Field(default="baseline", description="Scan profile: baseline, project, or deep")
    root: Optional[str] = Field(default=None, description="Root path to scan (overrides profile defaults)")
    ecosystem: Optional[str] = Field(default=None, description="Filter by ecosystem (e.g. 'npm', 'pypi,go')")
    findings_only: bool = Field(default=False, description="Only return findings, suppress package records")
    max_duration: Optional[str] = Field(default="60s", description="Max wall-clock duration (e.g. '30s', '2m')")


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("")
async def trigger_scan(req: ScanRequest):
    """Run a bumblebee package inventory scan and return results."""
    result = await run_scan(
        profile=req.profile,
        root=req.root,
        ecosystem=req.ecosystem,
        findings_only=req.findings_only,
        max_duration=req.max_duration,
    )
    if result.error:
        return {"status": "error", "error": result.error}

    data = result_to_dict(result)
    data["status"] = "ok"
    return data


@router.post("/packages")
async def scan_packages(
    req: ScanRequest,
    limit: int = Query(default=100, ge=1, le=10000),
    filter_ecosystem: Optional[str] = Query(default=None, alias="ecosystem_filter"),
):
    """Run a scan and return the package list (paginated)."""
    result = await run_scan(
        profile=req.profile,
        root=req.root,
        ecosystem=req.ecosystem,
        max_duration=req.max_duration,
    )
    if result.error:
        return {"status": "error", "error": result.error}

    packages = packages_to_list(result, limit=limit, ecosystem=filter_ecosystem or "")
    return {
        "status": "ok",
        "total": len(result.packages),
        "returned": len(packages),
        "packages": packages,
    }


@router.post("/findings")
async def scan_findings(req: ScanRequest):
    """Run a scan with exposure catalog and return only findings."""
    req.findings_only = True
    result = await run_scan(
        profile=req.profile,
        root=req.root,
        ecosystem=req.ecosystem,
        findings_only=True,
        max_duration=req.max_duration,
    )
    if result.error:
        return {"status": "error", "error": result.error}

    data = result_to_dict(result)
    data["status"] = "ok"
    return data


@router.get("/ecosystems")
async def list_ecosystems():
    """List supported ecosystems."""
    return {
        "ecosystems": [
            {"id": "npm", "label": "npm / Node.js", "file_types": ["package-lock.json", "node_modules/*/package.json"]},
            {"id": "pypi", "label": "PyPI / Python", "file_types": ["*.dist-info/METADATA", "*.egg-info/PKG-INFO"]},
            {"id": "go", "label": "Go Modules", "file_types": ["go.sum", "go.mod"]},
            {"id": "rubygems", "label": "RubyGems", "file_types": ["Gemfile.lock", "*.gemspec"]},
            {"id": "packagist", "label": "Composer / PHP", "file_types": ["composer.lock", "installed.json"]},
            {"id": "mcp", "label": "MCP Servers", "file_types": ["mcp.json", "claude_desktop_config.json", "cline_mcp_settings.json"]},
            {"id": "editor-extension", "label": "Editor Extensions", "file_types": ["VS Code, Cursor, Windsurf extensions"]},
            {"id": "browser-extension", "label": "Browser Extensions", "file_types": ["Chrome/Firefox manifest.json, extensions.json"]},
        ]
    }


@router.get("/profiles")
async def list_profiles():
    """List scan profiles."""
    return {
        "profiles": [
            {
                "id": "baseline",
                "label": "Baseline",
                "description": "User-level package roots, editor/browser extensions, MCP configs. No project trees.",
            },
            {
                "id": "project",
                "label": "Project",
                "description": "Scans a specific project directory (use --root). Includes lockfiles and node_modules.",
            },
            {
                "id": "deep",
                "label": "Deep",
                "description": "Full home-directory walk. Finds everything but takes longer.",
            },
        ]
    }
