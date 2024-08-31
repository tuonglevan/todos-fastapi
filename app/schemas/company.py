from datetime import datetime

from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CompanyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    mode: Optional[bool] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[bool] = None

class CompanyResponseDetail(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    status: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True