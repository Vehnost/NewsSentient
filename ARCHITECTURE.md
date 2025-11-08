# 🏗️ Architecture Overview

Technical architecture of the Sentient News Agent.

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Web Client   │  │ Python Client│  │ Sentient Chat│ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                    ┌────────▼────────┐
                    │   API Gateway   │
                    │   (FastAPI)     │
                    └────────┬────────┘
                             │
          ┌──────────────────┴──────────────────┐
          │                                     │
  ┌───────▼────────┐                  ┌────────▼────────┐
  │ Sentient Agent │                  │  API Endpoints  │
  │   Core Logic   │                  │ /chat /health   │
  └───────┬────────┘                  └─────────────────┘
          │
  ┌───────▼────────────────────┐
  │   News Aggregator          │
  │                            │
  │  ┌──────┐  ┌──────┐       │
  │  │ RSS  │  │ API  │       │
  │  └──────┘  └──────┘       │
  └────────────────────────────┘
```

## 🔧 Component Breakdown

### 1. API Layer (`main.py`)

**Responsibilities:**
- HTTP request handling
- Route management
- Middleware (CORS, error handling)
- Streaming response management
- Lifecycle management

**Key Endpoints:**
- `GET /` - Service info
- `GET /capabilities` - Agent capabilities
- `POST /v1/chat` - Non-streaming chat
- `POST /v1/chat/stream` - Streaming chat (SSE)
- `POST /v1/query/news` - Direct news query
- `GET /v1/categories` - Available categories
- `GET /health` - Health check

**Technologies:**
- FastAPI - Web framework
- Uvicorn - ASGI server
- Pydantic - Data validation

### 2. Agent Core (`agent.py`)

**Responsibilities:**
- Request interpretation
- Intent extraction
- Response orchestration
- Streaming event generation
- Content formatting

**Key Methods:**
```python
class SentientNewsAgent:
    _extract_intent()           # Parse user intent
    process_request()           # Non-streaming processing
    process_request_stream()    # Streaming processing
    get_capabilities()          # Return agent info
```

**Event Flow:**
1. **Thinking** - "Analyzing request..."
2. **Searching** - "Searching for news..."
3. **Analyzing** - "Processing results..."
4. **Content** - Stream article summaries
5. **Data** - Send structured data
6. **Complete** - Signal completion

### 3. News Aggregator (`news_sources.py`)

**Responsibilities:**
- Multi-source news fetching
- RSS feed parsing
- API integration (NewsAPI, etc.)
- Deduplication
- Result sorting and filtering

**Data Sources:**
```python
RSS_FEEDS = {
    "technology": [...],
    "crypto": [...],
    "finance": [...],
    "ai": [...],
    "general": [...]
}
```

**Key Methods:**
```python
class NewsAggregator:
    fetch_rss_feed()            # Fetch from RSS
    fetch_news_api()            # Fetch from NewsAPI
    fetch_news_by_category()    # Category-based search
    search_news()               # Keyword search
```

### 4. Data Models (`models.py`)

**Core Models:**

```python
# Request/Response
AgentRequest          # User request
AgentResponse         # Agent response
AgentThinking         # Thinking step

# News
NewsArticle           # Article data
NewsQuery             # Search parameters

# Metadata
AgentCapabilities     # Agent info
ConversationContext   # Cross-agent context
```

**Model Hierarchy:**
```
AgentRequest
├── message: str
├── conversation_history: List[Message]
├── context: List[ConversationContext]
└── stream: bool

AgentResponse
├── type: str (thinking|content|data|complete|error)
├── content: Optional[str]
├── data: Optional[Dict]
└── thinking: Optional[AgentThinking]

NewsArticle
├── title: str
├── description: str
├── url: str
├── source: str
├── published_at: datetime
└── author: Optional[str]
```

### 5. Configuration (`config.py`)

**Responsibilities:**
- Environment variable management
- Settings validation
- Feature flags

**Settings:**
```python
class Settings:
    # API Keys
    openai_api_key
    news_api_key
    
    # Server
    host, port, debug
    
    # Agent
    agent_name, max_news_items
    
    # Features
    enable_rss, enable_news_api
```

## 🔄 Request Flow

### Non-Streaming Flow

```
User Request
    ↓
