from fastapi import FastAPI
from app.core.db import engine, Base
from app.api.routers.chat_router import router as chat_router
from app.api.routers.message_router import router as message_router
from app.api.routers.promo_router import router as promo_router
from app.api.routers.stats_router import router as stats_router
import asyncio

app = FastAPI(
    title="OZON Chat Manager",
    description="Сервис для управления чатами OZON",
    version="1.0.0",
)

# Подключаем роутеры (эндпоинты)
app.include_router(chat_router, prefix="/chats", tags=["Chats"])
app.include_router(message_router, prefix="/messages", tags=["Messages"])
app.include_router(promo_router, prefix="/promo", tags=["Promo Codes"])
app.include_router(stats_router, prefix="/stats", tags=["Statistics"])


@app.on_event("startup")
async def on_startup():
    # Создание таблиц, если используется auto create (для dev)
    async with engine.begin() as conn:
        # здесь можно делать create_all - для dev, везде где нужны миграции - не используйте
        await conn.run_sync(Base.metadata.create_all)
    # Здесь также можно инициализировать соединения с Redis, Celery и прочим


@app.on_event("shutdown")
async def on_shutdown():
    pass
