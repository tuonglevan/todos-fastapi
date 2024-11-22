from typing import Sequence, Tuple, Optional
from uuid import UUID

from sqlalchemy import select, cast, Boolean, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from app.models import Task, User
from app.models.task import StatusEnum, PriorityEnum
from app.schemas.task import TaskCreate, TaskUpdate
from .base_crud_service import BaseCRUDService

class TaskService(BaseCRUDService):
    def __init__(self, async_session: AsyncSession = None, sync_session: Session = None):
        super().__init__(async_session, sync_session)

    async def get_tasks(
            self,
            user_id: Optional[str] = None,
            status: StatusEnum = None,
            priority: PriorityEnum = None,
            skip: int = 0,
            limit: int = 10
    ) -> Tuple[Sequence[Task], int]:
        # Count Query
        count_query = select(func.count(Task.id))
        if user_id is not None:
            count_query = count_query.filter(cast(Task.user_id == user_id, Boolean))
        if status is not None:
            count_query = count_query.where(cast(Task.status == status, Boolean))
        if priority is not None:
            count_query = count_query.where(cast(Task.priority == priority, Boolean))

        total_result = await self.async_session.execute(count_query)
        total_count = total_result.scalar()

        # Data Query
        data_query = select(Task).options(joinedload(Task.user, innerjoin=True))
        if user_id is not None:
            data_query = data_query.filter(cast(Task.user_id == user_id, Boolean))
        if status is not None:
            data_query = data_query.where(cast(Task.status == status, Boolean))
        if priority is not None:
            data_query = data_query.where(cast(Task.priority == priority, Boolean))

        data_query = data_query.offset(skip).limit(limit).order_by(desc(Task.created_at))

        result = await self.async_session.execute(data_query)
        tasks = result.scalars().all()

        return tasks, total_count

    async def get_task_by_id(self, task_id: UUID) -> Task:
        result = await self.async_session.execute(
            select(Task)
            .options(joinedload(Task.user, innerjoin=True))
            .filter(cast(Task.id == task_id, Boolean))
        )
        return result.scalar_one_or_none()

    async def get_task_by_id_and_user_id(self, task_id: UUID, user_id: UUID) -> Task:
        result = await self.async_session.execute(
            select(Task)
            .options(joinedload(Task.user, innerjoin=True))
            .filter(cast(Task.id == task_id, Boolean), cast(Task.user_id == user_id, Boolean))
        )
        return result.scalar_one_or_none()

    async def get_tasks_by_user_id(self, user_id: UUID) -> Sequence[Task]:
        result = await self.async_session.execute(
            select(Task)
            .options(joinedload(Task.user, innerjoin=True))
            .filter(cast(Task.user_id == user_id, Boolean))
        )
        return result.scalars().all()

    async def get_tasks_by_user_id_and_status(self, user_id: UUID, status: StatusEnum) -> Sequence[Task]:
        result = await self.async_session.execute(
            select(Task)
            .options(joinedload(Task.user, innerjoin=True))
            .filter(cast(Task.user_id == user_id, Boolean), cast(Task.status == status, Boolean))
        )
        return result.scalars().all()

    async def get_tasks_by_company_id_and_status(self, company_id: UUID, status: StatusEnum) -> Sequence[Task]:
        result = await self.async_session.execute(
            select(Task)
            .options(joinedload(Task.user, innerjoin=True))
            .where(User.company_id == company_id, Task.status == status)
        )
        return result.scalars().all()

    def create_task(self, task_create: TaskCreate) -> Task:
        task_info = Task(**task_create.model_dump())
        self.sync_session.add(task_info)
        self.sync_session.commit()
        self.sync_session.refresh(task_info)

        return task_info

    async def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Task | None:
        return await self.update_by_id(Task, task_id, task_update.model_dump(exclude_unset=True))

    async def delete_task(self, task_id: UUID) -> bool:
        return await self.delete_by_id(Task, task_id)