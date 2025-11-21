from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import services
import models
import database

app = FastAPI()

# CORS setup
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

crawler = services.NewsCrawler()
summarizer = services.LLMSummarizer()

@app.on_event("startup")
async def startup_event():
    # Create tables
    database.Base.metadata.create_all(bind=database.engine)
    
    # Initial crawl on startup (if DB is empty or for demo purposes)
    db = database.SessionLocal()
    try:
        # Check if we already have news to avoid duplicate crawling on every restart for this demo
        # In a real app, you'd have a background task or scheduler.
        if db.query(models.NewsItemDB).count() == 0:
            print("Crawling news...")
            news_data = await crawler.crawl()
            for item in news_data:
                # Check if URL exists
                existing = db.query(models.NewsItemDB).filter(models.NewsItemDB.url == item.url).first()
                if not existing:
                    print(f"Summarizing: {item.title}")
                    summary = await summarizer.summarize(item.content)
                    db_item = models.NewsItemDB(
                        title=item.title,
                        summary=summary,
                        url=item.url
                    )
                    db.add(db_item)
            db.commit()
            print("Crawl finished.")
    finally:
        db.close()

@app.get("/news", response_model=List[models.NewsItem])
async def get_news(db: Session = Depends(get_db)):
    return db.query(models.NewsItemDB).all()

@app.post("/like")
async def like_news(request: models.LikeRequest, db: Session = Depends(get_db)):
    item = db.query(models.NewsItemDB).filter(models.NewsItemDB.id == request.id).first()
    if item:
        item.likes += 1
        db.commit()
        db.refresh(item)
        return item
    raise HTTPException(status_code=404, detail="News item not found")

@app.post("/crawl")
async def trigger_crawl(db: Session = Depends(get_db)):
    print("Manual crawl triggered...")
    news_data = await crawler.crawl()
    added_count = 0
    
    for item in news_data:
        if added_count >= 10:
            break
            
        # Check if URL exists
        existing = db.query(models.NewsItemDB).filter(models.NewsItemDB.url == item.url).first()
        if not existing:
            print(f"Summarizing: {item.title}")
            summary = await summarizer.summarize(item.content)
            db_item = models.NewsItemDB(
                title=item.title,
                summary=summary,
                url=item.url
            )
            db.add(db_item)
            added_count += 1
            
    db.commit()
    return {"message": f"Crawl finished. Added {added_count} new items."}
