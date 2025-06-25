from contextlib import asynccontextmanager
from app.routes.rest import publish, tiles
from app.routes.web import web
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends
from app.config.db import get_db
from app.routes.rest import collect
import os

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root():
    return {"MapCrafter": "Ok"}


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
    

# Include routers
app.include_router(tiles.router)
app.include_router(web.router)
app.include_router(publish.router)
app.include_router(collect.router)