from pydantic import BaseModel
from enum import Enum


class TileStatus(str, Enum):
    processed = "processed"
    not_processed = "not processed"


class TileBase(BaseModel):
    name: str
    title: str
    src: str
    status: TileStatus = TileStatus.not_processed  # Valor padrão

    class Config:
        orm_mode = True


class TileCreate(TileBase):
    pass


class Tile(TileBase):
    id: int
