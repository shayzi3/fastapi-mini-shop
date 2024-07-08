
from pydantic_settings import BaseSettings, SettingsConfigDict


class Secrets(BaseSettings):
     DB_HOST: str
     DB_PORT: str
     DB_NAME: str
     DB_USER: str
     DB_PASS: str
     
     model_config = SettingsConfigDict(env_file='.env')
     
     
     @classmethod
     async def get_postgresql_url(cls) -> str:
          return f'postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASS}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}'
     
     
secret = Secrets()