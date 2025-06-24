from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.tile import Tile  # Assuming Tile is your SQLAlchemy model

# Create a new tile
async def create_tile(db: AsyncSession, tile: Tile):
    db_tile = Tile(**tile.dict())
    db.add(db_tile)
    await db.commit()
    await db.refresh(db_tile)
    return db_tile

# Get a tile by ID
async def get_tile(db: AsyncSession, tile_id: int):
    result = await db.execute(select(Tile).filter(Tile.id == tile_id))
    return result.scalars().first()

# Get all tiles
async def get_tiles(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Tile).offset(skip).limit(limit))
    return result.scalars().all()

# Update a tile
async def update_tile(db: AsyncSession, tile_id: int, name: str):
    db_tile = await get_tile(db, tile_id)
    if db_tile:
        db_tile.name = name
        await db.commit()
        await db.refresh(db_tile)
    return db_tile

# Delete a tile
async def delete_tile(db: AsyncSession, tile_id: int):
    db_tile = await get_tile(db, tile_id)
    if db_tile:
        await db.delete(db_tile)
        await db.commit()
    return db_tile