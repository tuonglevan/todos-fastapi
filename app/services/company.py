from typing import Sequence
from uuid import UUID

from sqlalchemy import select, cast, Boolean, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from .crud_helpers import delete_record

async def get_companies(async_session: AsyncSession) -> Sequence[Company]:
    result = await async_session.scalars(select(Company).order_by(desc(Company.created_at)))
    return result.all()

async def get_company_by_id(async_session: AsyncSession, company_id: UUID) -> Company:
    result = await async_session.execute(select(Company).filter(cast(Company.id == company_id, Boolean)))
    return result.scalar_one_or_none()

def create_company(sync_session: Session, company: CompanyCreate):
    db_company = Company(**company.model_dump())
    sync_session.add(db_company)
    sync_session.commit()
    sync_session.refresh(db_company)
    return db_company

async def update_company(async_session: AsyncSession, company_id: UUID, company: CompanyUpdate) -> Company | None:
    result = await async_session.execute(select(Company).where(cast(Company.id == company_id, Boolean)))
    company_info = result.scalar_one_or_none()

    if not company_info:
        return None

    if company.name is not None:
        company_info.name = company.name
    if company.description is not None:
        company_info.description = company.description
    if company.mode is not None:
        company_info.mode = company.mode

    await async_session.commit()
    await async_session.refresh(company_info)

    return company_info

async def delete_company(async_session: AsyncSession, company_id: UUID) -> bool:
    return await delete_record(async_session, Company, company_id)