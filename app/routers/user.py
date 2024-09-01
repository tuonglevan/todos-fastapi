from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from app.core.db import get_async_db_session, get_sync_db_session
from app.exceptions.user_exceptions import UserNotFoundException
from app.schemas.user import UserResponseDetail, UserCreate, UserUpdate
from app.services import user as UserService
from app.services.auth import is_admin

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(is_admin)])

def transform_to_user_response(user) -> UserResponseDetail:
    return UserResponseDetail(
        id=user.id,
        company_name=user.company.name if user.company else None,
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_admin=user.is_admin,
        created_at=user.created_at
    )

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserResponseDetail])
async def get_users(async_session: AsyncSession = Depends(get_async_db_session)):
    users = await UserService.get_users(async_session=async_session)
    return [transform_to_user_response(user) for user in users]

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseDetail)
async def get_user(user_id: UUID, async_session: AsyncSession = Depends(get_async_db_session)):
    user_info = await UserService.get_user_by_id(async_session=async_session, user_id=user_id)
    if not user_info:
        raise UserNotFoundException()
    return transform_to_user_response(user_info)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseDetail)
def create_user(user: UserCreate, sync_session: Session = Depends(get_sync_db_session)):
    user_info = UserService.create_user(sync_session=sync_session, user=user)
    return transform_to_user_response(user_info)

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseDetail)
async def update_user(user_id: UUID, user_update: UserUpdate, async_session: AsyncSession = Depends(get_async_db_session)):
    user_info = await UserService.update_user(async_session=async_session, user_id=user_id, user_update=user_update)
    if not user_info:
        raise UserNotFoundException()
    return transform_to_user_response(user_info)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, async_session: AsyncSession = Depends(get_sync_db_session)):
    success = await UserService.delete_user(async_session=async_session, user_id=user_id)
    if not success:
        raise UserNotFoundException()