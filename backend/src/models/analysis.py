import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.user import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    title: Mapped[str | None] = mapped_column(String(500))
    insights: Mapped[dict | None] = mapped_column(JSONB)
    chart_specs: Mapped[dict | None] = mapped_column(JSONB)
    llm_tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    files: Mapped[list["AnalysisFile"]] = relationship(back_populates="analysis")


class AnalysisFile(Base):
    __tablename__ = "analysis_files"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("analyses.id"), primary_key=True
    )
    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("uploaded_files.id"), primary_key=True
    )

    analysis: Mapped[Analysis] = relationship(back_populates="files")
