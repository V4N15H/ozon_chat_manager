from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL
    OZON_CLIENT_ID: str = os.getenv("OZON_CLIENT_ID")
    OZON_API_KEY: str = os.getenv("OZON_API_KEY")

    class Config:
        env_file = ".env"


settings = Settings()
