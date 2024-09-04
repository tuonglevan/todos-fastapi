import os
from dotenv import load_dotenv

from pydantic.v1 import BaseSettings, PostgresDsn

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    DEFAULT_PASSWORD_ADMIN: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

def get_database_url(async_mode: bool = True) -> str:
    scheme = 'postgresql+asyncpg' if async_mode else 'postgresql'
    return PostgresDsn.build(
        scheme=scheme,
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        path=f'/{os.getenv("POSTGRES_DB")}'
    )

def get_config() -> Settings:
    return Settings()