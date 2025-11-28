import os
import feedparser
import google.generativeai as genai
from typing import List
from dotenv import load_dotenv

load_dotenv()

import urllib.robotparser
from urllib.parse import urlparse
from datetime import datetime
from time import mktime

class CrawledItem:
    def __init__(self, title: str, content: str, url: str, source: str = None, published_date: datetime = None, image_url: str = None):
        self.title = title
        self.content = content
        self.url = url
        self.source = source
        self.published_date = published_date
        self.image_url = image_url

class RobotsTxtChecker:
    def __init__(self):
        self.parsers = {}

    def is_allowed(self, target_url: str, user_agent: str = "*") -> bool:
        parsed = urlparse(target_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        if base_url not in self.parsers:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"{base_url}/robots.txt")
            try:
                rp.read()
                self.parsers[base_url] = rp
            except Exception:
                # If robots.txt fails, assume allowed (or disallowed depending on policy, here we'll be nice but permissive if error)
                return True
        
        return self.parsers[base_url].can_fetch(user_agent, target_url)

class NewsCrawler:
    def __init__(self):
        self.feed_urls = [
            "https://ledge.ai/feed",
            "https://ainow.ai/feed",
            "https://aismiley.co.jp/feed",
            "https://wired.jp/rss/index.xml",
            "https://jp.techcrunch.com/feed/",
            "https://hnrss.org/newest?q=AI"
        ]
        self.robots_checker = RobotsTxtChecker()

    async def crawl(self) -> List[CrawledItem]:
        all_items = []
        for url in self.feed_urls:
            try:
                # Check robots.txt for the feed URL itself (though feeds are usually allowed, good practice)
                if not self.robots_checker.is_allowed(url):
                    print(f"Skipping {url} due to robots.txt")
                    continue

                print(f"Crawling: {url}")
                feed = feedparser.parse(url)
                
                if feed.bozo:
                    print(f"Warning: Feed {url} has parsing errors: {feed.bozo_exception}")
                
                # Extract source name from feed title or URL
                source_name = feed.feed.get('title', urlparse(url).netloc)

                for entry in feed.entries[:5]:
                    # Check if article URL is allowed
                    if not self.robots_checker.is_allowed(entry.link):
                        continue

                    content = ""
                    if hasattr(entry, 'summary'):
                        content = entry.summary
                    elif hasattr(entry, 'description'):
                        content = entry.description
                    
                    # Extract date
                    published_date = None
                    if hasattr(entry, 'published_parsed'):
                        published_date = datetime.fromtimestamp(mktime(entry.published_parsed))
                    elif hasattr(entry, 'updated_parsed'):
                        published_date = datetime.fromtimestamp(mktime(entry.updated_parsed))
                    
                    # Extract image (basic attempt)
                    image_url = None
                    if hasattr(entry, 'media_content'):
                        image_url = entry.media_content[0]['url']
                    elif hasattr(entry, 'enclosures') and entry.enclosures:
                         image_url = entry.enclosures[0]['href']
                    
                    all_items.append(CrawledItem(
                        title=entry.title,
                        content=content,
                        url=entry.link,
                        source=source_name,
                        published_date=published_date,
                        image_url=image_url
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
        
        retries = 3
        for attempt in range(retries):
            try:
                prompt = f"Summarize the following text in exactly 3 lines in Japanese:\n\n{text}"
                response = await self.model.generate_content_async(prompt)
                return response.text
            except Exception as e:
                print(f"Error summarizing text (Attempt {attempt + 1}/{retries}): {e}")
                if attempt == retries - 1:
                    # Fallback: Return first 200 chars
                    return text[:200] + "..." if len(text) > 200 else text
                import asyncio
                await asyncio.sleep(1) # Wait before retry
        return "Error generating summary."
