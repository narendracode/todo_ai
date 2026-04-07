from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from todoai_ai.chat import stream_answer as ai_stream_answer

from ..config import settings

router = APIRouter()


@router.get("/stream-answer")
async def stream_answer(query: str = Query(..., min_length=1)):
    return StreamingResponse(
        ai_stream_answer(settings.anthropic_api_key, query),
        media_type="text/plain",
    )
