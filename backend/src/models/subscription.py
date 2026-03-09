import uuid
from datetime import datetime, date

from sqlalchemy import ForeignKey, Integer, Date, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models.user import Base


class UsageRecord(Base):
    __tablename__ = "usage_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    period: Mapped[date] = mapped_column(Date)
    files_uploaded: Mapped[int] = mapped_column(Integer, default=0)
    analyses_run: Mapped[int] = mapped_column(Integer, default=0)
    chat_messages_sent: Mapped[int] = mapped_column(Integer, default=0)
    tokens_consumed: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
