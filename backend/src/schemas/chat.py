import uuid
from datetime import datetime

from pydantic import BaseModel


class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageResponse(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    chart_spec: dict | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
