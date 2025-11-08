"""Sentient News Agent - AI-powered news aggregator."""
import asyncio
from typing import AsyncGenerator, List, Dict, Any, Optional
from datetime import datetime
from loguru import logger

from models import (
    AgentRequest, AgentResponse, AgentThinking, 
    NewsArticle, AgentCapabilities
)
from news_sources import NewsAggregator
from config import settings


class SentientNewsAgent:
    """
    Sentient News Agent that aggregates and analyzes news from multiple sources.
    
    This agent follows Sentient API standards and provides streaming responses
    with intermediate events for better UX.
    """
    
    def __init__(self):
        self.aggregator = NewsAggregator()
        self.capabilities = AgentCapabilities(
            name=settings.agent_name,
            description=settings.agent_description,
            version="1.0.0",
            capabilities=[
                "news_aggregation",
                "multi_source_search",
                "category_filtering",
                "real_time_updates",
                "context_aware_analysis"
            ],
            supported_languages=["en", "ru"],
            max_context_length=8000,
            streaming_supported=True
        )
    
    async def close(self):
        """Cleanup resources."""
        await self.aggregator.close()
    
    def _extract_intent(self, message: str) -> Dict[str, Any]:
        """
        Extract user intent from message.
        
        Returns:
            Dict with query parameters (keywords, categories, etc.)
        """
        message_lower = message.lower()
        
        # Detect categories
        categories = []
        category_keywords = {
            "technology": ["tech", "technology", "gadget", "software", "hardware"],
            "crypto": ["crypto", "bitcoin", "ethereum", "blockchain", "defi", "web3"],
            "finance": ["finance", "stock", "market", "trading", "investment", "economy"],
            "ai": ["ai", "artificial intelligence", "machine learning", "llm", "gpt"],
            "general": ["news", "latest", "today", "recent", "world"]
        }
        
        for category, keywords in category_keywords.items():
            if any(kw in message_lower for kw in keywords):
                categories.append(category)
        
        if not categories:
            categories = ["general"]
        
        # Extract keywords (simple implementation)
        words = message.split()
        keywords = [w for w in words if len(w) > 3 and w.lower() not in 
                   ["what", "news", "about", "latest", "show", "find", "give"]]
        
        return {
            "keywords": keywords[:5],  # Limit to 5 keywords
            "categories": categories,
            "max_results": settings.max_news_items
        }
    
    def _format_article_summary(self, article: NewsArticle) -> str:
        """Format article for display."""
        time_ago = self._format_time_ago(article.published_at)
        
        summary = f"**{article.title}**\n"
        summary += f"*{article.source}* • {time_ago}\n"
        if article.description:
            summary += f"{article.description[:200]}...\n"
        summary += f"🔗 [Read more]({article.url})\n"
        
        return summary
    
    def _format_time_ago(self, dt: datetime) -> str:
        """Format datetime as 'X hours ago'."""
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
        delta = now - dt
        
        if delta.days > 0:
            return f"{delta.days} day{'s' if delta.days != 1 else ''} ago"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "just now"
    
    async def _stream_thinking(
        self, 
        thinking_type: str, 
        content: str
    ) -> AgentResponse:
        """Create a thinking event."""
        return AgentResponse(
            type="thinking",
            thinking=AgentThinking(
                type=thinking_type,
                content=content
            )
        )
    
    async def _stream_content(self, content: str) -> AgentResponse:
        """Create a content event."""
        return AgentResponse(
            type="content",
            content=content
        )
    
    async def _stream_data(self, data: Dict[str, Any]) -> AgentResponse:
        """Create a data event."""
        return AgentResponse(
            type="data",
            data=data
        )
    
    async def process_request_stream(
        self, 
        request: AgentRequest
    ) -> AsyncGenerator[AgentResponse, None]:
        """
        Process agent request with streaming responses.
        
        This method follows Sentient API standards by emitting intermediate
        events (thinking, searching, analyzing) before the final response.
        """
        try:
            # Step 1: Thinking - Understanding the request
            yield await self._stream_thinking(
                "thinking",
                "Analyzing your request and identifying news topics..."
            )
            await asyncio.sleep(0.3)  # Small delay for UX
            
            # Extract intent
            intent = self._extract_intent(request.message)
            logger.info(f"Extracted intent: {intent}")
            
            # Step 2: Searching
            search_desc = f"Searching for news about: {', '.join(intent['categories'])}"
            if intent['keywords']:
                search_desc += f" (keywords: {', '.join(intent['keywords'])})"
            
            yield await self._stream_thinking(
                "searching",
                search_desc
            )
            
            # Fetch news
            articles = await self.aggregator.search_news(
                keywords=intent['keywords'],
                categories=intent['categories'],
                max_results=intent['max_results']
            )
            
            if not articles:
                yield await self._stream_content(
                    "I couldn't find any recent news matching your request. "
                    "Try different keywords or categories."
                )
                yield AgentResponse(type="complete")
                return
            
            # Step 3: Analyzing
            yield await self._stream_thinking(
                "analyzing",
                f"Found {len(articles)} articles. Analyzing relevance and preparing summary..."
            )
            await asyncio.sleep(0.3)
            
            # Step 4: Streaming content
            intro = f"📰 Found **{len(articles)}** recent articles:\n\n"
            yield await self._stream_content(intro)
            
            # Stream articles one by one
            for i, article in enumerate(articles, 1):
                article_text = f"**{i}.** {self._format_article_summary(article)}\n"
                yield await self._stream_content(article_text)
                await asyncio.sleep(0.1)  # Small delay between articles
            
            # Step 5: Send structured data
            yield await self._stream_data({
                "articles": [article.dict() for article in articles],
                "categories": intent['categories'],
                "total_results": len(articles)
            })
            
            # Step 6: Complete
            yield AgentResponse(type="complete")
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            yield AgentResponse(
                type="error",
                content=f"An error occurred: {str(e)}"
            )
    
    async def process_request(self, request: AgentRequest) -> str:
        """
        Process agent request without streaming (fallback).
        
        Returns complete response as a single string.
        """
        intent = self._extract_intent(request.message)
        
        articles = await self.aggregator.search_news(
            keywords=intent['keywords'],
            categories=intent['categories'],
            max_results=intent['max_results']
        )
        
        if not articles:
            return "I couldn't find any recent news matching your request."
        
        # Build response
        response = f"📰 Found **{len(articles)}** recent articles:\n\n"
        
        for i, article in enumerate(articles, 1):
            response += f"**{i}.** {self._format_article_summary(article)}\n"
        
        return response
    
    def get_capabilities(self) -> AgentCapabilities:
        """Get agent capabilities."""
        return self.capabilities
