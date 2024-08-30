from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import get_config

config = get_config()
DATABASE_URL = config.POSTGRES_URI
# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an asynchronous session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Dependency function to get the session
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session