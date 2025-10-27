from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from uuid import UUID


class PromoBase(BaseModel):
    code: str
    valid_until: datetime


class PromoCreate(PromoBase):
    pass


class PromoUpdate(BaseModel):
    code: str
    valid_until: datetime | None = None


class PromoOut(PromoBase):
    id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        model_config = ConfigDict(from_attributes=True)
