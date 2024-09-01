from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.dependencies.config import get_database_url

DATABASE_URL = get_database_url(async_mode=False)
DATABASE_URL_ASYNC = get_database_url(async_mode=True)

# Create a configured "Session" class
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# Create an asynchronous engine
async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)
# Create an asynchronous session factory
AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

def get_sync_db_session() -> Generator:
    db = SessionLocal()
    try:
      yield db
    finally:
        db.close()

# Dependency function to get the session
async def get_async_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session