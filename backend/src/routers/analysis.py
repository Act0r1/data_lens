import uuid

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps import get_db, get_current_user
from src.models.user import User
from src.models.analysis import Analysis, AnalysisFile
from src.models.file import UploadedFile
from src.schemas.analysis import AnalysisCreate, AnalysisResponse
from src.workers.run_analysis import run_analysis_task

router = APIRouter()


@router.post("/run", response_model=AnalysisResponse, status_code=201)
async def create_analysis(
    data: AnalysisCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(UploadedFile).where(
            UploadedFile.id.in_(data.file_ids),
            UploadedFile.user_id == user.id,
            UploadedFile.status == "ready",
        )
    )
    files = result.scalars().all()
    if len(files) != len(data.file_ids):
        raise HTTPException(status_code=400, detail="Some files are not ready or not found")

    analysis = Analysis(user_id=user.id, status="pending")
    db.add(analysis)
    await db.flush()

    for f in files:
        db.add(AnalysisFile(analysis_id=analysis.id, file_id=f.id))

    await db.commit()
    await db.refresh(analysis)

    background_tasks.add_task(run_analysis_task, str(analysis.id))
    return analysis


@router.get("/", response_model=list[AnalysisResponse])
async def list_analyses(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Analysis)
        .where(Analysis.user_id == user.id)
        .order_by(Analysis.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Analysis).where(Analysis.id == analysis_id, Analysis.user_id == user.id)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
