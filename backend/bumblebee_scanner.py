"""Bumblebee scanner wrapper — calls the Go binary and parses NDJSON output.

This module wraps the bumblebee CLI (https://github.com/perplexityai/bumblebee)
to run package inventory scans and return structured results. The binary must
be pre-built at BUMBLEBEE_BIN (default: ../bumblebee/bumblebee).
"""

import asyncio
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ── Binary location ──────────────────────────────────────────────────────────

_BACKEND_DIR = Path(__file__).parent
BUMBLEBEE_BIN = os.getenv(
    "BUMBLEBEE_BIN",
    str(_BACKEND_DIR.parent / "bumblebee" / "bumblebee"),
)
THREAT_INTEL_DIR = os.getenv(
    "BUMBLEBEE_THREAT_INTEL",
    str(_BACKEND_DIR.parent / "bumblebee" / "threat_intel"),
)


# ── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class PackageRecord:
    record_type: str = ""
    record_id: str = ""
    ecosystem: str = ""
    package_name: str = ""
    normalized_name: str = ""
    version: str = ""
    project_path: str = ""
    root_kind: str = ""
    package_manager: str = ""
    source_type: str = ""
    source_file: str = ""
    confidence: str = ""
    direct_dependency: Optional[bool] = None
    has_lifecycle_scripts: bool = False
    lifecycle_scripts: list = field(default_factory=list)
    install_scope: str = ""
    server_name: str = ""
    requested_spec: str = ""


@dataclass
class Finding:
    record_type: str = ""
    record_id: str = ""
    ecosystem: str = ""
    package_name: str = ""
    normalized_name: str = ""
    version: str = ""
    catalog_id: str = ""
    catalog_name: str = ""
    severity: str = ""
    matched_version: str = ""
    source_file: str = ""
    project_path: str = ""


@dataclass
class ScanSummary:
    record_type: str = ""
    record_id: str = ""
    run_id: str = ""
    scan_time: str = ""
    end_time: str = ""
    profile: str = ""
    status: str = ""
    roots: list = field(default_factory=list)
    counts: dict = field(default_factory=dict)
    package_records_emitted: int = 0
    findings_emitted: int = 0
    duplicates: int = 0
    diagnostics_count: int = 0
    files_considered: int = 0
    timed_out: bool = False
    duration_ms: int = 0
    endpoint: dict = field(default_factory=dict)


@dataclass
class ScanResult:
    """Full parsed scan result."""
    packages: list[PackageRecord] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    summary: Optional[ScanSummary] = None
    error: str = ""


# ── Parsing ──────────────────────────────────────────────────────────────────

def _parse_package(raw: dict) -> PackageRecord:
    return PackageRecord(
        record_type=raw.get("record_type", ""),
        record_id=raw.get("record_id", ""),
        ecosystem=raw.get("ecosystem", ""),
        package_name=raw.get("package_name", ""),
        normalized_name=raw.get("normalized_name", ""),
        version=raw.get("version", ""),
        project_path=raw.get("project_path", ""),
        root_kind=raw.get("root_kind", ""),
        package_manager=raw.get("package_manager", ""),
        source_type=raw.get("source_type", ""),
        source_file=raw.get("source_file", ""),
        confidence=raw.get("confidence", ""),
        direct_dependency=raw.get("direct_dependency"),
        has_lifecycle_scripts=raw.get("has_lifecycle_scripts", False),
        lifecycle_scripts=raw.get("lifecycle_scripts") or [],
        install_scope=raw.get("install_scope", ""),
        server_name=raw.get("server_name", ""),
        requested_spec=raw.get("requested_spec", ""),
    )


def _parse_finding(raw: dict) -> Finding:
    return Finding(
        record_type=raw.get("record_type", ""),
        record_id=raw.get("record_id", ""),
        ecosystem=raw.get("ecosystem", ""),
        package_name=raw.get("package_name", ""),
        normalized_name=raw.get("normalized_name", ""),
        version=raw.get("version", ""),
        catalog_id=raw.get("catalog_id", ""),
        catalog_name=raw.get("catalog_name", ""),
        severity=raw.get("severity", ""),
        matched_version=raw.get("matched_version", ""),
        source_file=raw.get("source_file", ""),
        project_path=raw.get("project_path", ""),
    )


def _parse_summary(raw: dict) -> ScanSummary:
    return ScanSummary(
        record_type=raw.get("record_type", ""),
        record_id=raw.get("record_id", ""),
        run_id=raw.get("run_id", ""),
        scan_time=raw.get("scan_time", ""),
        end_time=raw.get("end_time", ""),
        profile=raw.get("profile", ""),
        status=raw.get("status", ""),
        roots=raw.get("roots") or [],
        counts=raw.get("counts") or {},
        package_records_emitted=raw.get("package_records_emitted", 0),
        findings_emitted=raw.get("findings_emitted", 0),
        duplicates=raw.get("duplicates", 0),
        diagnostics_count=raw.get("diagnostics_count", 0),
        files_considered=raw.get("files_considered", 0),
        timed_out=raw.get("timed_out", False),
        duration_ms=raw.get("duration_ms", 0),
        endpoint=raw.get("endpoint") or {},
    )


