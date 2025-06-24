from sqlalchemy import Column, Integer, String
from app.config.db import Base

class Tile(Base):
  __tablename__ = "tile"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  title = Column(String, nullable=False)
  src = Column(String, nullable=False)
  status = Column(String, nullable=False)

