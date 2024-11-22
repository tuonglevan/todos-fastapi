from uuid import UUID
from typing import Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, cast, Boolean
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseCRUDService:
    def __init__(self, async_session: AsyncSession = None, sync_session: Session = None):
        self.async_session = async_session
        self.sync_session = sync_session

    async def get_by_id(self, model: Type[ModelType], model_id: UUID) -> ModelType:
        result = await self.async_session.execute(select(model).where(cast(model.id == model_id, Boolean)))
        entity = result.scalar_one_or_none()
        return entity

    async def update_by_id(self, model: Type[ModelType], model_id: UUID, update_data: dict) -> ModelType | None:
        entity = self.sync_session.scalar(select(model).where(cast(model.id == model_id, Boolean)))
        if not entity:
            return None
        for attr, value in update_data.items():
            setattr(entity, attr, value)
        self.sync_session.add(entity)
        self.sync_session.commit()
        self.sync_session.refresh(entity)

        return entity

    async def delete_by_id(self, model: Type[ModelType], model_id: UUID) -> bool:
        async with self.async_session.begin():
            entity = await self.get_by_id(model, model_id)
            if not entity:
                return False
            await self.async_session.delete(entity)
            await self.async_session.commit()
            return True