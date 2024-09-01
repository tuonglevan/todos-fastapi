from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from starlette import status as StatusCode

from app.dependencies.services import get_task_service
from app.exceptions.task_exceptions import TaskNotFoundException
from app.models.task import StatusEnum, PriorityEnum
from app.schemas.paginate import PaginatedResponse
from app.schemas.task import TaskResponseDetail, TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from app.transformers.task_transformers import transform_to_task_response

router = APIRouter(prefix="/tasks", tags=["Tasks"])
# Define a PaginatedResponse for tasks
PaginatedTasksResponse = PaginatedResponse[TaskResponseDetail]

@router.get("", status_code=StatusCode.HTTP_200_OK, response_model=PaginatedTasksResponse)
async def get_tasks(
        status: Optional[StatusEnum] = Query(None),
        priority: Optional[PriorityEnum] = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        task_service: TaskService = Depends(get_task_service)
):
    tasks, total = await task_service.get_tasks(status=status, priority=priority, skip=skip, limit=limit)
    return PaginatedTasksResponse(
        total=total,
        page=(skip // limit) + 1,
        size=limit,
        items=[transform_to_task_response(task) for task in tasks]
    )

@router.get("/{task_id}", status_code=StatusCode.HTTP_200_OK, response_model=TaskResponseDetail)
async def get_user(task_id: UUID, task_service: TaskService = Depends(get_task_service)):
    task_info = await task_service.get_task_by_id(task_id=task_id)
    if not task_info:
        raise TaskNotFoundException()
    return transform_to_task_response(task_info)

@router.get("/user/{user_id}", status_code=StatusCode.HTTP_200_OK, response_model=List[TaskResponseDetail])
async def get_tasks_by_user_id(user_id: UUID, task_service: TaskService = Depends(get_task_service)):
    tasks = await task_service.get_tasks_by_user_id(user_id=user_id)
    return [transform_to_task_response(task) for task in tasks]

@router.post("", status_code=StatusCode.HTTP_201_CREATED, response_model=TaskResponseDetail)
def create_task(task_create: TaskCreate, task_service: TaskService = Depends(get_task_service)):
    task = task_service.create_task(task_create=task_create)
    return transform_to_task_response(task)

@router.put("/{task_id}", status_code=StatusCode.HTTP_200_OK, response_model=TaskResponseDetail)
async def update_task(task_id: UUID, task_update: TaskUpdate, task_service: TaskService = Depends(get_task_service)):
    task = await task_service.update_task(task_id=task_id, task_update=task_update)
    if not task:
        raise TaskNotFoundException
    return transform_to_task_response(task)

@router.delete("/{task_id}", status_code=StatusCode.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, task_service: TaskService = Depends(get_task_service)):
    success = await task_service.delete_task(task_id=task_id)
    if not success:
        raise TaskNotFoundException()