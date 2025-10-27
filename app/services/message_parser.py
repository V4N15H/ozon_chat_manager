from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import httpx

from app.models.message import Message
from app.schemas.message import MessageCreate, SenderEnum
from app.schemas.order import OrderCreate, OrderUpdate, StatusEnum
from app.crud.message import create_message
from app.crud.order import create_order, get_order, update_order
from app.models.chat import Chat  # ORM модель чатов
from datetime import datetime, timezone, timedelta


async def message_exists(db: AsyncSession, chat_id: UUID, text: str) -> bool:
    query = select(Message).where(Message.chat_id == chat_id, Message.text == text)
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


async def get_order_status(order_number: str, client_id: str, api_key: str) -> str | None:
    # Получает статус заказа по order_number
    url = "https://api-seller.ozon.ru/v3/posting/fbs/list"
    headers = {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "dir": "DESC",
        "filter": {
            "since": (datetime.now(timezone.utc) - timedelta(days=30)).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "to": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
,
        },
        "limit": 100,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

    postings = data.get("result", {}).get("postings", [])
    for posting in postings:
        if posting.get("order_number") == order_number:
            status = posting.get("status")  # например, "awaiting_deliver"
            substatus = posting.get("substatus")
            if status == "cancelled" or "cancelled_from_split_pending":
                return StatusEnum.CANCELLED
            if substatus == "posting_received":
                return StatusEnum.RECEIVED
            else:
                return StatusEnum.CREATED
    return None


async def fetch_and_save_messages(
    db: AsyncSession, client_id: str, api_key: str, limit: int = 100
):
    url = "https://api-seller.ozon.ru/v3/chat/history"
    headers = {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }

    result = await db.execute(select(Chat.id, Chat.ozon_chat_id))
    chats = result.all()  # список кортежей (id, ozon_chat_id)

    async with httpx.AsyncClient() as client:
        for chat_id_db, ozon_chat_id in chats:
            json_payload = {
                "chat_id": str(ozon_chat_id),
                "limit": limit,
            }
            response = await client.post(url, headers=headers, json=json_payload)
            response.raise_for_status()
            data = response.json()

            messages = data.get("messages", [])
            for msg in messages:
                user_type = msg.get("user", {}).get("type", "").lower()
                order_number = msg.get("context", {}).get("order_number", "")
                text = msg.get("data", [""])[-1]

                if "промокод" not in text.lower():
                    continue

                if user_type == "support":
                    sender = SenderEnum.MANAGER
                elif user_type == "customer":
                    sender = SenderEnum.USER
                else:
                    sender = SenderEnum.SYSTEM

                if await message_exists(db, chat_id_db, text):
                    continue

                # Создаём сообщение
                message_in = MessageCreate(
                    chat_id=chat_id_db,
                    sender=sender,
                    text=text,
                )
                await create_message(db, message_in)

                # Если есть номер заказа
                if order_number:
                    # Получаем статус заказа через API Ozon
                    status = await get_order_status(order_number, client_id, api_key)

                    # Проверяем наличие заказа в БД
                    existing_order = await get_order(db, chat_id=chat_id_db)

                    if existing_order:
                        order_up = OrderUpdate(
                            chat_id=chat_id_db,
                            order_number=order_number,
                            status=status,
                        )
                        await update_order(db, existing_order.id, order_up)
                    else:
                        order_in = OrderCreate(
                            chat_id=chat_id_db,
                            order_number=order_number,
                            status=status,
                        )
                        await create_order(db, order_in)
