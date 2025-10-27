import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.stats import StatsCreateUpdate
from app.crud.chat import list_chats
from app.crud.stats import create_stats
from app.schemas.chat import ChatStatusEnum


async def calculate_and_save_stats(db: AsyncSession):
        # Получаем все чаты
        chats = await list_chats(db)

        stats = StatsCreateUpdate(
            total_chats = len(chats),
            new_chats = sum(1 for c in chats if c.status == ChatStatusEnum.NEW),
            in_progress = sum(1 for c in chats if c.status == ChatStatusEnum.IN_PROGRESS),
            declined = sum(1 for c in chats if c.status == ChatStatusEnum.DECLINED),
            done = sum(1 for c in chats if c.status == ChatStatusEnum.DONE),
            error = sum(1 for c in chats if c.status == ChatStatusEnum.ERROR),
            promo_sent = sum(1 for c in chats if c.status == ChatStatusEnum.DONE),
        )
        # Создаём объект статистики и сохраняем
        await  create_stats(db, stats)


