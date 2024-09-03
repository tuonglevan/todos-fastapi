from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies.services import get_user_service, get_company_service
from app.dependencies.auth import is_admin
from app.exceptions.company_exceptions import CompanyNotFoundException
from app.exceptions.user_exceptions import UserNotFoundException
from app.schemas.user import UserResponseDetail, UserCreate, UserUpdate
from app.services.company_service import CompanyService
from app.services.user_service import UserService
from app.transformers.user_transformers import transform_to_user_response

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(is_admin)])

async def check_company_exists(company_id: UUID, company_service: CompanyService):
    company = await company_service.get_company_by_id(company_id)
    if not company:
        raise CompanyNotFoundException(detail=f"Company with ID {company_id} not found")

@router.get("", status_code=status.HTTP_200_OK, response_model=List[UserResponseDetail])
async def get_users(user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_users()
    return [transform_to_user_response(user) for user in users]

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseDetail)
async def get_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    user_info = await user_service.get_user_by_id(user_id=user_id)
    if not user_info:
        raise UserNotFoundException()
    return transform_to_user_response(user_info)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseDetail)
async def create_user(user_create: UserCreate, user_service: UserService = Depends(get_user_service), company_service: CompanyService = Depends(get_company_service)):
    if user_create.company_id is not None:
        await check_company_exists(user_create.company_id, company_service)
    user_info = user_service.create_user(user_create=user_create)
    return transform_to_user_response(user_info)

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseDetail)
async def update_user(user_id: UUID, user_update: UserUpdate, user_service: UserService = Depends(get_user_service), company_service: CompanyService = Depends(get_company_service)):
    if user_update.company_id is not None:
        await check_company_exists(user_update.company_id, company_service)
    user_info = await user_service.update_user(user_id=user_id, user_update=user_update)
    if not user_info:
        raise UserNotFoundException()
    return transform_to_user_response(user_info)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    success = await user_service.delete_user(user_id=user_id)
    if not success:
        raise UserNotFoundException()