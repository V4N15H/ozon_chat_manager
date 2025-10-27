from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://username:password@host:port/ozon_promo_db"
    )
    REDIS_URL: str = "redis://:password@host:port/0"
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL
    OZON_CLIENT_ID: str = "******"
    OZON_API_KEY: str = "******"

    class Config:
        env_file = ".env"


settings = Settings()
