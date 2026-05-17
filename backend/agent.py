"""LangGraph ReAct agent — explicit StateGraph with agent + tools nodes."""

import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_mcp_adapters.client import MultiServerMCPClient
from config import MCP_CONFIG  # load_dotenv() called here, sets OPENAI_API_KEY in env
from prompts import SYSTEM_PROMPT


async def run_query(query: str) -> dict:
    client = MultiServerMCPClient(MCP_CONFIG)
    tools = await client.get_tools()

    llm = ChatOpenAI(model="gpt-4o")
    llm_with_tools = llm.bind_tools(tools)

    # ── Graph nodes ────────────────────────────────────────────────────────────

    async def agent_node(state: MessagesState):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(tools)

    # ── Build graph ────────────────────────────────────────────────────────────
    #
    #   START → agent → (tool calls?) → tools → agent → ... → END
    #
    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)  # → "tools" or END
    graph.add_edge("tools", "agent")

    app = graph.compile()

    # ── Run ────────────────────────────────────────────────────────────────────

    result = await app.ainvoke({"messages": [("user", query)]})
    final = result["messages"][-1].content

    try:
        return json.loads(final)
    except json.JSONDecodeError:
        return {
            "party_number": "",
            "summary": final,
            "assets": [],
            "metadata": {"total": 0, "filters_applied": {}},
        }
