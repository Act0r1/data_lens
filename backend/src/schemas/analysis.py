import uuid
from datetime import datetime

from pydantic import BaseModel


class AnalysisCreate(BaseModel):
    file_ids: list[uuid.UUID]


class InsightItem(BaseModel):
    type: str
    title: str
    description: str
    severity: str = "info"
    data: dict | None = None


class AnalysisResponse(BaseModel):
    id: uuid.UUID
    status: str
    title: str | None = None
    insights: list[InsightItem] | None = None
    chart_specs: list[dict] | None = None
    llm_tokens_used: int = 0
    created_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}
