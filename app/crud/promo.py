from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.promo import Promo
from app.schemas.promo import PromoCreate, PromoUpdate


async def get_promo(db: AsyncSession, promo_id: UUID) -> Promo | None:
    result = await db.execute(select(Promo).where(Promo.id == promo_id))
    return result.scalar_one_or_none()


async def list_promos(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Promo]:
    result = await db.execute(select(Promo).offset(skip).limit(limit))
    return result.scalars().all()


async def create_promo(db: AsyncSession, obj_in: PromoCreate) -> Promo:
    promo = Promo(
        code=obj_in.code,
        valid_until=obj_in.valid_until,
    )
    db.add(promo)
    await db.commit()
    await db.refresh(promo)
    return promo


async def update_promo(
    db: AsyncSession, promo_id: UUID, obj_in: PromoUpdate
) -> Promo | None:
    promo = await get_promo(db, promo_id)
    if not promo:
        return None
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(promo, field, value)
    await db.commit()
    await db.refresh(promo)
    return promo


async def delete_promo(db: AsyncSession, promo_id: UUID) -> bool:
    promo = await get_promo(db, promo_id)
    if not promo:
        return False
    await db.delete(promo)
    await db.commit()
    return True
