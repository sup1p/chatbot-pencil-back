import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    GEMINI_API_KEY: str
    from dotenv import load_dotenv
    load_dotenv()

    class Config:
        env_file = ".env"
settings = Settings()