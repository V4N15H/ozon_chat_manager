from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.crud.promo import (
    get_promo,
    list_promos,
    create_promo,
    update_promo,
    delete_promo,
)
from app.schemas.promo import PromoCreate, PromoOut, PromoUpdate
from app.core.db import get_db

router = APIRouter()


@router.get("/", response_model=List[PromoOut])
async def read_promos(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    promos = await list_promos(db, skip=skip, limit=limit)
    return promos


@router.get("/{promo_id}", response_model=PromoOut)
async def read_promo(promo_id: UUID, db: AsyncSession = Depends(get_db)):
    promo = await get_promo(db, promo_id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return promo


@router.post("/", response_model=PromoOut)
async def create_promo_endpoint(
    payload: PromoCreate, db: AsyncSession = Depends(get_db)
):
    promo = await create_promo(db, payload)
    return promo


@router.patch("/{promo_id}", response_model=PromoOut)
async def update_promo_endpoint(
    promo_id: UUID, payload: PromoUpdate, db: AsyncSession = Depends(get_db)
):
    promo = await update_promo(db, promo_id, payload)
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return promo


@router.delete("/{promo_id}")
async def delete_promo_endpoint(promo_id: UUID, db: AsyncSession = Depends(get_db)):
    success = await delete_promo(db, promo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return {"status": "deleted"}
