from langchain_core.messages import HumanMessage, AnyMessage, AIMessage
from todoai_ai.schemas import AgentChatRequest

def format_chat_history(agent_chat_request: AgentChatRequest) -> AnyMessage:
    formatted_messages = []
    for ch in agent_chat_request.chat_history:
        formatted_messages.append(HumanMessage(content=ch.query, name="User"))
        formatted_messages.append(AIMessage(content=ch.response, name="Model"))
    formatted_messages.append(
        HumanMessage(content=agent_chat_request.query, name="User")
    )
    return formatted_messages

 