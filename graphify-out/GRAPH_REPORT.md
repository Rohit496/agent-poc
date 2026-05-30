# Graph Report - Agentrix  (2026-05-27)

## Corpus Check
- 48 files · ~13,812 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1272 nodes · 2988 edges · 85 communities (66 shown, 19 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 281 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4b1c21b6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]

## God Nodes (most connected - your core abstractions)
1. `constructor()` - 78 edges
2. `wf` - 76 edges
3. `ChatBotComponent` - 43 edges
4. `nd()` - 42 edges
5. `get()` - 38 edges
6. `m` - 33 edges
7. `cw()` - 32 edges
8. `l` - 31 edges
9. `qo()` - 31 edges
10. `K()` - 30 edges

## Surprising Connections (you probably didn't know these)
- `ChatBotComponent` --references--> `AssetStateService`  [INFERRED]
  chatbot-widget/src/app/chatbot.component.ts → frontend/src/app/services/asset-state.service.ts
- `query_agent()` --calls--> `run_query()`  [INFERRED]
  backend/main.py → backend/agent.py
- `AppComponent` --references--> `AssetStateService`  [EXTRACTED]
  frontend/src/app/app.component.ts → frontend/src/app/services/asset-state.service.ts
- `AssetTableComponent` --references--> `Asset`  [EXTRACTED]
  frontend/src/app/components/asset-table/asset-table.component.ts → frontend/src/app/models/asset.model.ts
- `AgentResponseComponent` --references--> `QueryResponse`  [EXTRACTED]
  frontend/src/app/components/agent-response/agent-response.component.ts → frontend/src/app/models/asset.model.ts

## Communities (85 total, 19 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (40): ad(), Ah(), as(), bb(), cs(), f, fd(), Ft() (+32 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (75): Ae, ba, Bl, bx(), c1, Ce, De, Dg (+67 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (51): architect, prefix, projectType, root, schematics, sourceRoot, build, extract-i18n (+43 more)

