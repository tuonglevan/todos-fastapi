from uuid import UUID
from typing import Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, cast, Boolean

ModelType = TypeVar("ModelType")

class BaseCRUDService:
    def __init__(self, async_session: AsyncSession = None):
        self.async_session = async_session

    async def get_by_id(self, model: Type[ModelType], model_id: UUID) -> ModelType:
        result = await self.async_session.execute(select(model).where(cast(model.id == model_id, Boolean)))
        entity = result.scalar_one_or_none()
        return entity

    async def update_by_id(self, model: Type[ModelType], model_id: UUID, update_data: dict) -> ModelType | None:
        async with self.async_session.begin():
            result = await self.async_session.execute(select(model).where(model.id == model_id))
            entity = result.scalar_one_or_none()
            if not entity:
                return None
            for attr, value in update_data.items():
                setattr(entity, attr, value)
            self.async_session.add(entity)
            await self.async_session.commit()
            await self.async_session.refresh(entity)
            return entity

    async def delete_by_id(self, model: Type[ModelType], model_id: UUID) -> bool:
        async with self.async_session.begin():
            entity = await self.get_by_id(model, model_id)
            if not entity:
                return False
            await self.async_session.delete(entity)
            await self.async_session.commit()
            return True