FastAPI Endpoint (/v1/chat)
    ↓
agent.process_request()
    ↓
├─ Extract intent
├─ Search news
│   ↓
│   NewsAggregator.search_news()
│   ├─ fetch_rss_feed()
│   ├─ fetch_news_api()
│   └─ Deduplicate & sort
│
├─ Format response
└─ Return complete response
    ↓
JSON Response to Client
```

### Streaming Flow (SSE)

```
User Request
    ↓
FastAPI Endpoint (/v1/chat/stream)
    ↓
agent.process_request_stream()
    ↓
Event Generator
├─ Emit: thinking (analyzing)
├─ Extract intent
├─ Emit: thinking (searching)
├─ Search news
├─ Emit: thinking (analyzing)
├─ Process results
├─ Emit: content (intro)
├─ For each article:
│   └─ Emit: content (article)
├─ Emit: data (structured)
└─ Emit: complete
    ↓
SSE Stream to Client
```

## 📦 Data Flow

### News Fetching Pipeline

```
1. User Query
   "Show me AI news"
   
2. Intent Extraction
   {
     keywords: ["AI"],
     categories: ["ai", "technology"],
     max_results: 10
   }
   
3. Multi-Source Fetch
   ├─ RSS Feeds (parallel)
   │  ├─ TechCrunch AI
   │  ├─ AI News
   │  └─ Wired AI
   │
   └─ NewsAPI (if enabled)
      └─ Search: "AI"
   
4. Aggregation
   ├─ Combine results
   ├─ Remove duplicates (by URL)
   └─ Sort by date
   
5. Filtering
   ├─ Keyword matching
   └─ Limit to max_results
   
6. Response
   └─ Format & stream
```

## 🧩 Integration Points

### Sentient Chat Integration

```
Sentient Chat
    ↓
HTTP POST /v1/chat/stream
    ↓
{
  "message": "Latest news",
  "stream": true,
  "context": [
    {
      "agent_id": "other_agent",
      "messages": [...]
    }
  ]
}
    ↓
Streaming Response (SSE)
```

### External APIs

```
News Sources:
├─ RSS Feeds (feedparser)
│  └─ Parse XML/RSS
│
├─ NewsAPI.org (httpx)
│  └─ REST API
│
└─ Future: Web Scraping
   └─ BeautifulSoup
```

## 🔐 Security Layers

```
Request
    ↓
CORS Middleware
    ↓
Rate Limiting (future)
    ↓
Request Validation (Pydantic)
    ↓
Business Logic
    ↓
API Key Protection
    ↓
Response Sanitization
    ↓
Response
```

## 🚀 Scalability Considerations

### Current Architecture
- Single process
- Async I/O (asyncio)
- Connection pooling (httpx)

### Scaling Strategy

**Horizontal Scaling:**
```
Load Balancer
    ↓
├─ Agent Instance 1
├─ Agent Instance 2
└─ Agent Instance N
```

**Vertical Scaling:**
- Increase workers: `uvicorn main:app --workers 4`
- Optimize connection pooling
- Add caching layer (Redis)

**Optimization Points:**
1. **Caching**
   - Cache news results (5-15 min TTL)
   - Cache RSS feeds
   - Cache API responses

2. **Connection Pooling**
   - Reuse HTTP connections
   - Configure limits

3. **Async Processing**
   - Parallel news fetching
   - Non-blocking I/O

## 📈 Monitoring & Observability

### Metrics to Track
- Request rate
- Response time
- Error rate
- News source availability
- Cache hit rate

### Logging Strategy
```
loguru
├─ INFO: Request/Response
├─ WARNING: Source failures
├─ ERROR: Critical errors
└─ DEBUG: Detailed traces
```

## 🔮 Future Enhancements

1. **AI Integration**
   - OpenAI for summarization
   - Sentiment analysis
   - Topic extraction

2. **Caching Layer**
   - Redis for news caching
   - Reduce API calls

3. **Database**
   - PostgreSQL for history
   - User preferences
   - Analytics

4. **Queue System**
   - Celery for background tasks
   - Scheduled news updates

5. **WebSocket Support**
   - Real-time updates
   - Bidirectional communication

---

**Architecture Version:** 1.0.0
**Last Updated:** 2024
