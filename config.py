
from pydantic_settings import BaseSettings, SettingsConfigDict


class Secrets(BaseSettings):
     DB_HOST: str
     DB_PORT: str
     DB_NAME: str
     DB_USER: str
     DB_PASS: str
     
     model_config = SettingsConfigDict(env_file='.env')
     
secret = Secrets()