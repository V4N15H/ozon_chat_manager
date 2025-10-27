from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID


class ChatStatusEnum(str, Enum):
    NEW = "Новый"
    IN_PROGRESS = "В работе"
    DECLINED = "Отклонён"
    DONE = "Готово"
    ERROR = "Ошибка"


class ChatBase(BaseModel):
    ozon_chat_id: str
    user_id: str
    status: ChatStatusEnum = ChatStatusEnum.NEW


class ChatCreate(ChatBase):
    pass


class ChatUpdate(BaseModel):
    status: ChatStatusEnum | None = None


class ChatOut(ChatBase):
    id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        model_config = ConfigDict(from_attributes=True)
