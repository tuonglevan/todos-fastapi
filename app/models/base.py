from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime

from app.utils.time_utils import get_current_utc_datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    def save(self, session):
        session.add(self)
        session.commit()