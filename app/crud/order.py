from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.order import Order
from datetime import datetime, timezone
from app.schemas.order import OrderCreate, OrderUpdate


async def get_order(
    db: AsyncSession, order_id: UUID | None = None, chat_id: UUID | None = None
) -> Order | None:
    query = select(Order)
    if chat_id and order_id:
        query = query.where(or_(Order.id == order_id, Order.chat_id == chat_id))
    elif order_id:
        query = query.where(Order.id == order_id)
    elif chat_id:
        query = query.where(Order.chat_id == chat_id)
    else:
        return None  # или выбросить исключение

    result = await db.execute(query)
    return result.scalar_one_or_none()


async def list_orders(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Order]:
    result = await db.execute(select(Order).offset(skip).limit(limit))
    return result.scalars().all()


async def create_order(db: AsyncSession, obj_in: OrderCreate) -> Order:
    order = Order(
        chat_id=obj_in.chat_id,
        order_number=obj_in.order_number,
        status=obj_in.status,
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def update_order(
    db: AsyncSession, order_id: UUID, obj_in: OrderUpdate
) -> Order | None:
    order = await get_order(db, order_id)
    if not order:
        return None
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    await db.commit()
    await db.refresh(order)
    return order


async def delete_order(db: AsyncSession, order_id: UUID) -> bool:
    order = await get_order(db, order_id)
    if not order:
        return False
    await db.delete(order)
    await db.commit()
    return True
