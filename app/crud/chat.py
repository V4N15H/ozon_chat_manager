from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate
from enum import Enum
from datetime import datetime, timezone

async def get_chat(
    db: AsyncSession, chat_id: UUID | None = None, ozon_chat_id: str | None = None
) -> Chat | None:
    query = select(Chat)
    if chat_id and ozon_chat_id:
        query = query.where(Chat.id == chat_id)
    elif chat_id:
        query = query.where(Chat.id == chat_id)
    elif ozon_chat_id:
        query = query.where(Chat.ozon_chat_id == ozon_chat_id)
    else:
        return None  # или выбросить исключение

    result = await db.execute(query)
    return result.scalar_one_or_none()


async def list_chats(db: AsyncSession, skip: int = 0, limit: int = 1000) -> List[Chat]:
    result = await db.execute(select(Chat).offset(skip).limit(limit))
    return result.scalars().all()


async def create_chat(db: AsyncSession, obj_in: ChatCreate) -> Chat:
    chat = Chat(
        ozon_chat_id=obj_in.ozon_chat_id,
        user_id=obj_in.user_id,
        status=obj_in.status.value if isinstance(obj_in.status, str) else obj_in.status,
    )
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


async def update_chat(
    db: AsyncSession, chat_id: UUID, obj_in: ChatUpdate
) -> Chat | None:
    existing = await get_chat(db, chat_id)
    if not existing:
        return None
    update_data = obj_in.dict(exclude_unset=True)
    if "status" in update_data and update_data["status"] is not None:
        update_data["status"] = (
            update_data["status"].value
            if isinstance(update_data["status"], Enum)
            else update_data["status"]
        )
    for field, value in update_data.items():
        setattr(existing, field, value)
    existing.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_chat(db: AsyncSession, chat_id: UUID) -> bool:
    existing = await get_chat(db, chat_id)
    if not existing:
        return False
    await db.delete(existing)
    await db.commit()
    return True


