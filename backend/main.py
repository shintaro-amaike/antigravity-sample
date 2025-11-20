from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import NewsCrawler, LLMSummarizer
from database import db
from models import NewsItem, LikeRequest
from typing import List

app = FastAPI()

# CORS setup
origins = [
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crawler = NewsCrawler()
summarizer = LLMSummarizer()

@app.on_event("startup")
async def startup_event():
    # Initial crawl on startup
    news_data = await crawler.crawl()
    for item in news_data:
        summary = await summarizer.summarize(item.content)
        db.add_news(item.title, summary, item.url)

@app.get("/news", response_model=List[NewsItem])
async def get_news():
    return db.get_all_news()

@app.post("/like")
async def like_news(request: LikeRequest):
    return db.increment_like(request.id)
