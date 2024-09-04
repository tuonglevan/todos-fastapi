from typing import Sequence
from uuid import UUID

from sqlalchemy import select, cast, Boolean, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from .base_crud_service import BaseCRUDService

class CompanyService(BaseCRUDService):
    def __init__(self, async_session: AsyncSession = None, sync_session: Session = None):
        super().__init__(async_session)
        self.sync_session = sync_session

    async def get_companies(self) -> Sequence[Company]:
        result = await self.async_session.scalars(select(Company).order_by(desc(Company.created_at)))
        return result.all()

    async def get_company_by_id(self, company_id: UUID) -> Company:
        result = await self.async_session.execute(select(Company).filter(cast(Company.id == company_id, Boolean)))
        return result.scalar_one_or_none()

    def create_company(self, company: CompanyCreate):
        db_company = Company(**company.model_dump())
        self.sync_session.add(db_company)
        self.sync_session.commit()
        self.sync_session.refresh(db_company)
        return db_company

    async def update_company(self, company_id: UUID, company_update: CompanyUpdate) -> Company | None:
        return await self.update_by_id(Company, company_id, company_update.model_dump(exclude_unset=True))

    async def delete_company(self, company_id: UUID) -> bool:
        return await self.delete_by_id(Company, company_id)