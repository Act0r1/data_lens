from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.deps import engine
from src.models.user import Base
from src.routers import auth, files, analysis, chat, charts, billing


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     await engine.dispose()


app = FastAPI(title="DataLens API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(charts.router, prefix="/api/v1/charts", tags=["charts"])
app.include_router(billing.router, prefix="/api/v1/billing", tags=["billing"])
