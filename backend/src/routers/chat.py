import json
import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps import get_db, get_current_user
from src.models.user import User
from src.models.analysis import Analysis
from src.models.message import ChatMessage
from src.schemas.chat import ChatMessageCreate, ChatMessageResponse
from src.services.llm_client import stream_chat_response

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/{analysis_id}/message")
async def send_message(
    analysis_id: uuid.UUID,
    data: ChatMessageCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Analysis).where(Analysis.id == analysis_id, Analysis.user_id == user.id)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    user_msg = ChatMessage(
        analysis_id=analysis_id,
        user_id=user.id,
        role="user",
        content=data.content,
    )
    db.add(user_msg)
    await db.commit()

    history_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.analysis_id == analysis_id)
        .order_by(ChatMessage.created_at)
    )
    history = history_result.scalars().all()

    async def event_stream():
        full_response = []
        async for chunk in stream_chat_response(analysis, history, data.content):
            full_response.append(chunk)
            yield f"data: {json.dumps({'content': chunk})}\n\n"

        content = "".join(full_response)
        assistant_msg = ChatMessage(
            analysis_id=analysis_id,
            user_id=user.id,
            role="assistant",
            content=content,
        )
        db.add(assistant_msg)
        await db.commit()
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.get("/{analysis_id}/history", response_model=list[ChatMessageResponse])
async def get_history(
    analysis_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.analysis_id == analysis_id, ChatMessage.user_id == user.id)
        .order_by(ChatMessage.created_at)
    )
    return result.scalars().all()
