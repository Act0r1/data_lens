import uuid
from datetime import datetime

from pydantic import BaseModel


class FileResponse(BaseModel):
    id: uuid.UUID
    original_name: str
    mime_type: str
    size_bytes: int
    status: str
    row_count: int | None = None
    column_count: int | None = None
    domain: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class FilePreview(BaseModel):
    columns: list[str]
    rows: list[dict]
    total_rows: int
