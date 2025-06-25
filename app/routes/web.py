from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.config.db import get_db
import app.controllers.tile as crud
from app.storage.minio_storage import create_minio_client

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/web/", response_class=HTMLResponse)
def home(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tiles = crud.get_tiles(db, skip=skip, limit=limit)
    tiles_data = [
        {
            "id": t.id,
            "name": t.name,
            "title": t.title,
            "src": t.src,
            "status": t.status
        }
        for t in tiles
    ]
    return templates.TemplateResponse("tiles/index.html", {"request": request, "tiles": tiles_data})

@router.get("/web/new-tile", response_class=HTMLResponse)
def new_tile(request: Request):
    return templates.TemplateResponse("tiles/new-tile.html", {"request": request, "message": "Olá FastAPI!"})

@router.get("/web/view", response_class=HTMLResponse)
def view(request: Request):
    return templates.TemplateResponse("view/index.html", {"request": request, "message": "Olá FastAPI!"})

@router.get("/web/map", response_class=HTMLResponse)
def map_view(request: Request):
    return templates.TemplateResponse("map/index.html", {"request": request, "message": "Olá FastAPI!"})

@router.get("/web/draw", response_class=HTMLResponse)
def draw_map(request: Request):
    return templates.TemplateResponse("map/draw-map.html", {"request": request, "message": "Olá FastAPI!"})

@router.get("/tiles/{tile_name}/{z}/{x}/{y}.png")
def get_tile(tile_name: str, z: int, x: int, y: int):
    TILE_BUCKET = "published-tiles"
    object_name = f"{tile_name}/{z}/{x}/{y}.png"
    print(object_name)
    try:
        minio_client = create_minio_client()
        response = minio_client.get_object(TILE_BUCKET, object_name)
        return StreamingResponse(response, media_type="image/png")
    except Exception:
        raise HTTPException(status_code=404, detail="Tile not found")
