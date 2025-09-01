from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.token_blacklist import TokenBlacklist
from app.models.user import User


async def generate_tokens(user: User):
    return {
        "access_token": create_access_token(str(user.id)),
        "refresh_token": create_refresh_token(str(user.id)),
    }


async def blacklist_token(db: AsyncSession, jti: str):
    entry = TokenBlacklist(jti=jti)
    db.add(entry)
    await db.commit()


async def is_token_blacklisted(db: AsyncSession, jti: str) -> bool:
    stmt = select(TokenBlacklist).where(TokenBlacklist.jti == jti)
    res = await db.execute(stmt)
    return res.scalar_one_or_none() is not None


async def refresh_access_token(db: AsyncSession, refresh_token: str):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    # Optionally check blacklist
    return create_access_token(user_id)
