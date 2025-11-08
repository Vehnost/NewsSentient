"""Data models for Sentient Agent API."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime


class Message(BaseModel):
    """Chat message model."""
    role: Literal["user", "assistant", "system"]
    content: str


class ConversationContext(BaseModel):
    """Conversation context from other agents."""
    agent_id: str
    messages: List[Message]
    metadata: Optional[Dict[str, Any]] = None


class AgentRequest(BaseModel):
    """Request to Sentient Agent."""
    message: str
    conversation_history: Optional[List[Message]] = Field(default_factory=list)
    context: Optional[List[ConversationContext]] = Field(default_factory=list)
    stream: bool = True
    parameters: Optional[Dict[str, Any]] = None


class NewsArticle(BaseModel):
    """News article model."""
    title: str
    description: Optional[str] = None
    url: str
    source: str
    published_at: str
    image_url: Optional[str] = None
    category: Optional[str] = None
    relevance_score: Optional[float] = None


class AgentThinking(BaseModel):
    """Agent thinking/reasoning step."""
    type: Literal["thinking", "searching", "analyzing", "summarizing"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentResponse(BaseModel):
    """Response from Sentient Agent."""
    type: Literal["thinking", "content", "data", "complete", "error"]
    content: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    thinking: Optional[AgentThinking] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentCapabilities(BaseModel):
    """Agent capabilities description."""
    name: str
    description: str
    version: str
    capabilities: List[str]
    supported_languages: List[str]
    max_context_length: int
    streaming_supported: bool


class NewsQuery(BaseModel):
    """News search query."""
    keywords: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    sources: Optional[List[str]] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    language: str = "en"
    max_results: int = 10
