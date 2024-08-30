from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from .base import BaseModel


class StatusEnum(enum.Enum):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'


class PriorityEnum(enum.Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


class Task(BaseModel):
    __tablename__: str = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    summary = Column(String(length=255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.TODO)
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.MEDIUM)

    user = relationship("User", back_populates="tasks")