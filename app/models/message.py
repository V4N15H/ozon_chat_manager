from sqlalchemy import Column, Enum, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
import uuid
from datetime import datetime, timezone
from app.core.db import Base


class SenderEnum(str, enum.Enum):
    user = "user"
    system = "system"
    manager = "manager"


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    chat_id = Column(
        UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False, index=True
    )
    sender = Column(Enum(SenderEnum), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    # chat = relationship("Chat", back_populates="messages")
