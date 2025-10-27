from celery import shared_task
from app.core.db import AsyncSessionLocal
from app.services.stats_updater import calculate_and_save_stats
from app.core.config import settings


@shared_task
def update_stats_task():
    import asyncio

    async def runner():
        async with AsyncSessionLocal() as db:
            await calculate_and_save_stats(db)

    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(runner())
    else:
        loop.run_until_complete(runner())