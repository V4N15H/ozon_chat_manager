from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.crud.chat import get_chat, list_chats, create_chat, update_chat, delete_chat
from app.schemas.chat import ChatCreate, ChatOut, ChatUpdate
from app.core.db import get_db

router = APIRouter()


@router.get("/", response_model=list[ChatOut])
async def read_chats(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    chats = await list_chats(db, skip=skip, limit=limit)
    return chats


@router.get("/{chat_id}", response_model=ChatOut)
async def read_chat(chat_id: UUID, db: AsyncSession = Depends(get_db)):
    chat = await get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.post("/", response_model=ChatOut)
async def create_chat_endpoint(payload: ChatCreate, db: AsyncSession = Depends(get_db)):
    chat = await create_chat(db, payload)
    return chat


@router.patch("/{chat_id}/status", response_model=ChatOut)
async def update_chat_status(
    chat_id: UUID, payload: ChatCreate, db: AsyncSession = Depends(get_db)
):
    chat = await update_chat(db, chat_id, payload)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.delete("/{chat_id}")
async def delete_chat_endpoint(chat_id: UUID, db: AsyncSession = Depends(get_db)):
    ok = await delete_chat(db, chat_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"status": "deleted"}
