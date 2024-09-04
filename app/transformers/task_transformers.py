from typing import Sequence

from app.models import Task
from app.schemas.paginate import PaginatedResponse
from app.schemas.task import TaskResponseDetail
from app.schemas.user import UserInfo

# Define a type alias for PaginatedResponse of TaskResponseDetail
TasksPaginatedResponse = PaginatedResponse[TaskResponseDetail]

def transform_to_task_response(task: Task) -> TaskResponseDetail:
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

def generate_tasks_paginated_response(tasks: Sequence[Task], total: int, skip: int, limit: int) -> TasksPaginatedResponse:
    return TasksPaginatedResponse(
        total=total,
        page=(skip // limit) + 1,
        size=limit,
        items=[transform_to_task_response(task) for task in tasks]
    )