from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies.auth import is_admin
from app.dependencies.services import get_company_service
from app.exceptions.company_exceptions import CompanyNotFoundException
from app.schemas.company import CompanyResponseDetail, CompanyCreate, CompanyUpdate
from app.services import company_service as CompanyService
from app.transformers.company_transformers import transform_to_company_response_detail

router = APIRouter(prefix="/companies", tags=["Companies"], dependencies=[Depends(is_admin)])

@router.get("", status_code=status.HTTP_200_OK, response_model=List[CompanyResponseDetail])
async def get_companies(company_service: CompanyService = Depends(get_company_service)):
    companies = await company_service.get_companies()
    return [transform_to_company_response_detail(company) for company in companies]

@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponseDetail)
async def get_company(company_id: UUID, company_service: CompanyService = Depends(get_company_service)):
    company_info = await company_service.get_company_by_id(company_id=company_id)
    if not company_info:
        raise CompanyNotFoundException()
    return transform_to_company_response_detail(company_info)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyResponseDetail)
def create_company(company: CompanyCreate, company_service: CompanyService = Depends(get_company_service)):
    company_info = company_service.create_company(company=company)
    return transform_to_company_response_detail(company_info)

@router.put("/{company_id}", response_model=CompanyResponseDetail, status_code=status.HTTP_200_OK)
async def update_company(company_id: UUID, company: CompanyUpdate, company_service: CompanyService = Depends(get_company_service)):
    updated_company = await company_service.update_company(company_id=company_id, company=company)
    if not updated_company:
        raise CompanyNotFoundException()
    return transform_to_company_response_detail(updated_company)

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: UUID, company_service: CompanyService = Depends(get_company_service)):
    result = await company_service.delete_company(company_id=company_id)
    if not result:
        raise CompanyNotFoundException()