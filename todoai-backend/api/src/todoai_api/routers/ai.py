from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from todoai_ai.chat import chat as ai_chat, stream_answer as ai_stream_answer
from todoai_ai.schemas import AgentChatRequest
from todoai_common.models import User

from ..config import settings
from ..dependencies import get_access_token, get_current_user

router = APIRouter()


@router.get("/stream-answer")
async def stream_answer(
    query: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
):
    return StreamingResponse(
        ai_stream_answer(settings.anthropic_api_key, query, str(current_user.id)),
        media_type="text/plain",
    )


@router.post("/stream-chat")
async def stream_chat(
    agent_chat_request: AgentChatRequest,
    current_user: User = Depends(get_current_user),
    access_token: str = Depends(get_access_token),
):
    agent_chat_request.user_id = str(current_user.id)
    generator = await ai_chat(
        agent_chat_request,
        settings.anthropic_api_key,
        access_token,
        settings.api_base_url,
    )
    return StreamingResponse(generator, media_type="application/x-ndjson")
