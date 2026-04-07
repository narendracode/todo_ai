from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

from todoai_ai.chat import stream_answer as ai_stream_answer
from todoai_common.models import User

from ..config import settings
from ..dependencies import get_current_user

router = APIRouter()


@router.get("/stream-answer")
async def stream_answer(
    query: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_user),
):
    print(f"User {current_user.id} is asking: {query}")
    return StreamingResponse(
        ai_stream_answer(settings.anthropic_api_key, query, current_user.id),
        media_type="text/plain",
    )
