from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# SQLAlchemy Model
class NewsItemDB(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    summary = Column(Text)
    url = Column(String, unique=True, index=True)
    likes = Column(Integer, default=0)
    
    # New fields
    source = Column(String, index=True, nullable=True)
    published_date = Column(DateTime, nullable=True)
    image_url = Column(String, nullable=True)
    category = Column(String, index=True, nullable=True)

# Pydantic Models
class NewsItem(BaseModel):
    id: int
    title: str
    summary: str
    url: str
    likes: int
    source: Optional[str] = None
    published_date: Optional[datetime] = None
    image_url: Optional[str] = None
    category: Optional[str] = None

    class Config:
        orm_mode = True

class LikeRequest(BaseModel):
    id: int

# Auth Models
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
