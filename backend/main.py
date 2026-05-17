"""Single async FastAPI server — asset REST API + AI agent endpoint."""
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fixtures import ASSETS
from agent import run_query

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Agentrix", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _filter(assets: list, asset_type: str | None, status: str | None) -> list:
    if asset_type:
        assets = [a for a in assets if a["asset_type"] == asset_type]
    if status:
        assets = [a for a in assets if a["status"] == status]
    return assets


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok"}


# ── Asset REST API ────────────────────────────────────────────────────────────

@app.get("/api/parties/{party_number}/assets")
async def get_assets(
    party_number: str,
    asset_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    if party_number not in ASSETS:
        raise HTTPException(404, "Party not found")
    assets = _filter(ASSETS[party_number], asset_type, status)
    return {"party_number": party_number, "total": len(assets), "assets": assets}


@app.get("/api/parties/{party_number}/assets/{asset_id}")
async def get_asset_detail(party_number: str, asset_id: str):
    if party_number not in ASSETS:
        raise HTTPException(404, "Party not found")
    for a in ASSETS[party_number]:
        if a["id"] == asset_id:
            return a
    raise HTTPException(404, "Asset not found")


@app.get("/api/assets/search")
async def search_assets(
    party_number: str = Query(...),
    q: str | None = Query(default=None),
    asset_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    if party_number not in ASSETS:
        raise HTTPException(404, "Party not found")
    assets = _filter(ASSETS[party_number], asset_type, status)
    if q:
        ql = q.lower()
        assets = [
            a for a in assets
            if any(ql in str(a.get(f, "")).lower()
                   for f in ("name", "model", "location", "manufacturer", "serial_number"))
        ]
    return {"party_number": party_number, "query": q, "total": len(assets), "assets": assets}


# ── AI Agent endpoint ─────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)


@app.post("/api/query")
async def query_agent(req: QueryRequest):
    try:
        return await run_query(req.query)
    except Exception as e:
        raise HTTPException(500, f"Agent error: {e}")
