from typing import Sequence, Tuple, Any
from uuid import UUID

from sqlalchemy import select, cast, Boolean, desc, ScalarResult, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from app.models import Task
from app.models.task import StatusEnum, PriorityEnum
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.crud_helpers import delete_record

async def get_tasks(
        async_session: AsyncSession,
        status: StatusEnum = None,
        priority: PriorityEnum = None,
        skip: int = 0,
        limit: int = 10
) -> Tuple[Sequence[Task], int]:
    # Count Query
    count_query = select(func.count(Task.id))
    if status is not None:
        count_query = count_query.where(cast(Task.status == status, Boolean))
    if priority is not None:
        count_query = count_query.where(cast(Task.priority == priority, Boolean))

    total_result = await async_session.execute(count_query)
    total_count = total_result.scalar()

    # Data Query
    data_query = select(Task).options(joinedload(Task.user, innerjoin=True))
    if status is not None:
        data_query = data_query.where(cast(Task.status == status, Boolean))
    if priority is not None:
        data_query = data_query.where(cast(Task.priority == priority, Boolean))

    data_query = data_query.offset(skip).limit(limit).order_by(desc(Task.created_at))

    result = await async_session.execute(data_query)
    tasks = result.scalars().all()

    return tasks, total_count

async def get_task_by_id(async_session: AsyncSession, task_id: UUID) -> Task:
    result = await async_session.execute(
        select(Task)
        .options(joinedload(Task.user, innerjoin=True))
        .filter(cast(Task.id == task_id, Boolean))
    )
    return result.scalar_one_or_none()

async def get_tasks_by_user_id(user_id: UUID, async_session: AsyncSession) -> Sequence[Task]:
    result = await async_session.execute(
        select(Task)
        .options(joinedload(Task.user, innerjoin=True))
        .filter(cast(Task.user_id == user_id, Boolean))
    )
    return result.scalars().all()

def create_task(sync_session: Session, task_create: TaskCreate) -> Task:
    task_info = Task(**task_create.model_dump())
    sync_session.add(task_info)
    sync_session.commit()
    sync_session.refresh(task_info)

    return task_info

async def update_task(task_id: UUID, async_session: AsyncSession, task_update: TaskUpdate) -> Task | None:
    result = await async_session.execute(
        select(Task)
        .options(joinedload(Task.user, innerjoin=True))
        .where(cast(Task.id == task_id, Boolean))
    )
    task_info = result.scalar_one_or_none()
    if not task_info:
        return None

    for attr, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task_info, attr, value)
    async_session.add(task_info)
    await async_session.commit()
    await async_session.refresh(task_info)

    return task_info

async def delete_task(async_session: AsyncSession, task_id: UUID) -> bool:
    return await delete_record(async_session, Task, task_id)