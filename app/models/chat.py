from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from datetime import datetime, timezone
from app.core.db import Base


class ChatStatusEnum(str, enum.Enum):
    new = "Новый"
    in_progress = "В работе"
    declined = "Отклонён"
    done = "Готово"
    error = "Ошибка"


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    ozon_chat_id = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    status = Column(Enum(ChatStatusEnum), default=ChatStatusEnum.new, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
