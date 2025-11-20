from pydantic import BaseModel

class NewsItem(BaseModel):
    id: int
    title: str
    summary: str
    url: str
    likes: int

class LikeRequest(BaseModel):
    id: int
