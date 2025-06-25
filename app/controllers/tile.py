from sqlalchemy.orm import Session
from app.models.tile import Tile  # SQLAlchemy model
from app.schema.tile import Tile as TileSchema  # Pydantic schema

# Create a new tile
def create_tile(db: Session, tile: TileSchema):
    db_tile = Tile(**tile.dict())
    db.add(db_tile)
    db.commit()
    db.refresh(db_tile)
    return db_tile

# Get a tile by ID
def get_tile(db: Session, tile_id: int):
    return db.query(Tile).filter(Tile.id == tile_id).first()

# Get all tiles
def get_tiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tile).offset(skip).limit(limit).all()

# Update a tile
def update_tile(db: Session, tile_id: int, name: str):
    db_tile = get_tile(db, tile_id)
    if db_tile:
        db_tile.name = name
        db.commit()
        db.refresh(db_tile)
    return db_tile

# Delete a tile
def delete_tile(db: Session, tile_id: int):
    db_tile = get_tile(db, tile_id)
    if db_tile:
        db.delete(db_tile)
        db.commit()
    return db_tile
