from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc),
                        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))

    def save(self, session):
        session.add(self)
        session.commit()