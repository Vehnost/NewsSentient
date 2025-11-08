"""Unit tests for Sentient News Agent."""
import pytest
import asyncio
from datetime import datetime

from agent import SentientNewsAgent
from models import AgentRequest, NewsArticle
from news_sources import NewsAggregator


@pytest.fixture
async def agent():
    """Create agent instance for testing."""
    agent = SentientNewsAgent()
    yield agent
    await agent.close()


@pytest.fixture
async def aggregator():
    """Create aggregator instance for testing."""
    agg = NewsAggregator()
    yield agg
    await agg.close()


class TestNewsAggregator:
    """Test NewsAggregator class."""
    
    @pytest.mark.asyncio
    async def test_fetch_rss_feed(self, aggregator):
        """Test RSS feed fetching."""
        feed_url = "https://techcrunch.com/feed/"
        articles = await aggregator.fetch_rss_feed(feed_url)
        
        assert isinstance(articles, list)
        if articles:  # May be empty if network issues
            assert isinstance(articles[0], NewsArticle)
            assert articles[0].title
            assert articles[0].url
    
    @pytest.mark.asyncio
    async def test_fetch_news_by_category(self, aggregator):
        """Test news fetching by category."""
        articles = await aggregator.fetch_news_by_category("technology", max_results=5)
        
        assert isinstance(articles, list)
        assert len(articles) <= 5
    
    @pytest.mark.asyncio
    async def test_search_news(self, aggregator):
        """Test news search with keywords."""
        articles = await aggregator.search_news(
            keywords=["AI", "machine learning"],
            categories=["technology"],
            max_results=5
        )
        
        assert isinstance(articles, list)
        assert len(articles) <= 5


class TestSentientNewsAgent:
    """Test SentientNewsAgent class."""
    
    def test_extract_intent(self, agent):
        """Test intent extraction from message."""
        message = "Show me latest AI and crypto news"
        intent = agent._extract_intent(message)
        
        assert "keywords" in intent
        assert "categories" in intent
        assert isinstance(intent["categories"], list)
        assert "ai" in intent["categories"] or "crypto" in intent["categories"]
    
    def test_format_article_summary(self, agent):
        """Test article formatting."""
        article = NewsArticle(
            title="Test Article",
            description="This is a test article",
            url="https://example.com",
            source="Test Source",
            published_at=datetime.now()
        )
        
        summary = agent._format_article_summary(article)
        
        assert "Test Article" in summary
        assert "Test Source" in summary
        assert "https://example.com" in summary
    
    def test_format_time_ago(self, agent):
        """Test time formatting."""
        now = datetime.now()
        
        # Just now
        time_str = agent._format_time_ago(now)
        assert "just now" in time_str or "minute" in time_str
    
    @pytest.mark.asyncio
    async def test_process_request(self, agent):
        """Test non-streaming request processing."""
        request = AgentRequest(
            message="Show me tech news",
            stream=False
        )
        
        response = await agent.process_request(request)
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    @pytest.mark.asyncio
    async def test_process_request_stream(self, agent):
        """Test streaming request processing."""
        request = AgentRequest(
            message="Latest AI news",
            stream=True
        )
        
        events = []
        async for response in agent.process_request_stream(request):
            events.append(response)
        
        assert len(events) > 0
        
        # Check for expected event types
        event_types = [e.type for e in events]
        assert "thinking" in event_types
        assert "complete" in event_types or "error" in event_types
    
    def test_get_capabilities(self, agent):
        """Test capabilities retrieval."""
        capabilities = agent.get_capabilities()
        
        assert capabilities.name
        assert capabilities.version
        assert len(capabilities.capabilities) > 0
        assert capabilities.streaming_supported


@pytest.mark.asyncio
async def test_agent_lifecycle():
    """Test agent initialization and cleanup."""
    agent = SentientNewsAgent()
    
    # Test agent is initialized
    assert agent.aggregator is not None
    assert agent.capabilities is not None
    
    # Test cleanup
    await agent.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
