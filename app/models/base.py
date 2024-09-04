from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime

from app.utils.time_utils import get_current_utc_datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), nullable=False, default=get_current_utc_datetime())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=get_current_utc_datetime(), onupdate=get_current_utc_datetime())