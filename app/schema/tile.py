from pydantic import BaseModel
from enum import Enum


class TileStatus(str, Enum):
    published = "published"
    not_published = "not_published"


class TileBase(BaseModel):
    name: str
    title: str
    src: str
    status: TileStatus = TileStatus.not_published  # Valor padrão

    class Config:
        orm_mode = True


class TileCreate(TileBase):
    pass


class Tile(TileBase):
    id: int
