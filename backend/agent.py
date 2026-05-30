"""LangGraph ReAct agent — explicit StateGraph with agent + tools nodes."""

import json
import logging
import contextlib
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from openai import APIConnectionError, APIStatusError, RateLimitError
from config import MCP_CONFIG  # load_dotenv() called here, sets OPENAI_API_KEY in env
from prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

_ERROR_RESPONSE = lambda summary: {
    "party_number": "",
    "summary": summary,
    "assets": [],
    "metadata": {"total": 0, "filters_applied": {}},
}


class MCPSessionManager:
    """Manages the lifespan of persistent MCP server connections and tools."""

    def __init__(self, mcp_config: dict):
        self.mcp_config = mcp_config
        self.client = None
        self.tools = []
        self._exit_stack = None

    async def start(self):
        if not self.mcp_config:
            logger.info("No MCP servers configured for session manager.")
            return

        logger.info("Initializing persistent MCP sessions...")
        self._exit_stack = contextlib.AsyncExitStack()
        try:
            self.client = MultiServerMCPClient(self.mcp_config)
            self.tools = []
            for server_name in self.mcp_config:
                logger.info("Opening persistent session for MCP server: %s", server_name)
                session = await self._exit_stack.enter_async_context(
                    self.client.session(server_name)
                )
                logger.info("Loading tools from persistent session for: %s", server_name)
                server_tools = await load_mcp_tools(session, server_name=server_name)
                self.tools.extend(server_tools)
            logger.info("Successfully loaded %d persistent tools from MCP", len(self.tools))
        except Exception as e:
            logger.exception("Failed to initialize persistent MCP session manager")
            await self.stop()
            raise

    async def stop(self):
        if self._exit_stack:
            logger.info("Closing persistent MCP sessions...")
            await self._exit_stack.aclose()
            self._exit_stack = None
        self.client = None
        self.tools = []
        logger.info("Persistent MCP sessions closed.")


mcp_session_manager = MCPSessionManager(MCP_CONFIG)


async def run_query(query: str) -> dict:
    # ── Connect to MCP and load tools ─────────────────────────────────────────
    if mcp_session_manager.tools:
        tools = mcp_session_manager.tools
    else:
        # Fallback to standard dynamic loading for script-based/standalone execution
        try:
            client = MultiServerMCPClient(MCP_CONFIG)
            tools = await client.get_tools()
        except Exception as e:
            logger.exception("Failed to connect to MCP server or load tools")
            return _ERROR_RESPONSE(f"Unable to connect to the asset tools service: {e}")

    if not tools:
        logger.warning("MCP returned no tools — check MCP_CONFIG")
        return _ERROR_RESPONSE("Asset tools are unavailable at the moment. Please try again later.")

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

    try:
        result = await app.ainvoke({"messages": [("user", query)]})
    except RateLimitError:
        logger.warning("OpenAI rate limit exceeded")
        return _ERROR_RESPONSE("The AI service is currently rate-limited. Please try again in a moment.")
    except APIConnectionError as e:
        logger.exception("OpenAI connection error")
        return _ERROR_RESPONSE(f"Could not reach the AI service: {e}")
    except APIStatusError as e:
        logger.exception("OpenAI API error: status=%s", e.status_code)
        return _ERROR_RESPONSE(f"The AI service returned an error (HTTP {e.status_code}). Please try again.")
    except Exception as e:
        logger.exception("Unexpected error running agent graph")
        return _ERROR_RESPONSE(f"An unexpected error occurred: {e}")

    messages = result.get("messages", [])
    if not messages:
        logger.error("Agent graph returned no messages")
        return _ERROR_RESPONSE("The agent did not return a response. Please try again.")

    final = messages[-1].content

    try:
        return json.loads(final)
    except json.JSONDecodeError:
        return {
            "party_number": "",
            "summary": final,
            "assets": [],
            "metadata": {"total": 0, "filters_applied": {}},
        }
