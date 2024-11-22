from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from starlette import status as StatusCode

from app.dependencies.auth import is_authenticated, is_admin
from app.dependencies.services import get_task_service, get_user_service
from app.exceptions.task_exceptions import TaskNotFoundException
from app.exceptions.user_exceptions import UserNotFoundException
from app.models import User
from app.models.task import StatusEnum, PriorityEnum
from app.schemas.task import TaskResponseDetail, TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from app.services.user_service import UserService
from app.transformers.task_transformers import transform_to_task_response, TasksPaginatedResponse, generate_tasks_paginated_response

router = APIRouter(prefix="/tasks", tags=["Tasks"])

async def check_user_exists(user_id: UUID, user_service: UserService):
    company = await user_service.get_user_by_id(user_id)
    if not company:
        raise UserNotFoundException(detail=f"User with ID {user_id} not found")

@router.get("", status_code=StatusCode.HTTP_200_OK, response_model=TasksPaginatedResponse, dependencies=[Depends(is_authenticated)])
async def get_tasks(
        status: Optional[StatusEnum] = Query(None),
        priority: Optional[PriorityEnum] = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        task_service: TaskService = Depends(get_task_service),
        current_user: User = Depends(is_authenticated)
):
    if current_user.is_admin:
        tasks, total = await task_service.get_tasks(status=status, priority=priority, skip=skip, limit=limit)
    else:
        tasks, total = await task_service.get_tasks(user_id=current_user.id, status=status, priority=priority, skip=skip, limit=limit)
    return generate_tasks_paginated_response(tasks, total, skip, limit)

@router.get("/{task_id}", status_code=StatusCode.HTTP_200_OK, response_model=TaskResponseDetail, dependencies=[Depends(is_authenticated)])
async def get_task(task_id: UUID, task_service: TaskService = Depends(get_task_service), current_user: User = Depends(is_authenticated)):
    if current_user.is_admin:
        task_info = await task_service.get_task_by_id(task_id=task_id)
    else:
        task_info = await task_service.get_task_by_id_and_user_id(task_id=task_id, user_id=current_user.id)
    if not task_info:
        raise TaskNotFoundException()
    return transform_to_task_response(task_info)

@router.get("/user/{user_id}", status_code=StatusCode.HTTP_200_OK, response_model=List[TaskResponseDetail], dependencies=[Depends(is_admin)])
async def get_tasks_by_user_id(user_id: UUID, task_service: TaskService = Depends(get_task_service)):
    tasks = await task_service.get_tasks_by_user_id(user_id=user_id)
    return [transform_to_task_response(task) for task in tasks]

@router.get("/user/{user_id}/completed", status_code=StatusCode.HTTP_200_OK, response_model=List[TaskResponseDetail], dependencies=[Depends(is_authenticated)])
async def get_completed_tasks_by_user_id(user_id: UUID, task_service: TaskService = Depends(get_task_service)):
    tasks = await task_service.get_tasks_by_user_id_and_status(user_id=user_id, status=StatusEnum.DONE)
    return [transform_to_task_response(task) for task in tasks]

@router.get("/company/{company_id}/completed", status_code=StatusCode.HTTP_200_OK, response_model=List[TaskResponseDetail], dependencies=[Depends(is_authenticated)])
async def get_completed_tasks_by_company_id(company_id: UUID, task_service: TaskService = Depends(get_task_service)):
    tasks = await task_service.get_tasks_by_company_id_and_status(company_id=company_id, status=StatusEnum.DONE)
    return [transform_to_task_response(task) for task in tasks]

@router.post("", status_code=StatusCode.HTTP_201_CREATED, response_model=TaskResponseDetail, dependencies=[Depends(is_admin)])
async def create_task(task_create: TaskCreate, task_service: TaskService = Depends(get_task_service), user_service: UserService = Depends(get_user_service)):
    if task_create.user_id is not None:
        await check_user_exists(task_create.user_id, user_service)
    task = task_service.create_task(task_create=task_create)
    return transform_to_task_response(task)

@router.put("/{task_id}", status_code=StatusCode.HTTP_200_OK, response_model=TaskResponseDetail, dependencies=[Depends(is_admin)])
async def update_task(task_id: UUID, task_update: TaskUpdate, task_service: TaskService = Depends(get_task_service), user_service: UserService = Depends(get_user_service)):
    if task_update.user_id is not None:
        await check_user_exists(task_update.user_id, user_service)
    task = await task_service.update_task(task_id=task_id, task_update=task_update)
    if not task:
        raise TaskNotFoundException
    return transform_to_task_response(task)

@router.delete("/{task_id}", status_code=StatusCode.HTTP_200_OK, dependencies=[Depends(is_admin)])
async def delete_task(task_id: UUID, task_service: TaskService = Depends(get_task_service)):
    success = await task_service.delete_task(task_id=task_id)
    if not success:
        raise TaskNotFoundException()