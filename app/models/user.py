from sqlalchemy import Column, String, Boolean, ForeignKey, UUID
from sqlalchemy.orm import relationship
import uuid
from .base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id'), nullable=True)

    tasks = relationship("Task", back_populates="user")
    company = relationship("Company", back_populates="users")