import httpx
from app.crud.chat import create_chat, get_chat, update_chat
from app.schemas.chat import ChatCreate, ChatUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


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
    url = "https://api-seller.ozon.ru/v3/chat/list"
    headers = {
        "Host": "api-seller.ozon.ru",
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }
    json_payload = {"limit": limit}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json_payload)
        response.raise_for_status()
        data = response.json()
        chats = data.get("chats", [])
        for chat in chats:
            chat_id = chat.get("chat", {}).get("chat_id")
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
