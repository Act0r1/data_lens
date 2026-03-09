import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps import get_db, get_current_user
from src.models.user import User
from src.models.analysis import Analysis
from src.services.chart_generator import generate_chart_spec

router = APIRouter()


@router.get("/{analysis_id}/specs")
async def get_chart_specs(
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
    return analysis.chart_specs or []


@router.post("/{analysis_id}/generate")
async def generate_chart(
    analysis_id: uuid.UUID,
    request: dict,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Analysis).where(Analysis.id == analysis_id, Analysis.user_id == user.id)
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    spec = await generate_chart_spec(analysis, request.get("prompt", ""))
    return spec
