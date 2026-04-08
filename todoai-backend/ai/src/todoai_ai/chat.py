import json
from collections.abc import AsyncIterator
from pathlib import Path
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, StateGraph
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode

from todoai_ai.schemas import AgentChatRequest
from todoai_ai.tools.create_task_tool import CreateTaskTool
from todoai_ai.tools.current_date_tools import CurrentTimeTool
from todoai_ai.tools.delete_task_tool import DeleteTaskTool
from todoai_ai.tools.list_tasks_tool import ListTasksTool
from todoai_ai.tools.update_task_tool import UpdateTaskTool

_SYSTEM_PROMPT = """You are TodoAI, an intelligent task management assistant integrated into a task scheduling application.

You help users manage their tasks by:
- Listing and searching tasks (by status, priority, or general queries)
- Creating new tasks with appropriate priorities and deadlines
- Updating task details, status, priority, and scheduling
- Deleting tasks the user no longer needs

Guidelines:
- Use current_time to understand today's date when the user mentions relative dates ("tomorrow", "next week").
- When creating or updating tasks, use ISO 8601 for datetimes (e.g. 2026-04-15T14:00:00) and YYYY-MM-DD for due dates.
- Always confirm destructive operations (delete) with the user before calling the tool.
- After any write operation, report what was done clearly and concisely.
- If a task operation fails, explain why and suggest a correction.
- Never assume task IDs — use list_tasks to retrieve them when needed."""

_memory = InMemorySaver()


def _get_llm(api_key: str) -> ChatAnthropic:
    return ChatAnthropic(model="claude-sonnet-4-20250514", api_key=api_key)


async def stream_answer(api_key: str, query: str, user_id: str) -> AsyncIterator[str]:
    """Simple single-turn streaming answer (no tool use)."""
    llm = _get_llm(api_key)
    async for chunk in llm.astream([HumanMessage(content=query)]):
        if chunk.content:
            yield chunk.content


async def chat(
    agent_chat_request: AgentChatRequest,
    api_key: str,
    access_token: str,
    api_base_url: str,
) -> AsyncIterator[str]:
    """Multi-turn agentic chat with real task management tools."""
    tool_kwargs = {"api_base_url": api_base_url, "access_token": access_token}
    tools = [
        CurrentTimeTool(),
        ListTasksTool(**tool_kwargs),
        CreateTaskTool(**tool_kwargs),
        UpdateTaskTool(**tool_kwargs),
        DeleteTaskTool(**tool_kwargs),
    ]

    model = _get_llm(api_key).bind_tools(tools)

    def should_continue(state: MessagesState):
        return "tools" if state["messages"][-1].tool_calls else END

    async def call_model(state: MessagesState):
        messages = [SystemMessage(content=_SYSTEM_PROMPT)] + state["messages"]
        return {"messages": [await model.ainvoke(messages)]}

    graph = (
        StateGraph(MessagesState)
        .add_node("assistant", call_model)
        .add_node("tools", ToolNode(tools))
        .set_entry_point("assistant")
        .add_conditional_edges("assistant", should_continue, {"tools": "tools", END: END})
        .add_edge("tools", "assistant")
        .compile(checkpointer=_memory)
    )

    # graph_png = graph.get_graph().draw_mermaid_png()
    # output_path = Path(__file__).with_name("task_graph.png")
    # output_path.write_bytes(graph_png)
    # print(f"Graph image saved to: {output_path}")

    config = {"configurable": {"thread_id": agent_chat_request.user_id}}

    async def generate() -> AsyncIterator[str]:
        async for chunk in graph.astream(
            input={"messages": [HumanMessage(content=agent_chat_request.query)]},
            config=config,
            stream_mode="updates",
        ):
            try:
                if "assistant" in chunk:
                    message = chunk["assistant"]["messages"][0]

                    # Extract text (Anthropic returns str or list-of-blocks)
                    if isinstance(message.content, str):
                        text = message.content
                    elif isinstance(message.content, list):
                        text = "".join(
                            b.get("text", "")
                            for b in message.content
                            if isinstance(b, dict) and b.get("type") == "text"
                        )
                    else:
                        text = ""

                    for tool_call in message.tool_calls or []:
                        yield json.dumps({"type": "tool_name", "content": tool_call["name"]}) + "\n"
                        args = tool_call.get("args") or {}
                        yield json.dumps({"type": "tool_args", "content": json.dumps(args)}) + "\n"

                    if text and not message.tool_calls:
                        yield json.dumps({"type": "answer", "content": text}) + "\n"

                elif "tools" in chunk:
                    for msg in chunk["tools"]["messages"]:
                        if msg.content:
                            yield json.dumps({"type": "tool_content", "content": msg.content}) + "\n"

            except Exception as e:
                yield json.dumps({"type": "answer", "content": f"Something went wrong: {e}"}) + "\n"

    return generate()
