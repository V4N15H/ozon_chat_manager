from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageUpdate


async def get_message(db: AsyncSession, message_id: UUID) -> Message | None:
    result = await db.execute(select(Message).where(Message.id == message_id))
    return result.scalar_one_or_none()


async def list_messages(
    db: AsyncSession, chat_id: UUID, skip: int = 0, limit: int = 1000
) -> List[Message]:
    result = await db.execute(
        select(Message).where(Message.chat_id == chat_id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_message(db: AsyncSession, obj_in: MessageCreate) -> Message:
    message = Message(
        chat_id=obj_in.chat_id,
        sender=obj_in.sender,
        text=obj_in.text,
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def update_message(
    db: AsyncSession, message_id: UUID, obj_in: MessageUpdate
) -> Message | None:
    existing = await get_message(db, message_id)
    if not existing:
        return None
    data = obj_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(existing, field, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_message(db: AsyncSession, message_id: UUID) -> bool:
    existing = await get_message(db, message_id)
    if not existing:
        return False
    await db.delete(existing)
    await db.commit()
    return True
