from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db import get_db
import app.controllers.tile as crud
from app.storage.minio_storage import create_minio_client
from fastapi.responses import StreamingResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/web/", response_class=HTMLResponse)
async def home(request: Request, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    tiles = await crud.get_tiles(db, skip=skip, limit=limit)
    return templates.TemplateResponse("tiles/index.html", {"request": request, "tiles": tiles})

@router.get("/web/new-tile", response_class=HTMLResponse)
async def new_tile(request: Request):
    return templates.TemplateResponse("tiles/new-tile.html", {"request": request, "message": "Olá FastAPI!"})

@router.get("/web/view", response_class=HTMLResponse)
async def view(request: Request):
    return templates.TemplateResponse("view/index.html", {"request": request, "message": "Olá FastAPI!"})

@router.get("/web/map", response_class=HTMLResponse)
async def view(request: Request):
    return templates.TemplateResponse("map/index.html", {"request": request, "message": "Olá FastAPI!"})

@router.get("/tiles/{z}/{x}/{y}.png")
def get_tile(z: int, x: int, y: int):
  TILE_BUCKET = "tiles-bucket"
  object_name = f"tiles/meu_raster/{z}/{x}/{y}.png"
  print(object_name)
  minio_client = create_minio_client()
  response = minio_client.get_object(TILE_BUCKET, object_name)
  return StreamingResponse(response, media_type="image/png")
  # try:
  #     response = minio_client.get_object(TILE_BUCKET, object_name)
  #     return StreamingResponse(response, media_type="image/png")
  # except Exception:
  #     raise HTTPException(status_code=404, detail="Tile not found")