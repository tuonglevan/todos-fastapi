from sqlalchemy import Column, String, Text, Float, DateTime, UUID
from sqlalchemy.orm import relationship
import uuid
from .base import BaseModel

class Company(BaseModel):
    __tablename__ = 'companies'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=255), nullable=False)
    description = Column(Text, nullable=True)
    mode = Column(String(length=50), nullable=False)
    rating = Column(Float, nullable=False)

    users = relationship("User", back_populates="company")