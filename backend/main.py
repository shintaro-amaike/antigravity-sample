from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import services
import models
import database
import auth
from datetime import timedelta

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
        if db.query(models.NewsItemDB).count() == 0:
            print("Crawling news...")
            news_data = await crawler.crawl()
            for item in news_data:
                existing = db.query(models.NewsItemDB).filter(models.NewsItemDB.url == item.url).first()
                if not existing:
                    print(f"Summarizing: {item.title}")
                    summary = await summarizer.summarize(item.content)
                    db_item = models.NewsItemDB(
                        title=item.title,
                        summary=summary,
                        url=item.url,
                        source=item.source,
                        published_date=item.published_date,
                        image_url=item.image_url
                    )
                    db.add(db_item)
            db.commit()
            print("Crawl finished.")
    finally:
        db.close()

# Auth Endpoints
@app.post("/register", response_model=models.User)
def register(user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.UserDB).filter(models.UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.UserDB(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.UserDB).filter(models.UserDB.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/news", response_model=List[models.NewsItem])
async def get_news(
    skip: int = 0, 
    limit: int = 20, 
    q: Optional[str] = None,
    source: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.NewsItemDB)
    
    if q:
        search = f"%{q}%"
        query = query.filter(
            or_(
                models.NewsItemDB.title.ilike(search),
                models.NewsItemDB.summary.ilike(search)
            )
        )
    
    if source:
        query = query.filter(models.NewsItemDB.source == source)
        
    return query.order_by(models.NewsItemDB.published_date.desc()).offset(skip).limit(limit).all()

@app.post("/like")
async def like_news(
    request: models.LikeRequest, 
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(auth.get_current_user)
):
    item = db.query(models.NewsItemDB).filter(models.NewsItemDB.id == request.id).first()
    if item:
        item.likes += 1
        db.commit()
        db.refresh(item)
        return item
    raise HTTPException(status_code=404, detail="News item not found")

@app.post("/crawl")
async def trigger_crawl(
    db: Session = Depends(get_db),
    current_user: models.UserDB = Depends(auth.get_current_user)
):
    print("Manual crawl triggered...")
    news_data = await crawler.crawl()
    added_count = 0
    
    for item in news_data:
        if added_count >= 10:
            break
            
        existing = db.query(models.NewsItemDB).filter(models.NewsItemDB.url == item.url).first()
        if not existing:
            print(f"Summarizing: {item.title}")
            summary = await summarizer.summarize(item.content)
            db_item = models.NewsItemDB(
                title=item.title,
                summary=summary,
                url=item.url,
                source=item.source,
                published_date=item.published_date,
                image_url=item.image_url
            )
            db.add(db_item)
            added_count += 1
            
    db.commit()
    return {"message": f"Crawl finished. Added {added_count} new items."}
