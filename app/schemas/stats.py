from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from uuid import UUID


class ChatStatsBase(BaseModel):
    total_chats: int
    new_chats: int
    in_progress: int
    declined: int
    done: int
    error: int
    promo_sent: int


class StatsCreateUpdate(ChatStatsBase):
    pass


class StatsOut(ChatStatsBase):
    id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        model_config = ConfigDict(from_attributes=True)
