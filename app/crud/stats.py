from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.stats import Stats
from app.schemas.stats import StatsCreateUpdate


async def get_stats(db: AsyncSession, stats_id: UUID) -> Stats | None:
    result = await db.execute(select(Stats).where(Stats.id == stats_id))
    return result.scalar_one_or_none()


async def list_stats(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Stats]:
    result = await db.execute(select(Stats).offset(skip).limit(limit))
    return result.scalars().all()


async def create_stats(db: AsyncSession, obj_in: StatsCreateUpdate) -> Stats:
    stats = Stats(**obj_in.dict())
    db.add(stats)
    await db.commit()
    await db.refresh(stats)
    return stats


async def update_stats(
    db: AsyncSession, stats_id: UUID, obj_in: StatsCreateUpdate
) -> Stats | None:
    stats = await get_stats(db, stats_id)
    if not stats:
        return None
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(stats, field, value)
    await db.commit()
    await db.refresh(stats)
    return stats


async def delete_stats(db: AsyncSession, stats_id: UUID) -> bool:
    stats = await get_stats(db, stats_id)
    if not stats:
        return False
    await db.delete(stats)
    await db.commit()
    return True
