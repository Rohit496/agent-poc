# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

```
Agentrix/
├── backend/        # Python — FastAPI + LangGraph agent (single server)
└── frontend/       # Angular 17 — chat UI + asset dashboard
```

## Running the Project

Two terminals only:

```bash
# Terminal 1 — Backend (port 8000)
cd backend
uv run uvicorn main:app --port 8000 --reload

# Terminal 2 — Frontend (port 4200)
cd frontend
npm start
```

## Backend (`backend/`)

Single UV project. One FastAPI server handles everything on **port 8000**.

| File | Role |
|---|---|
| `main.py` | FastAPI app — asset REST API + `POST /api/query` agent endpoint |
| `agent.py` | LangGraph ReAct agent — `run_query(query)` |
| `mcp_server.py` | MCP server (launched as subprocess by agent via stdio) |
| `fixtures.py` | Dummy asset data — **swap this file** to connect real data |
| `prompts.py` | GPT-4o system prompt |
| `config.py` | Env vars + MCP subprocess config |
| `.env` | `OPENAI_API_KEY`, `API_BASE_URL` |

**API routes:**
- `GET /api/parties/{party_number}/assets` — list assets
- `GET /api/parties/{party_number}/assets/{asset_id}` — single asset
- `GET /api/assets/search?party_number=&q=` — search
- `POST /api/query` — NLP query via LangGraph agent
- `GET /health`

**Swap to real API:** Replace `fixtures.py` with calls to the real data source. All route shapes stay the same.

## Frontend (`frontend/`)

Angular 17 standalone app. Signals for state, no NgRx.

| Key file | Role |
|---|---|
| `src/app/components/chat-bot/` | Floating chat FAB + panel |
| `src/app/pages/dashboard/` | Asset table page (updated by chat agent) |
| `src/app/services/agent-api.service.ts` | HTTP client → `POST /api/query` |
| `src/app/services/asset-state.service.ts` | Shared signal state between chat and dashboard |
| `src/environments/environment.ts` | `agentApiUrl` — update for production |
| `proxy.conf.json` | Dev proxy: `/api` → `http://localhost:8000` |

## Test Party Numbers

| Party | Assets |
|---|---|
| `P-10042` | 3 servers, 1 hardware |
| `P-20017` | 2 servers, 3 hardware |
| `P-30099` | 4 servers, 2 hardware |

## Environment Variables (`backend/.env`)

```
OPENAI_API_KEY=sk-...
API_BASE_URL=http://localhost:8000
```
