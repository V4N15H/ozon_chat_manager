from sqlalchemy import Column, DateTime, String, Date
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.core.db import Base
import uuid


class Promo(Base):
    __tablename__ = "promo_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    valid_until = Column(Date, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
