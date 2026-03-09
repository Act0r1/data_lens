import uuid

from pydantic import BaseModel


class PlanResponse(BaseModel):
    id: uuid.UUID
    slug: str
    name: str
    price_monthly: int
    max_files_per_month: int
    max_file_size_mb: int
    max_chat_messages_per_day: int
    max_analyses_per_month: int

    model_config = {"from_attributes": True}


class UsageResponse(BaseModel):
    files_uploaded: int = 0
    analyses_run: int = 0
    chat_messages_sent: int = 0
    tokens_consumed: int = 0
