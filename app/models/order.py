from sqlalchemy import Column, Enum, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.db import Base


class StatusEnum(str, enum.Enum):
    created = "created"
    received = "received"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    chat_id = Column(
        UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False, index=True
    )
    order_number = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
