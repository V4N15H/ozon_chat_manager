from celery import shared_task
from app.core.db import AsyncSessionLocal
from app.services.message_parser import fetch_and_save_messages
from app.core.config import settings


@shared_task
def parse_messages_task():
    import asyncio

    async def runner():
        async with AsyncSessionLocal() as db:
            await fetch_and_save_messages(
                db, settings.OZON_CLIENT_ID, settings.OZON_API_KEY
            )

    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(runner())
    else:
        loop.run_until_complete(runner())
