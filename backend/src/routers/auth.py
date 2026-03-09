from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.deps import get_db, get_current_user
from src.models.user import User, Plan
from src.schemas.user import UserRegister, UserLogin, TokenResponse, RefreshRequest, UserResponse

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(user_id: str, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    return jwt.encode({"sub": user_id, "exp": expire}, settings.secret_key, algorithm="HS256")


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    free_plan = await db.execute(select(Plan).where(Plan.slug == "free"))
    plan = free_plan.scalar_one_or_none()

    user = User(
        email=data.email,
        password_hash=pwd_context.hash(data.password),
        name=data.name,
        plan_id=plan.id if plan else None,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        plan_slug=plan.slug if plan else None,
        created_at=user.created_at,
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return TokenResponse(
        access_token=create_token(str(user.id), timedelta(minutes=settings.access_token_expire_minutes)),
        refresh_token=create_token(str(user.id), timedelta(days=settings.refresh_token_expire_days)),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(data.refresh_token, settings.secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.id == user_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=401, detail="User not found")

    return TokenResponse(
        access_token=create_token(user_id, timedelta(minutes=settings.access_token_expire_minutes)),
        refresh_token=create_token(user_id, timedelta(days=settings.refresh_token_expire_days)),
    )


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)):
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        plan_slug=user.plan.slug if user.plan else None,
        created_at=user.created_at,
    )
