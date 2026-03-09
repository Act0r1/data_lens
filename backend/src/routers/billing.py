from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps import get_db, get_current_user
from src.models.user import User, Plan
from src.schemas.subscription import PlanResponse, UsageResponse
from src.services.usage_tracker import get_current_usage

router = APIRouter()


@router.get("/plans", response_model=list[PlanResponse])
async def list_plans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Plan).order_by(Plan.price_monthly))
    return result.scalars().all()


@router.get("/usage", response_model=UsageResponse)
async def get_usage(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_current_usage(user.id, db)


@router.post("/subscribe")
async def subscribe(
    plan_slug: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Plan).where(Plan.slug == plan_slug))
    plan = result.scalar_one_or_none()
    if not plan:
        return {"error": "Plan not found"}

    if plan.price_monthly == 0:
        user.plan_id = plan.id
        await db.commit()
        return {"status": "switched", "plan": plan.slug}

    return {"payment_url": f"https://yookassa.ru/checkout?plan={plan.slug}", "status": "redirect"}
