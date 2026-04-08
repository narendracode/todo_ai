from collections.abc import AsyncIterator

from todoai_ai.schemas import AgentChatRequest
from todoai_ai.utils import format_chat_history
from todoai_ai.tools.current_date_tools import CurrentTimeTool
from todoai_ai.tools.join_waitinglist_tool import JoinWaitingListTool
from todoai_ai.tools.save_booking_tool import SaveBookingTool
from todoai_ai.tools.table_availability_tool import GetTableAvailabilityTool
import json

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage



def get_llm(api_key: str) -> ChatAnthropic:
    return ChatAnthropic(
        model="claude-sonnet-4-20250514",
        api_key=api_key,
    )


async def stream_answer(api_key: str, query: str, user_id: str) -> AsyncIterator[str]:
    llm = get_llm(api_key)
    print(f"LLM is processing query for user {user_id}...")
    async for chunk in llm.astream([HumanMessage(content=query)]):
        if chunk.content:
            yield chunk.content

memory = InMemorySaver()

async def chat(agent_chat_request: AgentChatRequest, api_key: str):
    print(f"agent chat request : {agent_chat_request}")
    memory_config = {"configurable": {"thread_id": agent_chat_request.user_id}}

    model = get_llm(api_key)

    tools = [CurrentTimeTool(), JoinWaitingListTool(), SaveBookingTool(), GetTableAvailabilityTool()]
    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt="""You are an AI agent to helps users book tables at restaurants and provide information about restraurants.
    Never assume any value, try to use the tools otherwise always ask for clarity if the request is ambiguous.""",
        checkpointer=memory
    )

    async def generate():
        async for chunk in agent.astream(
            input={"messages": [HumanMessage(content=agent_chat_request.query)]},
            config=memory_config,
            stream_mode="updates",
        ):
            try:
                if "agent" in chunk:
                    message = chunk["agent"]["messages"][0]
                    # Extract text content (handles both str and list-of-blocks from Anthropic)
                    text_content = ""
                    if isinstance(message.content, str):
                        text_content = message.content
                    elif isinstance(message.content, list):
                        text_content = "".join(
                            block.get("text", "") for block in message.content if isinstance(block, dict) and block.get("type") == "text"
                        )

                    if message.tool_calls:
                        for tool_call in message.tool_calls:
                            yield (
                                json.dumps(
                                    {
                                        "type": "tool_name",
                                        "content": tool_call["name"],
                                    }
                                )
                                + "\n"
                            )
                            args = tool_call.get("args", {})
                            if not args:
                                yield (
                                    json.dumps(
                                        {
                                            "type": "tool_args",
                                            "content": "No arguments",
                                        }
                                    )
                                    + "\n"
                                )
                            else:
                                yield (
                                    json.dumps(
                                        {
                                            "type": "tool_args",
                                            "content": json.dumps(args) if isinstance(args, dict) else args,
                                        }
                                    )
                                    + "\n"
                                )
                    elif text_content:
                        yield (
                            json.dumps(
                                {
                                    "type": "answer",
                                    "content": text_content,
                                }
                            )
                            + "\n"
                        )
                if "tools" in chunk:
                    for tool_msg in chunk["tools"]["messages"]:
                        if tool_msg.content:
                            yield (
                                json.dumps(
                                    {
                                        "type": "tool_content",
                                        "content": tool_msg.content,
                                    }
                                )
                                + "\n"
                            )
            except Exception as e:
                print(f"Error at /agent/chat: {e}")
                yield (
                    json.dumps({"type": "answer", "content": "We are facing an issue, please try after sometimes."})
                    + "\n"
                )

    return generate()

