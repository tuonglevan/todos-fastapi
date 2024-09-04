from sqlalchemy import Column, String, Text, UUID, Boolean
from sqlalchemy.orm import relationship
import uuid
from .base import BaseModel

class Company(BaseModel):
    __tablename__ = 'companies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=255), nullable=False)
    description = Column(Text, nullable=True)
    mode = Column(Boolean, default=True)

    users = relationship("User", back_populates="company")