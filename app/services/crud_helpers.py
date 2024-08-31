from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import cast
from sqlalchemy.types import Boolean
from typing import Type
from uuid import UUID


async def delete_record(async_session: AsyncSession, model: Type, record_id: UUID) -> bool:
    result = await async_session.execute(select(model).where(cast(model.id == record_id, Boolean)))
    record = result.scalar_one_or_none()

    if not record:
        return False

    await async_session.delete(record)
    await async_session.commit()
    return True