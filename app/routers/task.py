from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status as StatusCode

from app.core.db import get_async_db_session, get_sync_db_session
from app.exceptions.task_exceptions import TaskNotFoundException
from app.models.task import StatusEnum, PriorityEnum
from app.schemas.paginate import PaginatedResponse
from app.schemas.task import TaskResponseDetail, TaskCreate, TaskUpdate
from app.schemas.user import UserInfo
from app.services import task as TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])
# Define a PaginatedResponse for tasks
PaginatedTasksResponse = PaginatedResponse[TaskResponseDetail]

def transform_to_task_response(task) -> TaskResponseDetail:
    return TaskResponseDetail(
        task_id=task.id,
        user_info=UserInfo(
            user_id=task.user_id,
            first_name=task.user.first_name,
            last_name=task.user.last_name
        ),
        summary=task.summary,
        description=task.description,
        status=task.status,
        priority=task.priority,
        created_at=task.created_at
    )

@router.get("", status_code=StatusCode.HTTP_200_OK, response_model=PaginatedTasksResponse)
async def get_tasks(
        status: Optional[StatusEnum] = Query(None),
        priority: Optional[PriorityEnum] = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        async_session: AsyncSession = Depends(get_async_db_session)
):
    tasks, total = await TaskService.get_tasks(async_session=async_session, status=status, priority=priority, skip=skip, limit=limit)
    return PaginatedTasksResponse(
        total=total,
        page=(skip // limit) + 1,
        size=limit,
        items=[transform_to_task_response(task) for task in tasks]
    )

@router.get("/{task_id}", status_code=StatusCode.HTTP_200_OK, response_model=TaskResponseDetail)
async def get_user(task_id: UUID, async_session: AsyncSession = Depends(get_async_db_session)):
    task_info = await TaskService.get_task_by_id(async_session=async_session, task_id=task_id)
    if not task_info:
        raise TaskNotFoundException()
    return transform_to_task_response(task_info)

@router.get("/user/{user_id}", status_code=StatusCode.HTTP_200_OK, response_model=List[TaskResponseDetail])
async def get_tasks_by_user_id(user_id: UUID, async_session: AsyncSession = Depends(get_async_db_session)):
    tasks = await TaskService.get_tasks_by_user_id(user_id=user_id, async_session=async_session)
    return [transform_to_task_response(task) for task in tasks]

@router.post("", status_code=StatusCode.HTTP_201_CREATED, response_model=TaskResponseDetail)
def create_task(task_create: TaskCreate, sync_session: Session = Depends(get_sync_db_session)):
    task = TaskService.create_task(sync_session=sync_session, task_create=task_create)
    return transform_to_task_response(task)

@router.put("/{task_id}", status_code=StatusCode.HTTP_200_OK, response_model=TaskResponseDetail)
async def update_task(task_id: UUID, task_update: TaskUpdate, async_session: AsyncSession = Depends(get_async_db_session)):
    task = await TaskService.update_task(task_id=task_id, async_session=async_session, task_update=task_update)
    if not task:
        raise TaskNotFoundException
    return transform_to_task_response(task)

@router.delete("/{task_id}", status_code=StatusCode.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, async_session: AsyncSession = Depends(get_async_db_session)):
    success = await TaskService.delete_task(task_id=task_id, async_session=async_session)
    if not success:
        raise TaskNotFoundException()