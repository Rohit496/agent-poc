# Agentrix

An AI-powered asset intelligence platform. Ask questions in plain English — the LangGraph agent finds your assets and updates the dashboard in real time.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Browser                                  │
│                                                                 │
│  ┌──────────────────────┐     ┌──────────────────────────────┐  │
│  │   Angular App        │     │  <agentrix-chat> Web         │  │
│  │   (frontend/)        │     │  Component (chatbot-widget/) │  │
│  │                      │     │                              │  │
│  │  Dashboard ──────────│◄────│── agentrix-response event    │  │
│  │  Asset Table         │     │                              │  │
│  │                      │     │  fetch POST /api/query       │  │
│  └──────────────────────┘     └──────────┬───────────────────┘  │
└─────────────────────────────────────────-│───────────────────────┘
                                           │
                                    ┌──────▼──────────┐
                                    │  FastAPI         │
                                    │  (port 8000)     │
                                    │                  │
                                    │  POST /api/query │
                                    │  GET  /api/...   │
                                    └──────┬──────────┘
                                           │
                                    ┌──────▼──────────┐
                                    │  LangGraph       │
                                    │  ReAct Agent     │
                                    │  (GPT-4o)        │
                                    └──────┬──────────┘
                                           │ stdio
                                    ┌──────▼──────────┐
                                    │  MCP Server      │
                                    │  (asset tools)   │
                                    └─────────────────┘
```

**Key design decision:** the chatbot is a standalone [Web Component](https://developer.mozilla.org/en-US/docs/Web/API/Web_components) (`<agentrix-chat>`) built with Angular Elements. It can be dropped into *any* web application — Angular, React, Vue, or plain HTML — with a single `<script>` tag.

---

## Project Structure

```
Agentrix/
├── backend/              Python — FastAPI + LangGraph agent
├── frontend/             Angular 17 — asset dashboard
├── chatbot-widget/       Angular Elements — portable chat web component
├── pyproject.toml        uv workspace config
└── uv.lock
```

### Backend (`backend/`)

| File | Role |
|---|---|
| `main.py` | FastAPI app — asset REST API + `POST /api/query` |
| `agent.py` | LangGraph ReAct agent — `run_query(query)` |
| `mcp_server.py` | MCP server launched as subprocess by agent (stdio) |
| `fixtures.py` | Demo asset data — **swap this** to connect real data |
| `prompts.py` | GPT-4o system prompt |
| `config.py` | Env vars + MCP subprocess config |

### Frontend (`frontend/`)

| File | Role |
|---|---|
| `src/app/pages/dashboard/` | Asset table page |
| `src/app/components/asset-table/` | Sortable, filterable table with CSV export |
| `src/app/services/asset-state.service.ts` | Signal state shared between chat events and dashboard |
| `src/app/app.component.ts` | Mounts `<agentrix-chat>`, listens for `agentrix-response` event |
| `proxy.conf.json` | Dev proxy: `/api` → `http://localhost:8000` |

### Chatbot Widget (`chatbot-widget/`)

| File | Role |
|---|---|
| `src/main.ts` | Registers `<agentrix-chat>` as a custom element |
| `src/app/chatbot.component.ts` | Chat UI, audio tones, `fetch` API calls |
| `build-bundle.mjs` | Post-build: concatenates output into `agentrix-chat.js` |
| `dist/` → `frontend/src/assets/agentrix-chat.js` | Built bundle consumed by the Angular app |

---

## Prerequisites

