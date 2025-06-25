from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


from .config import settings

DATABASE_URL = settings.DATABASE_URL

# Engine e sessão síncronas
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência do FastAPI para injetar sessão
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
