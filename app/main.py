from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import routes_auth, routes_users
from app.db.session import engine
from app.db.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[override]
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)


app.include_router(
    routes_auth.router,
    prefix=settings.API_V1_PREFIX + "/auth",
    tags=["auth"],
)
app.include_router(
    routes_users.router,
    prefix=settings.API_V1_PREFIX + "/users",
    tags=["users"],
)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
