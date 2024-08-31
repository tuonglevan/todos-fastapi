from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from app.core.db import get_sync_db_session, get_async_db_session
from app.exceptions.company_exceptions import CompanyNotFoundException
from app.schemas.company import CompanyResponseDetail, CompanyCreate, CompanyUpdate
from app.services import company as CompanyService
from app.services.auth import is_admin

router = APIRouter(prefix="/companies", tags=["Companies"], dependencies=[Depends(is_admin)])

def transform_to_company_response_detail(company) -> CompanyResponseDetail:
    return CompanyResponseDetail(
        id=company.id,
        name=company.name,
        description=company.description,
        status="Active" if company.mode else "Inactive",
        created_at=company.created_at
    )

@router.get("", status_code=status.HTTP_200_OK, response_model=List[CompanyResponseDetail])
async def get_companies(async_session: AsyncSession = Depends(get_async_db_session)):
    companies = await CompanyService.get_companies(async_session)
    return [transform_to_company_response_detail(company) for company in companies]

@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponseDetail)
async def get_company(company_id: UUID, async_session: AsyncSession = Depends(get_async_db_session)):
    company_info = await CompanyService.get_company_by_id(async_session=async_session, company_id=company_id)
    if not company_info:
        raise CompanyNotFoundException()
    return transform_to_company_response_detail(company_info)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyResponseDetail)
def create_company(company: CompanyCreate, sync_session: Session = Depends(get_sync_db_session)):
    company_info = CompanyService.create_company(sync_session=sync_session, company=company)
    return transform_to_company_response_detail(company_info)

@router.put("/{company_id}", response_model=CompanyResponseDetail, status_code=status.HTTP_200_OK)
async def update_company(company_id: UUID, company: CompanyUpdate, async_session: AsyncSession = Depends(get_async_db_session)):
    updated_company = await CompanyService.update_company(async_session=async_session, company_id=company_id, company=company)
    if not updated_company:
        raise CompanyNotFoundException()
    return transform_to_company_response_detail(updated_company)

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: UUID, async_session: AsyncSession = Depends(get_async_db_session)):
    result = await CompanyService.delete_company(async_session=async_session, company_id=company_id)
    if not result:
        raise CompanyNotFoundException()