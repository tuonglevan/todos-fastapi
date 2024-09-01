from datetime import datetime

from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    company_id: Optional[UUID] = None
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

class UserInToken(BaseModel):
    id: UUID
    sub: str  # user.username
    first_name: str
    last_name: str
    is_admin: bool

class UserInfo(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str

class UserCreate(BaseModel):
    company_id: str
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponseDetail(BaseModel):
    id: UUID
    company_name: Optional[str] = None
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True