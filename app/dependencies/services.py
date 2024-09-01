from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from .config import get_config
from .db import get_async_db_session, get_sync_db_session
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.company_service import CompanyService
from app.services.task_service import TaskService

def get_user_service(
        async_session: AsyncSession = Depends(get_async_db_session),
        sync_session: Session = Depends(get_sync_db_session)
) -> UserService:
    return UserService(async_session=async_session, sync_session=sync_session)

def get_auth_service(
        user_service: UserService = Depends(get_user_service),
        config=Depends(get_config),
) -> AuthService:
    return AuthService(config=config, user_service=user_service)

def get_company_service(
        async_session: AsyncSession = Depends(get_async_db_session),
        sync_session: Session = Depends(get_sync_db_session)
) -> CompanyService:
    return CompanyService(async_session=async_session, sync_session=sync_session)

def get_task_service(
        async_session: AsyncSession = Depends(get_async_db_session),
        sync_session: Session = Depends(get_sync_db_session)
) -> TaskService:
    return TaskService(async_session=async_session, sync_session=sync_session)