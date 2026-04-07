from collections.abc import AsyncIterator

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
