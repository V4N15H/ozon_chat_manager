from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID


class StatusEnum(str, Enum):
    CREATED = "created"
    RECEIVED = "received"
    CANCELLED = "cancelled"


class OrderBase(BaseModel):
    chat_id: UUID
    order_number: str
    status: StatusEnum = StatusEnum.CREATED


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: StatusEnum | None = None


class OrderOut(OrderBase):
    id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        model_config = ConfigDict(from_attributes=True)