def parse_ndjson(output: str) -> ScanResult:
    """Parse NDJSON output from bumblebee into a ScanResult."""
    result = ScanResult()
    for line in output.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        rt = record.get("record_type", "")
        if rt == "package":
            result.packages.append(_parse_package(record))
        elif rt == "finding":
            result.findings.append(_parse_finding(record))
        elif rt == "scan_summary":
            result.summary = _parse_summary(record)
    return result


# ── Runner ───────────────────────────────────────────────────────────────────

async def run_scan(
    profile: str = "baseline",
    root: Optional[str] = None,
    ecosystem: Optional[str] = None,
    exposure_catalog: Optional[str] = None,
    findings_only: bool = False,
    max_duration: Optional[str] = None,
) -> ScanResult:
    """Run bumblebee scan and return parsed results.

    Args:
        profile: Scan profile — baseline, project, or deep.
        root: Optional root path to scan (overrides profile defaults).
        ecosystem: Optional ecosystem filter (e.g. "npm", "pypi,go").
        exposure_catalog: Path to exposure catalog file or directory.
                          Defaults to the bundled threat_intel/ directory.
        findings_only: If True, only emit findings (suppress package records).
        max_duration: Max wall-clock duration (e.g. "30s", "2m").
    """
    if not Path(BUMBLEBEE_BIN).exists():
        return ScanResult(error=f"Bumblebee binary not found at {BUMBLEBEE_BIN}")

    cmd = [BUMBLEBEE_BIN, "scan", "--profile", profile]

    if root:
        cmd.extend(["--root", root])

    if ecosystem:
        cmd.extend(["--ecosystem", ecosystem])

    catalog = exposure_catalog or THREAT_INTEL_DIR
    if Path(catalog).exists():
        cmd.extend(["--exposure-catalog", catalog])

    if findings_only:
        cmd.append("--findings-only")

    if max_duration:
        cmd.extend(["--max-duration", max_duration])

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            err_msg = stderr.decode("utf-8", errors="replace").strip()
            return ScanResult(error=f"bumblebee exited {proc.returncode}: {err_msg}")

        return parse_ndjson(stdout.decode("utf-8", errors="replace"))

    except FileNotFoundError:
        return ScanResult(error=f"Bumblebee binary not found at {BUMBLEBEE_BIN}")
    except Exception as e:
        return ScanResult(error=str(e))


# ── Convenience helpers ──────────────────────────────────────────────────────

def result_to_dict(result: ScanResult) -> dict:
    """Convert ScanResult to a JSON-serializable dict."""
    ecosystem_counts = {}
    for pkg in result.packages:
        ecosystem_counts[pkg.ecosystem] = ecosystem_counts.get(pkg.ecosystem, 0) + 1

    return {
        "packages_total": len(result.packages),
        "findings_total": len(result.findings),
        "ecosystem_counts": ecosystem_counts,
        "findings": [
            {
                "ecosystem": f.ecosystem,
                "package_name": f.package_name,
                "version": f.version,
                "catalog_id": f.catalog_id,
                "catalog_name": f.catalog_name,
                "severity": f.severity,
                "matched_version": f.matched_version,
                "source_file": f.source_file,
                "project_path": f.project_path,
            }
            for f in result.findings
        ],
        "summary": {
            "run_id": result.summary.run_id,
            "profile": result.summary.profile,
            "status": result.summary.status,
            "scan_time": result.summary.scan_time,
            "end_time": result.summary.end_time,
            "duration_ms": result.summary.duration_ms,
            "package_records_emitted": result.summary.package_records_emitted,
            "findings_emitted": result.summary.findings_emitted,
            "files_considered": result.summary.files_considered,
            "roots": result.summary.roots,
            "endpoint": result.summary.endpoint,
        } if result.summary else None,
        "error": result.error,
    }


def packages_to_list(result: ScanResult, limit: int = 100, ecosystem: str = "") -> list[dict]:
    """Return packages as a list of dicts, optionally filtered by ecosystem."""
    pkgs = result.packages
    if ecosystem:
        pkgs = [p for p in pkgs if p.ecosystem == ecosystem]
    return [
        {
            "ecosystem": p.ecosystem,
            "package_name": p.package_name,
            "version": p.version,
            "package_manager": p.package_manager,
            "source_type": p.source_type,
            "confidence": p.confidence,
            "direct_dependency": p.direct_dependency,
            "install_scope": p.install_scope,
            "project_path": p.project_path,
            "has_lifecycle_scripts": p.has_lifecycle_scripts,
        }
        for p in pkgs[:limit]
    ]
