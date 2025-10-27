from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.crud.stats import (
    get_stats,
    list_stats,
    create_stats,
    update_stats,
    delete_stats,
)
from app.schemas.stats import StatsCreateUpdate, StatsOut
from app.core.db import get_db

router = APIRouter()


@router.get("/", response_model=List[StatsOut])
async def read_stats(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    stats_list = await list_stats(db, skip=skip, limit=limit)
    return stats_list


@router.get("/{stats_id}", response_model=StatsOut)
async def read_stats_item(stats_id: UUID, db: AsyncSession = Depends(get_db)):
    stats = await get_stats(db, stats_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    return stats


@router.post("/", response_model=StatsOut)
async def create_stats_item(
    payload: StatsCreateUpdate, db: AsyncSession = Depends(get_db)
):
    stats = await create_stats(db, payload)
    return stats


@router.patch("/{stats_id}", response_model=StatsOut)
async def update_stats_item(
    stats_id: UUID, payload: StatsCreateUpdate, db: AsyncSession = Depends(get_db)
):
    stats = await update_stats(db, stats_id, payload)
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    return stats


@router.delete("/{stats_id}")
async def delete_stats_item(stats_id: UUID, db: AsyncSession = Depends(get_db)):
    success = await delete_stats(db, stats_id)
    if not success:
        raise HTTPException(status_code=404, detail="Stats not found")
    return {"status": "deleted"}
