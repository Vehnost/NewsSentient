"""Configuration settings for Sentient News Agent."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    news_api_key: Optional[str] = None
    newsdata_api_key: Optional[str] = None
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Agent configuration
    agent_name: str = "Daily Digest"
    agent_description: str = "AI-powered news aggregator and analyzer"
    max_news_items: int = 10
    update_interval: int = 300
    
    # Feature flags
    enable_rss: bool = True
    enable_news_api: bool = True
    enable_web_scraping: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
