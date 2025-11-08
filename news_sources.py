"""News sources aggregation module."""
import asyncio
import feedparser
import httpx
from datetime import datetime, timedelta
from typing import List, Optional
from loguru import logger
from bs4 import BeautifulSoup

from models import NewsArticle
from config import settings


class NewsAggregator:
    """Aggregates news from multiple sources."""
    
    # Popular RSS feeds - Authoritative sources
    RSS_FEEDS = {
        "technology": [
            "https://techcrunch.com/feed/",
            "https://www.theverge.com/rss/index.xml",
            "https://www.wired.com/feed/rss",
            "https://arstechnica.com/feed/",
            "https://www.engadget.com/rss.xml",
            "https://www.zdnet.com/news/rss.xml",
            "https://www.techmeme.com/feed.xml",
        ],
        "crypto": [
            # Major Crypto News Sites
            "https://cointelegraph.com/rss",
            "https://cryptopotato.com/feed/",
            "https://u.today/rss.php",
            "https://decrypt.co/feed",
            "https://beincrypto.com/feed/",
            "https://cryptoslate.com/feed/",
            "https://cryptonews.com/news/feed/",
            "https://cryptobriefing.com/feed/",
            "https://ambcrypto.com/feed/",
            "https://www.coinbureau.com/feed/",
            "https://cryptodaily.co.uk/feed",
            # Mainstream covering crypto
            "https://www.forbes.com/crypto-blockchain/feed/",
            "https://cointelegraph.com/rss/tag/bitcoin",
            "https://cointelegraph.com/rss/tag/ethereum",
        ],
        "finance": [
            "https://finance.yahoo.com/news/rssindex",
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
            "https://feeds.bloomberg.com/markets/news.rss",
            "https://www.marketwatch.com/rss/",
            "https://www.investing.com/rss/news.rss",
        ],
        "ai": [
            # AI-specific sources
            "https://www.artificialintelligence-news.com/feed/",
            "https://techcrunch.com/category/artificial-intelligence/feed/",
            "https://www.theverge.com/rss/index.xml",
            "https://www.wired.com/feed/tag/ai/latest/rss",
            "https://venturebeat.com/feed/",
            "https://www.marktechpost.com/feed/",
            "https://analyticsindiamag.com/feed/",
            "https://www.unite.ai/feed/",
            "https://www.technologyreview.com/feed/",
            # Major tech sites covering AI
            "https://www.zdnet.com/topic/artificial-intelligence/rss.xml",
            "https://arstechnica.com/tag/artificial-intelligence/feed/",
        ],
        "general": [
            "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
            "https://feeds.bbci.co.uk/news/rss.xml",
            "https://www.theguardian.com/world/rss",
            "https://www.aljazeera.com/xml/rss/all.xml",
        ]
    }
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()
    
    async def fetch_rss_feed(self, url: str) -> List[NewsArticle]:
        """Fetch news from RSS feed."""
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            
            feed = feedparser.parse(response.text)
            articles = []
            
            for entry in feed.entries[:settings.max_news_items]:
                try:
                    # Parse published date
                    pub_date = datetime.now()
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                    
                    # Extract image URL
                    image_url = None
                    # Try media:content tag (common in RSS)
                    if hasattr(entry, 'media_content') and entry.media_content:
                        image_url = entry.media_content[0].get('url')
                    # Try media:thumbnail
                    elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                        image_url = entry.media_thumbnail[0].get('url')
                    # Try enclosure
                    elif hasattr(entry, 'enclosures') and entry.enclosures:
                        for enclosure in entry.enclosures:
                            if enclosure.get('type', '').startswith('image/'):
                                image_url = enclosure.get('href')
                                break
                    # Try to find image in content/description
                    if not image_url:
                        content = entry.get('content', [{}])[0].get('value', '') if hasattr(entry, 'content') else entry.get('description', '')
                        if content:
                            soup = BeautifulSoup(content, 'html.parser')
                            img = soup.find('img')
                            if img and img.get('src'):
                                image_url = img.get('src')
                    
                    article = NewsArticle(
                        title=entry.get('title', 'No title'),
                        description=entry.get('summary', entry.get('description', '')),
                        url=entry.get('link', ''),
                        source=feed.feed.get('title', 'Unknown'),
                        published_at=pub_date.isoformat(),
                        image_url=image_url
                    )
                    articles.append(article)
                except Exception as e:
                    logger.warning(f"Failed to parse RSS entry: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed {url}: {e}")
            return []
    
    async def fetch_news_api(self, query: str, category: Optional[str] = None) -> List[NewsArticle]:
        """Fetch news from NewsAPI.org."""
        if not settings.news_api_key:
            return []
        
        try:
            params = {
                "q": query,
                "apiKey": settings.news_api_key,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": settings.max_news_items
            }
            
            if category:
                params["category"] = category
            
            response = await self.client.get(
                "https://newsapi.org/v2/everything",
                params=params
            )
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for item in data.get("articles", []):
                try:
                    article = NewsArticle(
                        title=item.get("title", "No title"),
                        description=item.get("description", ""),
                        url=item.get("url", ""),
                        source=item.get("source", {}).get("name", "Unknown"),
                        published_at=datetime.fromisoformat(
                            item.get("publishedAt", "").replace("Z", "+00:00")
                        ),
                        author=item.get("author", None)
                    )
                    articles.append(article)
                except Exception as e:
                    logger.warning(f"Failed to parse NewsAPI article: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            logger.error(f"Failed to fetch from NewsAPI: {e}")
            return []
    
    async def fetch_news_by_category(
        self, 
        category: str = "general",
        max_results: int = 10
    ) -> List[NewsArticle]:
        """Fetch news from multiple sources by category."""
        articles = []
        
        # Fetch from RSS feeds
        if settings.enable_rss and category in self.RSS_FEEDS:
            feeds = self.RSS_FEEDS[category]
            tasks = [self.fetch_rss_feed(feed) for feed in feeds]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    articles.extend(result)
        
        # Fetch from NewsAPI
        if settings.enable_news_api:
            api_articles = await self.fetch_news_api(category, category)
            articles.extend(api_articles)
        
        # Sort by date and limit
        articles.sort(key=lambda x: x.published_at, reverse=True)
        return articles[:max_results]
    
    async def search_news(
        self,
        keywords: List[str],
        categories: Optional[List[str]] = None,
        max_results: int = 10
    ) -> List[NewsArticle]:
        """Search news by keywords and categories."""
        all_articles = []
        
        # Search in specified categories or all
        categories = categories or ["general", "technology", "crypto", "finance", "ai"]
        
        for category in categories:
            articles = await self.fetch_news_by_category(category, max_results)
            all_articles.extend(articles)
        
        # Filter by keywords
        if keywords:
            filtered = []
            for article in all_articles:
                text = f"{article.title} {article.description or ''}".lower()
                if any(keyword.lower() in text for keyword in keywords):
                    filtered.append(article)
            all_articles = filtered
        
        # Remove duplicates by URL
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                unique_articles.append(article)
        
        # Sort by date
        unique_articles.sort(key=lambda x: x.published_at, reverse=True)
        return unique_articles[:max_results]
