from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserOut, UserUpdate
from app.api.deps import get_current_user, require_role
from app.services import user_service
from app.models.user import UserRole, User

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserOut)
async def update_me(
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = await user_service.update_user(db, current_user, user_in)
    return user


@router.get(
    "/{user_id}",
    response_model=UserOut,
    dependencies=[
        Depends(
            require_role(
                [UserRole.admin, UserRole.superadmin]
            )
        )
    ],
)
async def get_user(
    user_id: int, db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
