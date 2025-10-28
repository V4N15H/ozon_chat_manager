import httpx
from app.crud.chat import create_chat, get_chat, update_chat, list_chats
from app.schemas.chat import ChatCreate, ChatUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta



# Сбор user id для записи в chats
async def fetch_user_id(
    client: httpx.AsyncClient, client_id: str, api_key: str, chat_id: str
) -> str:
    url = "https://api-seller.ozon.ru/v3/chat/history"
    headers = {
        "Host": "api-seller.ozon.ru",
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }
    json_payload = {
        "chat_id": chat_id,
        "limit": 1,
    }  # получаем только одно последнее сообщение
    response = await client.post(url, headers=headers, json=json_payload)
    response.raise_for_status()
    data = response.json()
    messages = data.get("messages", [])
    if messages:
        user = messages[0].get("user", {})
        return user.get("id", "")
    return ""


# функция сборки чатов
async def fetch_and_save_chats(
    db: AsyncSession, client_id: str, api_key: str, limit: int = 100
):
    chat_init = await list_chats(db)
    url = "https://api-seller.ozon.ru/v3/chat/list"
    headers = {
        "Host": "api-seller.ozon.ru",
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }
    filter_conditions = {}
    # фильтр по статусу при последующем парсинге
    if chat_init:
        filter_conditions = {
            "chat_status": "Opened",
        }
    cursor = None
    chat_expire_limit = datetime.now(timezone.utc) - timedelta(days=5)

    async with httpx.AsyncClient() as client:
        # пагинация по параметрам cursor и has_next
        while True:
            json_payload = {
                "limit": limit,
                "filter": filter_conditions
            }
            if cursor:
                json_payload["cursor"] = cursor

            response = await client.post(url, headers=headers, json=json_payload)
            response.raise_for_status()
            data = response.json()

            chats = data.get("chats", [])
            has_next = data.get("has_next") == "true"
            cursor = data.get("cursor")

            if not chats:
                break

            for chat in chats:
                chat_info = chat.get("chat", {})
                chat_id = chat_info.get("chat_id")
                created_at = chat_info.get("created_at")

                # проверка чата на попадание во временые рамки
                if created_at:
                    created_date = datetime.fromisoformat(created_at.rstrip("Z")).replace(tzinfo=timezone.utc)
                    if chat_init and created_date < chat_expire_limit:
                        continue

                user_id = await fetch_user_id(client, client_id, api_key, chat_id)
                chat_in = ChatCreate(
                    ozon_chat_id=chat_id,
                    user_id=user_id,
                )
                # проверка чатов на наличие в бд
                existing_chat = await get_chat(db, ozon_chat_id=chat_id)
                if existing_chat:
                    chat_up = ChatUpdate(
                        ozon_chat_id=chat_id,
                        user_id=user_id,
                    )
                    await update_chat(db, existing_chat.id, chat_up)
                else:
                    await create_chat(db, chat_in)

            if not has_next:
                break
