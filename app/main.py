from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends
from app.config.db import get_db
from app.routes import tiles, user_interface, publish
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
app.include_router(user_interface.router)
app.include_router(publish.router)