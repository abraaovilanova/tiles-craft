from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.config.db import get_db
from app.schema.tile import Tile, TileCreate
import app.controllers.tile as crud

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

@router.post("/tiles/", response_model=Tile)
async def create_tile(tile: TileCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_tile(db=db, tile=tile)

@router.get("/tiles/{tile_id}", response_model=Tile)
async def get_tile(tile_id: int, db: AsyncSession = Depends(get_db)):
    db_tile = await crud.get_tile(db, tile_id=tile_id)
    if db_tile is None:
        raise HTTPException(status_code=404, detail="Tile not found")
    return db_tile

@router.get("/tiles/", response_model=list[Tile])
async def get_tiles(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_tiles(db, skip=skip, limit=limit)

@router.put("/tiles/{tile_id}", response_model=Tile)
async def update_tile(tile_id: int, tile: TileCreate, db: AsyncSession = Depends(get_db)):
    db_tile = await crud.update_tile(db, tile_id=tile_id, name=tile.name)
    if db_tile is None:
        raise HTTPException(status_code=404, detail="Tile not found")
    return db_tile

@router.delete("/tiles/{tile_id}", response_model=Tile)
def delete_tile(tile_id: int, db: Session = Depends(get_db)):
    db_tile = crud.delete_tile(db, tile_id=tile_id)  # ✅ CORRETO
    if db_tile is None:
        raise HTTPException(status_code=404, detail="Tile not found")
    return db_tile