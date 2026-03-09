import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.subscription import UsageRecord
from src.schemas.subscription import UsageResponse


async def get_current_usage(user_id: uuid.UUID, db: AsyncSession) -> UsageResponse:
    today = date.today()
    period_start = today.replace(day=1)

    result = await db.execute(
        select(UsageRecord).where(
            UsageRecord.user_id == user_id,
            UsageRecord.period >= period_start,
        )
    )
    records = result.scalars().all()

    return UsageResponse(
        files_uploaded=sum(r.files_uploaded for r in records),
        analyses_run=sum(r.analyses_run for r in records),
        chat_messages_sent=sum(r.chat_messages_sent for r in records),
        tokens_consumed=sum(r.tokens_consumed for r in records),
    )


async def increment_usage(user_id: uuid.UUID, db: AsyncSession, **kwargs):
    today = date.today()
    result = await db.execute(
        select(UsageRecord).where(
            UsageRecord.user_id == user_id,
            UsageRecord.period == today,
        )
    )
    record = result.scalar_one_or_none()

    if not record:
        record = UsageRecord(user_id=user_id, period=today)
        db.add(record)

    for field, value in kwargs.items():
        current = getattr(record, field, 0)
        setattr(record, field, current + value)

    await db.commit()