| Tool | Version |
|---|---|
| Python | 3.11+ |
| [uv](https://docs.astral.sh/uv/) | latest |
| Node.js | 18+ |
| npm | 9+ |

Verify:

```bash
python --version && uv --version && node --version && npm --version
```

---

## Setup

### 1. Environment variables

```bash
cp backend/.env.example backend/.env   # or create it manually
```

`backend/.env`:

```env
OPENAI_API_KEY=sk-...
API_BASE_URL=http://localhost:8000
```

> `backend/.env` is git-ignored. Never commit real API keys.

### 2. Install dependencies

```bash
# Python (backend)
cd backend && uv sync

# Node (frontend)
cd frontend && npm install

# Node (chatbot widget)
cd chatbot-widget && npm install
```

### 3. Build the chatbot widget

The widget must be built once before running the frontend. After any changes to `chatbot-widget/` source, re-run this:

```bash
cd chatbot-widget
npm run build
# Outputs → frontend/src/assets/agentrix-chat.js
```

---

## Running

Two terminals:

```bash
# Terminal 1 — Backend (port 8000)
cd backend
uv run uvicorn main:app --port 8000 --reload
```

```bash
# Terminal 2 — Frontend (port 4200)
cd frontend
npm start
```

Open **http://localhost:4200** and click the chat button in the bottom-right corner.

---

## How It Works

```
User types a question in the chat widget
  → fetch POST /api/query  (proxied to port 8000)
  → FastAPI receives the query
  → LangGraph agent calls GPT-4o
  → GPT-4o selects an MCP tool (get_assets / search_assets / get_asset_detail)
  → MCP tool calls the backend REST API
  → Agent returns { party_number, summary, assets }
  → Widget fires  agentrix-response  CustomEvent (bubbles to window)
  → Angular app catches the event → updates AssetStateService
  → Dashboard re-renders with matching assets
```

---

## Demo Party Numbers

| Party Number | Data |
|---|---|
| `P-10042` | 3 servers, 1 hardware |
| `P-20017` | 2 servers, 3 hardware |
| `P-30099` | 4 servers, 2 hardware |

Example queries:

```
Show me all active servers for P-10042
List all hardware in DC-East for P-20017
Which servers are in maintenance for P-30099?
Show all assets for P-20017
```

---

## API Reference

### Health

```http
GET /health
→ {"status": "ok"}
```

### Asset REST API

```http
GET  /api/parties/{party_number}/assets
GET  /api/parties/{party_number}/assets?asset_type=server&status=active
GET  /api/parties/{party_number}/assets/{asset_id}
GET  /api/assets/search?party_number=P-10042&q=Dell
```

Interactive docs: **http://localhost:8000/docs**

### AI Query Endpoint

```http
POST /api/query
Content-Type: application/json

{ "query": "Show me all active servers for P-10042" }
```

Response:

```json
{
  "party_number": "P-10042",
  "summary": "Found 2 active servers for P-10042 ...",
  "assets": [ ... ],
  "metadata": { "total": 2, "filters_applied": { "status": "active" } }
}
```

---

## Chatbot Web Component

The widget is a self-contained custom element — no framework required to use it.

### Drop into any page

```html
<!-- 1. Load the bundle -->
<script src="path/to/agentrix-chat.js"></script>

<!-- 2. Place the element -->
<agentrix-chat api-url="https://your-api.example.com"></agentrix-chat>

<!-- 3. Listen for results -->
<script>
  window.addEventListener('agentrix-response', function(e) {
    console.log(e.detail); // { party_number, summary, assets, metadata }
  });
</script>
```

### Attribute

| Attribute | Default | Description |
|---|---|---|
| `api-url` | `""` (same origin) | Base URL of the Agentrix backend |

### Event

| Event | Bubbles | `detail` payload |
|---|---|---|
| `agentrix-response` | yes (to `window`) | Full `QueryResponse` object |

### Rebuild after changes

```bash
cd chatbot-widget
npm run build   # builds + copies bundle to frontend/src/assets/agentrix-chat.js
```

---

## MCP Server

The MCP server exposes three tools to the LangGraph agent over stdio:

| Tool | Description |
|---|---|
| `get_assets` | List all assets for a party, with optional `asset_type` / `status` filters |
| `get_asset_detail` | Fetch a single asset by ID |
| `search_assets` | Full-text search across assets |

Inspect tools interactively:

```bash
cd backend
npx @modelcontextprotocol/inspector@latest uv run python mcp_server.py
# Opens inspector UI — keep backend running on port 8000
```

---

## Connecting Real Data

All demo data lives in `backend/fixtures.py`. To use a real data source:

1. Replace or rewrite `fixtures.py` so `ASSETS` is populated from your database/API.
2. Keep the same dict shape — the REST routes and MCP tools don't change.

---

## Production Build

```bash
# Widget
cd chatbot-widget && npm run build

# Frontend
cd frontend && npm run build
# Output → frontend/dist/agentrix-ui/

# Backend smoke check
cd backend && uv run python -c "from main import app; from agent import run_query; print('OK')"
```

---

## Troubleshooting

### `Error: Not Found` in the chat

The widget's `api-url` attribute is set to a path with `/api` already — this doubles the prefix. Leave the attribute empty when the Angular proxy handles routing:

```html
<agentrix-chat></agentrix-chat>       <!-- same-origin with proxy -->
<agentrix-chat api-url="https://api.example.com"></agentrix-chat>  <!-- explicit host -->
```

### Port 8000 already in use

```bash
curl http://localhost:8000/health    # check if it's already the Agentrix backend
lsof -i :8000                        # find what's using it
```

### Chatbot sends a message but nothing happens

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Show me all active servers for P-10042"}'
```

If this fails, check `backend/.env` — `OPENAI_API_KEY` is likely missing or invalid.

### Chatbot widget not visible

The widget bundle must exist at `frontend/src/assets/agentrix-chat.js`. Run:

```bash
cd chatbot-widget && npm run build
```

Then hard-refresh the browser (`Cmd+Shift+R` / `Ctrl+Shift+R`).

---

## What Not to Commit

```
backend/.env
.venv/
frontend/node_modules/
frontend/dist/
chatbot-widget/node_modules/
chatbot-widget/dist/
**/__pycache__/
```
