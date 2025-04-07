import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
settings = Settings()