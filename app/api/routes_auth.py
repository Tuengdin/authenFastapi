from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.services import user_service, auth_service

router = APIRouter()


@router.post("/register", response_model=Token, status_code=201)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await user_service.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=400, detail="Email already registered"
        )
    user = await user_service.create_user(db, user_in)
    tokens = await auth_service.generate_tokens(user)
    return {**tokens, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await user_service.authenticate(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    tokens = await auth_service.generate_tokens(user)
    return {**tokens, "token_type": "bearer"}


@router.post("/refresh")
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    new_access = await auth_service.refresh_access_token(db, refresh_token)
    if not new_access:
        raise HTTPException(
            status_code=401, detail="Invalid refresh token"
        )
    return {"access_token": new_access, "token_type": "bearer"}