### Community 5 - "Community 5"
Cohesion: 0.24
Nodes (9): AgentResponseComponent, environment, LoadingSpinnerComponent, QueryRequest, QueryResponse, QueryInputComponent, QueryPageComponent, QueryState (+1 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (20): MCPSessionManager, str, LangGraph ReAct agent — explicit StateGraph with agent + tools nodes., Manages the lifespan of persistent MCP server connections and tools., run_query(), _hosted_mcp_connection(), str, Swap this file with real DB/API calls when moving to production. (+12 more)

### Community 7 - "Community 7"
Cohesion: 0.06
Nodes (33): dependencies, @angular/animations, @angular/common, @angular/compiler, @angular/core, @angular/forms, @angular/platform-browser, @angular/platform-browser-dynamic (+25 more)

### Community 8 - "Community 8"
Cohesion: 0.20
Nodes (5): _, A, cn(), J(), so()

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (25): angularCompilerOptions, enableI18nLegacyMessageIdFormat, strictInjectionParameters, strictInputAccessModifiers, strictTemplates, compileOnSave, compilerOptions, declaration (+17 more)

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (19): _adjustIndex(), at, av(), Ch(), detach(), ed(), insert(), insertImpl() (+11 more)

### Community 12 - "Community 12"
Cohesion: 0.08
Nodes (23): dependencies, @angular/animations, @angular/common, @angular/compiler, @angular/core, @angular/elements, @angular/forms, @angular/platform-browser (+15 more)

### Community 13 - "Community 13"
Cohesion: 0.07
Nodes (28): Bf(), bp(), co(), cp(), ep(), fo(), gs(), He() (+20 more)

### Community 14 - "Community 14"
Cohesion: 0.06
Nodes (41): architect, prefix, projectType, root, schematics, sourceRoot, build, serve (+33 more)

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (21): ds(), em(), fs(), go, hs(), kg(), lc(), lu (+13 more)

### Community 16 - "Community 16"
Cohesion: 0.21
Nodes (12): au(), BI(), d, el(), hc(), hM, lo(), mo (+4 more)

### Community 17 - "Community 17"
Cohesion: 0.24
Nodes (10): ar, ca(), createComponent(), get(), K(), ns(), op(), un() (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.35
Nodes (3): lv, Wh(), yg

### Community 21 - "Community 21"
Cohesion: 0.29
Nodes (6): bD(), fv(), gD(), ml(), Pt(), yd()

### Community 22 - "Community 22"
Cohesion: 0.18
Nodes (10): Gg(), h, Jc(), Jl(), mh(), o(), OE, Qp() (+2 more)

### Community 23 - "Community 23"
Cohesion: 0.23
Nodes (5): fh, or(), ou(), vw(), xF()

### Community 25 - "Community 25"
Cohesion: 0.13
Nodes (8): Ak, bn, constructor(), hu(), Kf(), pu, qh, Tk

### Community 26 - "Community 26"
Cohesion: 0.16
Nodes (19): Any, _get(), get_asset_detail(), get_assets(), health(), httpx_lifespan(), str, MCP server - exposes REST API as async tools for the LangGraph agent. (+11 more)

### Community 27 - "Community 27"
Cohesion: 0.11
Nodes (28): bh(), bo(), C, cl(), dc(), dp(), fg(), ic() (+20 more)

### Community 28 - "Community 28"
Cohesion: 0.15
Nodes (20): be(), bM, Bs(), cc(), ct(), Fn(), hb(), ih() (+12 more)

### Community 30 - "Community 30"
Cohesion: 0.20
Nodes (6): Ea(), indexOf(), kt(), Nw(), Qe(), Vm()

### Community 31 - "Community 31"
Cohesion: 0.21
Nodes (11): gn(), ir(), iv(), la(), Mn, Qc(), Ru(), ua() (+3 more)

### Community 32 - "Community 32"
Cohesion: 0.17
Nodes (6): du(), E1, ee(), emit(), sh, subscribe()

### Community 33 - "Community 33"
Cohesion: 0.33
Nodes (4): a1, ks(), vg, Vn()

### Community 35 - "Community 35"
Cohesion: 0.09
Nodes (13): ac(), createEmbeddedView(), createEmbeddedViewImpl(), length(), ms(), nc(), Qu(), Tc (+5 more)

### Community 37 - "Community 37"
Cohesion: 0.18
Nodes (6): eh(), fu, ji(), U(), WN, ye()

### Community 38 - "Community 38"
Cohesion: 0.29
Nodes (6): compilerOptions, outDir, types, extends, files, include

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (6): API_BASE_URL, MCP_HOST, MCP_PATH, MCP_PORT, MCP_TRANSPORT, start-hf-space.sh script

### Community 41 - "Community 41"
Cohesion: 0.50
Nodes (4): ec(), Pg(), Tr(), Vs()

### Community 42 - "Community 42"
Cohesion: 0.40
Nodes (4): enableAllProjectMcpServers, enabledMcpjsonServers, permissions, allow

### Community 43 - "Community 43"
Cohesion: 0.40
Nodes (4): /api, changeOrigin, secure, target

### Community 44 - "Community 44"
Cohesion: 0.21
Nodes (7): AppComponent, compiled, fixture, appConfig, routes, DashboardComponent, AssetStateService

### Community 45 - "Community 45"
Cohesion: 0.15
Nodes (7): ChatMessage, ToneNote, FormatMessagePipe, ChatMessage, ToneNote, FormatMessagePipe, ChatElement

### Community 48 - "Community 48"
Cohesion: 0.14
Nodes (5): af, hy, Ib, injector(), V0

### Community 53 - "Community 53"
Cohesion: 0.13
Nodes (14): Agentrix, Architecture, code:block1 (┌───────────────────────────────────────────────────────────), code:block23 (User types a question in the chat widget), code:block24 (Show me all active servers for P-10042), code:bash (python --version && uv --version && node --version && npm --), code:bash (# Widget), code:block38 (backend/.env) (+6 more)

### Community 55 - "Community 55"
Cohesion: 0.17
Nodes (15): am(), cd(), element(), et(), gb(), gm(), Mb(), oc() (+7 more)

### Community 56 - "Community 56"
Cohesion: 0.19
Nodes (6): ao(), b(), Hi(), Ln, n(), S()

### Community 57 - "Community 57"
Cohesion: 0.15
Nodes (4): aI(), Hk(), I0, l

### Community 58 - "Community 58"
Cohesion: 0.17
Nodes (12): Cloud deployment, code:bash (cd backend), code:bash (docker compose up --build mcp), code:text (http://localhost:8001/mcp), code:bash (cd backend), code:text (API_BASE_URL=http://host.docker.internal:8000), code:bash (API_BASE_URL=http://host.docker.internal:9000 docker compose), code:bash (API_BASE_URL=http://backend:8000 docker compose --profile ba) (+4 more)

### Community 59 - "Community 59"
Cohesion: 0.27
Nodes (4): clear(), cu(), mt(), remove()

### Community 60 - "Community 60"
Cohesion: 0.18
Nodes (9): Backend (`backend/`), code:block1 (Agentrix/), code:bash (# Terminal 1 — Backend (port 8000)), code:block3 (OPENAI_API_KEY=sk-...), Environment Variables (`backend/.env`), Frontend (`frontend/`), Project Structure, Running the Project (+1 more)

### Community 61 - "Community 61"
Cohesion: 0.33
Nodes (7): dw(), fe(), fw(), gf(), mf(), Um, yf()

### Community 62 - "Community 62"
Cohesion: 0.22
Nodes (9): Chatbot sends a message but nothing happens, Chatbot widget not visible, code:html (<agentrix-chat></agentrix-chat>       <!-- same-origin with ), code:bash (curl http://localhost:8000/health    # check if it's already), code:bash (curl -X POST http://localhost:8000/api/query \), code:bash (cd chatbot-widget && npm run build), `Error: Not Found` in the chat, Port 8000 already in use (+1 more)

### Community 63 - "Community 63"
Cohesion: 0.36
Nodes (4): AssetTableComponent, SortDir, SortKey, Asset

### Community 64 - "Community 64"
Cohesion: 0.25
Nodes (8): 1. Environment variables, 2. Install dependencies, 3. Build the chatbot widget, code:bash (cp backend/.env.example backend/.env   # or create it manual), code:env (OPENAI_API_KEY=sk-...), code:bash (# Python (backend)), code:bash (cd chatbot-widget), Setup

### Community 65 - "Community 65"
Cohesion: 0.25
Nodes (8): AI Query Endpoint, API Reference, Asset REST API, code:http (GET /health), code:http (GET  /api/parties/{party_number}/assets), code:http (POST /api/query), code:json ({), Health

### Community 66 - "Community 66"
Cohesion: 0.50
Nodes (3): Eg(), mr(), wM

### Community 67 - "Community 67"
Cohesion: 0.25
Nodes (7): candidates, __dirname, distRoot, filePath, outDir, outFile, parts

### Community 68 - "Community 68"
Cohesion: 0.25
Nodes (7): AgentrixUi, Build, Code scaffolding, Development server, Further help, Running end-to-end tests, Running unit tests

### Community 69 - "Community 69"
Cohesion: 0.29
Nodes (7): Attribute, Chatbot Web Component, code:html (<!-- 1. Load the bundle -->), code:bash (cd chatbot-widget), Drop into any page, Event, Rebuild after changes

### Community 70 - "Community 70"
Cohesion: 0.52
Nodes (4): fc(), ho(), Wi(), yl()

### Community 71 - "Community 71"
Cohesion: 0.47
Nodes (5): bu, Lh(), Nn(), ur(), Uu()

### Community 72 - "Community 72"
Cohesion: 0.33
Nodes (3): cM, dM, fM

### Community 73 - "Community 73"
Cohesion: 0.40
Nodes (6): es(), gu(), Iu(), ju(), rh(), Ui()

### Community 75 - "Community 75"
Cohesion: 0.40
Nodes (5): Backend (`backend/`), Chatbot Widget (`chatbot-widget/`), code:block2 (Agentrix/), Frontend (`frontend/`), Project Structure

### Community 77 - "Community 77"
Cohesion: 0.50
Nodes (4): code:text (SDK: Docker), code:text (https://<user>-<space-name>.hf.space/health), code:env (MCP_SERVER_URL=https://<user>-<space-name>.hf.space), Hugging Face Spaces deployment

### Community 78 - "Community 78"
Cohesion: 0.50
Nodes (4): bt(), md(), x, xn()

### Community 79 - "Community 79"
Cohesion: 0.67
Nodes (3): code:bash (cd backend), code:bash (docker compose up --build mcp), MCP Server

### Community 80 - "Community 80"
Cohesion: 0.67
Nodes (3): code:bash (# Terminal 1 — Backend (port 8000)), code:bash (# Terminal 2 — Frontend (port 4200)), Running

## Knowledge Gaps
- **262 isolated node(s):** `$schema`, `version`, `newProjectRoot`, `projectType`, `style` (+257 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ChatBotComponent` connect `Community 3` to `Community 5`, `Community 67`, `Community 44`, `Community 45`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Why does `wf` connect `Community 11` to `Community 32`, `Community 1`, `Community 37`, `Community 13`, `Community 17`, `Community 18`, `Community 19`, `Community 20`, `Community 83`, `Community 23`, `Community 24`, `Community 25`, `Community 57`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `AgentApiService` connect `Community 5` to `Community 3`, `Community 45`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `constructor()` (e.g. with `o()` and `n()`) actually correct?**
  _`constructor()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `nd()` (e.g. with `K()` and `fe()`) actually correct?**
  _`nd()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `version`, `newProjectRoot` to the rest of the system?**
  _269 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.11829268292682926 - nodes in this community are weakly interconnected._