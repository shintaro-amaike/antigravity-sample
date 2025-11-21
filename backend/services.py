import os
import feedparser
import google.generativeai as genai
from typing import List
from dotenv import load_dotenv

load_dotenv()

class CrawledItem:
    def __init__(self, title: str, content: str, url: str):
        self.title = title
        self.content = content
        self.url = url

class NewsCrawler:
    def __init__(self):
        self.feed_urls = [
            "https://ledge.ai/feed",
            "https://ainow.ai/feed",
            "https://aismiley.co.jp/feed",
            "https://wired.jp/rss/index.xml",
            "https://jp.techcrunch.com/feed/",
            "https://hnrss.org/newest?q=AI" # Keep HN as a backup/global source
        ]

    async def crawl(self) -> List[CrawledItem]:
        all_items = []
        for url in self.feed_urls:
            try:
                print(f"Crawling: {url}")
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]: # Limit per feed to avoid overwhelming
                    content = ""
                    if hasattr(entry, 'summary'):
                        content = entry.summary
                    elif hasattr(entry, 'description'):
                        content = entry.description
                    
                    all_items.append(CrawledItem(
                        title=entry.title,
                        content=content,
                        url=entry.link
                    ))
            except Exception as e:
                print(f"Failed to crawl {url}: {e}")
        
        # Shuffle to mix sources
        import random
        random.shuffle(all_items)
        return all_items

class LLMSummarizer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found. Summarization will fail.")
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')

    async def summarize(self, text: str) -> str:
        if not hasattr(self, 'model'):
            return "Summarization unavailable (Missing API Key)"
        
        try:
            prompt = f"Summarize the following text in exactly 3 lines in Japanese:\n\n{text}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return "Error generating summary."
