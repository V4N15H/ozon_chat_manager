from celery import shared_task
from app.core.db import AsyncSessionLocal
from app.services.message_sender import send_promo_messages
from app.core.config import settings
from app.core.config import settings


@shared_task
def check_promos_task():
    import asyncio

    async def runner():
        async with AsyncSessionLocal() as db:
            await send_promo_messages(db, settings.OZON_CLIENT_ID, settings.OZON_API_KEY)

    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(runner())
    else:
        loop.run_until_complete(runner())