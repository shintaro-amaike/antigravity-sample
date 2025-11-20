from typing import List, Dict
from models import NewsItem

class Database:
    def __init__(self):
        self.news: Dict[int, NewsItem] = {}
        self.counter = 0

    def add_news(self, title: str, summary: str, url: str):
        self.counter += 1
        self.news[self.counter] = NewsItem(
            id=self.counter,
            title=title,
            summary=summary,
            url=url,
            likes=0
        )

    def get_all_news(self) -> List[NewsItem]:
        return list(self.news.values())

    def increment_like(self, news_id: int) -> NewsItem:
        if news_id in self.news:
            self.news[news_id].likes += 1
            return self.news[news_id]
        return None

db = Database()
