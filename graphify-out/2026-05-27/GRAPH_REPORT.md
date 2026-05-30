# Graph Report - .  (2026-05-27)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 983 nodes · 2336 edges · 55 communities (45 shown, 10 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 259 edges (avg confidence: 0.8)
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
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]

## God Nodes (most connected - your core abstractions)
1. `constructor()` - 78 edges
2. `wf` - 59 edges
3. `ChatBotComponent` - 42 edges
4. `get()` - 38 edges
5. `nd()` - 33 edges
6. `m` - 32 edges
7. `K()` - 28 edges
8. `cw()` - 28 edges
9. `l` - 26 edges
10. `qo()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `ChatBotComponent` --references--> `AssetStateService`  [INFERRED]
  chatbot-widget/src/app/chatbot.component.ts → frontend/src/app/services/asset-state.service.ts
- `AssetTableComponent` --references--> `Asset`  [EXTRACTED]
  frontend/src/app/components/asset-table/asset-table.component.ts → frontend/src/app/models/asset.model.ts
- `query_agent()` --calls--> `run_query()`  [INFERRED]
  backend/main.py → backend/agent.py
- `AppComponent` --references--> `AssetStateService`  [EXTRACTED]
  frontend/src/app/app.component.ts → frontend/src/app/services/asset-state.service.ts
- `AgentResponseComponent` --references--> `QueryResponse`  [EXTRACTED]
  frontend/src/app/components/agent-response/agent-response.component.ts → frontend/src/app/models/asset.model.ts

## Communities (55 total, 10 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (78): ac(), ad(), Ah(), am(), as(), bb(), be(), bo() (+70 more)

### Community 1 - "Community 1"
Cohesion: 0.02
Nodes (73): Ae, Ak, ba, Bl, bn, c1, Ce, Dg (+65 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (33): clear(), cu(), du(), E1, ee(), eh(), es(), fu (+25 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (13): ChatBotComponent, ChatMessage, ToneNote, FormatMessagePipe, ChatMessage, ToneNote, candidates, __dirname (+5 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (41): architect, prefix, projectType, root, schematics, sourceRoot, build, extract-i18n (+33 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (21): AgentResponseComponent, AppComponent, compiled, fixture, appConfig, routes, AssetTableComponent, SortDir (+13 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (29): str, LangGraph ReAct agent — explicit StateGraph with agent + tools nodes., run_query(), _hosted_mcp_connection(), str, Swap this file with real DB/API calls when moving to production., _filter(), get_asset_detail() (+21 more)

### Community 7 - "Community 7"
Cohesion: 0.06
Nodes (31): dependencies, @angular/animations, @angular/common, @angular/compiler, @angular/core, @angular/forms, @angular/platform-browser, @angular/router (+23 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (12): _, A, aI(), b(), cn(), Hk(), l, Ln (+4 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (25): angularCompilerOptions, enableI18nLegacyMessageIdFormat, strictInjectionParameters, strictInputAccessModifiers, strictTemplates, compileOnSave, compilerOptions, declaration (+17 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (18): _adjustIndex(), Ch(), detach(), Gg(), insert(), insertImpl(), Jc(), Jl() (+10 more)

### Community 11 - "Community 11"
Cohesion: 0.10
Nodes (3): eu(), Ka(), wf

### Community 12 - "Community 12"
Cohesion: 0.08
Nodes (23): dependencies, @angular/animations, @angular/common, @angular/compiler, @angular/core, @angular/elements, @angular/forms, @angular/platform-browser (+15 more)

### Community 13 - "Community 13"
Cohesion: 0.18
Nodes (18): bp(), cp(), ep(), gs(), He(), hl(), Ip(), ll() (+10 more)

### Community 14 - "Community 14"
Cohesion: 0.11
Nodes (22): architect, build, serve, builder, configurations, defaultConfiguration, options, development (+14 more)

### Community 15 - "Community 15"
Cohesion: 0.12
Nodes (22): au(), Bf(), ds(), Hi(), kg(), ki(), lo(), mp() (+14 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (16): BI(), cM, d, dl(), dM, el(), fM, gm() (+8 more)

### Community 17 - "Community 17"
Cohesion: 0.16
Nodes (11): af, ar, fc(), ho(), hy, Ib, Pg(), un() (+3 more)

### Community 18 - "Community 18"
Cohesion: 0.28
Nodes (9): constructor(), ed(), get(), lv, ns(), qh, ur(), xF() (+1 more)

### Community 20 - "Community 20"
Cohesion: 0.22
Nodes (6): dw(), fw(), gf(), mf(), vw(), yf()

### Community 21 - "Community 21"
Cohesion: 0.19
Nodes (14): ao(), bD(), bu, fv(), gD(), Lh(), md(), Nn() (+6 more)

### Community 22 - "Community 22"
Cohesion: 0.14
Nodes (15): em(), fs(), go, gT(), h, Ht, ME(), mh() (+7 more)

### Community 25 - "Community 25"
Cohesion: 0.24
Nodes (9): createComponent(), hs(), js(), K(), qv(), Tk, xr(), yg (+1 more)

### Community 26 - "Community 26"
Cohesion: 0.33
Nodes (7): at, av(), move(), nd(), QN, uv(), zn()

### Community 27 - "Community 27"
Cohesion: 0.18
Nodes (13): cl(), dc(), dp(), fg(), ig(), im(), Kl(), lc() (+5 more)

### Community 28 - "Community 28"
Cohesion: 0.17
Nodes (13): bM, bx(), element(), et(), hb(), Ix(), jm(), Kn (+5 more)

### Community 30 - "Community 30"
Cohesion: 0.17
Nodes (8): ct(), Ea(), indexOf(), je(), kt(), Nw(), Qe(), Vm()

### Community 31 - "Community 31"
Cohesion: 0.27
Nodes (12): gn(), ir(), iv(), la(), Mn, Qc(), Ru(), ua() (+4 more)

### Community 32 - "Community 32"
Cohesion: 0.17
Nodes (4): co(), fo(), w, z

### Community 33 - "Community 33"
Cohesion: 0.33
Nodes (4): a1, Eg(), mr(), wM

### Community 34 - "Community 34"
Cohesion: 0.27
Nodes (6): bh(), $e(), ku(), ne, wg(), Zg()

### Community 35 - "Community 35"
Cohesion: 0.29
Nodes (4): createEmbeddedView(), nc(), Tc, Zu()

### Community 37 - "Community 37"
Cohesion: 0.29
Nodes (6): cli, analytics, newProjectRoot, projects, $schema, version

### Community 38 - "Community 38"
Cohesion: 0.29
Nodes (6): compilerOptions, outDir, types, extends, files, include

### Community 39 - "Community 39"
Cohesion: 0.29
Nodes (6): API_BASE_URL, MCP_HOST, MCP_PATH, MCP_PORT, MCP_TRANSPORT, start-hf-space.sh script

### Community 41 - "Community 41"
Cohesion: 0.50
Nodes (5): ec(), jg(), Tr(), vg, Vs()

### Community 42 - "Community 42"
Cohesion: 0.40
Nodes (4): enableAllProjectMcpServers, enabledMcpjsonServers, permissions, allow

### Community 43 - "Community 43"
Cohesion: 0.40
Nodes (4): /api, changeOrigin, secure, target

### Community 44 - "Community 44"
Cohesion: 0.40
Nodes (5): De, dh(), i, ic(), Xg()

### Community 45 - "Community 45"
Cohesion: 0.67
Nodes (3): schematics, style, @schematics/angular:component

### Community 53 - "Community 53"
Cohesion: 0.40
Nodes (4): fI, gw(), ou(), Wh()

## Knowledge Gaps
- **215 isolated node(s):** `$schema`, `version`, `newProjectRoot`, `projectType`, `style` (+210 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ChatBotComponent` connect `Community 3` to `Community 5`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `wf` connect `Community 11` to `Community 1`, `Community 8`, `Community 15`, `Community 48`, `Community 18`, `Community 19`, `Community 20`, `Community 23`, `Community 24`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `architect` connect `Community 14` to `Community 1`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `constructor()` (e.g. with `n()` and `J()`) actually correct?**
  _`constructor()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `nd()` (e.g. with `fe()` and `K()`) actually correct?**
  _`nd()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `version`, `newProjectRoot` to the rest of the system?**
  _222 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.055642633228840124 - nodes in this community are weakly interconnected._