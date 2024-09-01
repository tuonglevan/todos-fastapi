from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.task import StatusEnum, PriorityEnum
from app.schemas.user import UserInfo


class TaskCreate(BaseModel):
    user_id: UUID
    summary: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.TODO
    priority: PriorityEnum = PriorityEnum.LOW

class TaskUpdate(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None

class TaskResponseDetail(BaseModel):
    task_id: UUID
    user_info: UserInfo
    summary: str
    description: Optional[str]
    status: StatusEnum
    priority: PriorityEnum
    created_at: datetime