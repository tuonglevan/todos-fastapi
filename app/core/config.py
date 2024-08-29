from dotenv import load_dotenv
from typing import Optional, Any

from pydantic.v1 import BaseSettings, PostgresDsn, SecretStr, validator

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_ASYNC: Optional[bool] = False
    POSTGRES_URI: Optional[PostgresDsn] = None

    @validator('POSTGRES_URI', pre=True)
    def get_connection_string(cls, _: str, values: dict[str, Any]) -> str:
        postgres_password: SecretStr = values.get('POSTGRES_PASSWORD', SecretStr(''))
        scheme = 'postgresql+asyncpg' if values.get('POSTGRES_ASYNC') else 'postgresql'
        return PostgresDsn.build(
            scheme=scheme,
            user=values.get('POSTGRES_USER'),
            password=postgres_password.get_secret_value(),
            host=values.get('POSTGRES_HOST'),
            path=f'/{values.get("POSTGRES_DB")}'
        )

def get_config() -> Settings:
    return Settings()