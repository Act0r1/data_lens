import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps import get_db, get_current_user
from src.models.user import User
from src.models.file import UploadedFile
from src.schemas.file import FileResponse, FilePreview
from src.services.s3_storage import upload_to_s3
from src.workers.process_file import process_file_task

logger = logging.getLogger(__name__)

router = APIRouter()

ALLOWED_MIMES = {
    "text/csv",
    "text/tab-separated-values",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
    "application/octet-stream",
}


@router.post("/upload", response_model=FileResponse, status_code=201)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if file.content_type not in ALLOWED_MIMES:
        ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename else ""
        if ext not in ("csv", "tsv", "xlsx", "xls"):
            raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    s3_key = f"uploads/{user.id}/{uuid.uuid4()}/{file.filename}"
    await upload_to_s3(s3_key, content, file.content_type or "application/octet-stream")

    db_file = UploadedFile(
        user_id=user.id,
        original_name=file.filename or "unknown",
        s3_key=s3_key,
        mime_type=file.content_type or "application/octet-stream",
        size_bytes=len(content),
        status="uploaded",
    )
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)

    background_tasks.add_task(process_file_task, str(db_file.id))
    logger.info("File uploaded: %s", db_file.id)
    return db_file


@router.get("/", response_model=list[FileResponse])
async def list_files(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UploadedFile)
        .where(UploadedFile.user_id == user.id)
        .order_by(UploadedFile.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{file_id}/preview", response_model=FilePreview)
async def get_preview(
    file_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UploadedFile).where(UploadedFile.id == file_id, UploadedFile.user_id == user.id)
    )
    f = result.scalar_one_or_none()
    if not f:
        raise HTTPException(status_code=404, detail="File not found")
    if f.status != "ready":
        raise HTTPException(status_code=400, detail="File is not processed yet")
    return FilePreview(
        columns=list(f.preview.get("columns", [])),
        rows=f.preview.get("rows", [])[:50],
        total_rows=f.row_count or 0,
    )


@router.delete("/{file_id}", status_code=204)
async def delete_file(
    file_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UploadedFile).where(UploadedFile.id == file_id, UploadedFile.user_id == user.id)
    )
    f = result.scalar_one_or_none()
    if not f:
        raise HTTPException(status_code=404, detail="File not found")
    await db.delete(f)
    await db.commit()
