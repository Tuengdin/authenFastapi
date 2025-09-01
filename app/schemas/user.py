from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    guest = "guest"
    member = "member"
    admin = "admin"
    superadmin = "superadmin"


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole | None = None
    is_verified: bool | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
