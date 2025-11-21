from sqlalchemy import Column, Integer, String, Text
from database import Base
from pydantic import BaseModel

# SQLAlchemy Model
class NewsItemDB(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    summary = Column(Text)
    url = Column(String, unique=True, index=True)
    likes = Column(Integer, default=0)

# Pydantic Models
class NewsItem(BaseModel):
    id: int
    title: str
    summary: str
    url: str
    likes: int

    class Config:
        orm_mode = True

class LikeRequest(BaseModel):
    id: int
