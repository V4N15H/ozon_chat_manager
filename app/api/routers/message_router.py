from fastapi import APIRouter, Depends, HTTPException
from typing import List
from uuid import UUID

from app.crud.message import (
    get_message,
    list_messages,
    create_message,
    update_message,
    delete_message,
)
from app.schemas.message import MessageCreate, MessageOut, MessageUpdate
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/chats/{chat_id}/messages", response_model=List[MessageOut])
async def get_messages(
    chat_id: UUID, db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
):
    messages = await list_messages(db, chat_id=chat_id, skip=skip, limit=limit)
    return messages


@router.post("/messages", response_model=MessageOut)
async def post_message(payload: MessageCreate, db: AsyncSession = Depends(get_db)):
    message = await create_message(db, payload)
    return message


@router.get("/messages/{message_id}", response_model=MessageOut)
async def get_message_endpoint(message_id: UUID, db: AsyncSession = Depends(get_db)):
    msg = await get_message(db, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg


@router.patch("/messages/{message_id}", response_model=MessageOut)
async def update_message_endpoint(
    message_id: UUID, payload: MessageUpdate, db: AsyncSession = Depends(get_db)
):
    updated = await update_message(db, message_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated


@router.delete("/messages/{message_id}")
async def delete_message_endpoint(message_id: UUID, db: AsyncSession = Depends(get_db)):
    ok = await delete_message(db, message_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"status": "deleted"}
