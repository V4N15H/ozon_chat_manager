from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.core.db import Base
import uuid


class Stats(Base):
    __tablename__ = "chat_stats"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    total_chats = Column(Integer, nullable=False)
    new_chats = Column(Integer, nullable=False)
    in_progress = Column(Integer, nullable=False)
    declined = Column(Integer, nullable=False)
    done = Column(Integer, nullable=False)
    error = Column(Integer, nullable=False)
    promo_sent = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
