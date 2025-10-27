from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.chat import get_chat, update_chat
from app.schemas.chat import ChatUpdate
from app.schemas.chat import ChatStatusEnum


async def update_chat_status(db: AsyncSession, chat_id, new_status: ChatStatusEnum):
    chat = await get_chat(db, chat_id=chat_id)

    if not chat:
        raise ValueError(f"Чат с ID {chat_id} не найден")

    chat_up = ChatUpdate(
                    status = new_status.value,
                )
    await update_chat(db, chat_id, chat_up)

