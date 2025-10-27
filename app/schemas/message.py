from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID


class SenderEnum(str, Enum):
    USER = "user"
    SYSTEM = "system"
    MANAGER = "manager"


class MessageBase(BaseModel):
    chat_id: UUID
    sender: SenderEnum
    text: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    text: str | None = None
    sender: SenderEnum | None = None


class MessageOut(MessageBase):
    id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        model_config = ConfigDict(from_attributes=True)
