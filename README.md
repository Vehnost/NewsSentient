# 🚀 CryptoNews AI

AI-powered news aggregator with intelligent chat assistant. Get the latest crypto, AI, and tech news from 40+ authoritative sources with real-time updates and smart filtering.

## 🎯 Features

- 🤖 **AI Chat Assistant** - Ask about any company or topic
- 📰 **40+ News Sources** - Crypto (14), AI (11), Tech (7), Finance (5)
- 🔥 **Real-time Updates** - Fresh news with LIVE/HOT/NEW badges
- 📸 **Image Support** - News articles with images
- 💬 **Smart Search** - Natural language queries
- 🎨 **Beautiful UI** - Modern, responsive design
- ⚡ **Fast Performance** - Optimized async fetching
- 🌊 **Streaming API** - Server-Sent Events support
- 🔍 **Smart Filtering** - By category, source, and keywords
- 📊 **Structured Data** - Clean JSON responses

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd c:\python_projects\analyzerSentient

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and add your API keys:

```bash
# API Keys (optional but recommended)
OPENAI_API_KEY=your_openai_key_here
NEWS_API_KEY=your_newsapi_key_here

# Server configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

**Note**: The agent works without API keys but with limited functionality (RSS only).

### 3. Run the Agent

```bash
# Start the server
python main.py

# Or with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

## 📡 API Endpoints

### Get Agent Capabilities
```http
GET /capabilities
```

Response:
```json
{
  "name": "Daily Digest",
  "description": "AI-powered news aggregator and analyzer",
  "version": "1.0.0",
  "capabilities": [
    "news_aggregation",
    "multi_source_search",
    "category_filtering",
    "real_time_updates"
  ],
  "streaming_supported": true
}
```

### Chat with Agent (Streaming)
```http
POST /v1/chat/stream
Content-Type: application/json

{
  "message": "Show me latest AI news",
  "stream": true
}
```

Response (Server-Sent Events):
```
data: {"type":"thinking","thinking":{"type":"thinking","content":"Analyzing request..."}}

data: {"type":"searching","thinking":{"type":"searching","content":"Searching for AI news..."}}

data: {"type":"content","content":"📰 Found 10 articles:\n\n"}

data: {"type":"complete"}
```

### Chat with Agent (Non-Streaming)
```http
POST /v1/chat
Content-Type: application/json

{
  "message": "Latest crypto news",
  "stream": false
}
```

### Direct News Query
```http
POST /v1/query/news
Content-Type: application/json

{
  "keywords": ["bitcoin", "ethereum"],
  "categories": ["crypto"],
  "max_results": 5
}
```

### Get Categories
```http
GET /v1/categories
```

## 💡 Usage Examples

### Python Client

```python
import requests
import json

# Streaming request
def stream_chat(message: str):
    url = "http://localhost:8000/v1/chat/stream"
    data = {
        "message": message,
        "stream": True
    }
    
    with requests.post(url, json=data, stream=True) as response:
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    event_data = json.loads(line[6:])
                    print(f"Event: {event_data['type']}")
                    if event_data.get('content'):
                        print(event_data['content'])

# Usage
stream_chat("Show me latest technology news")
```

### JavaScript Client

```javascript
async function streamChat(message) {
  const response = await fetch('http://localhost:8000/v1/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      stream: true
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        console.log('Event:', data.type);
        if (data.content) {
          console.log(data.content);
        }
      }
    }
  }
}

// Usage
streamChat('Latest AI news');
```

### cURL

```bash
# Streaming chat
curl -X POST http://localhost:8000/v1/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message":"Latest crypto news","stream":true}' \
  --no-buffer

# Direct news query
curl -X POST http://localhost:8000/v1/query/news \
  -H "Content-Type: application/json" \
  -d '{"keywords":["bitcoin"],"categories":["crypto"],"max_results":5}'
```

## 📂 Project Structure

```
analyzerSentient/
├── main.py              # FastAPI server & API endpoints
├── agent.py             # Sentient News Agent implementation
├── news_sources.py      # News aggregation from multiple sources
├── models.py            # Pydantic models for API
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Example environment configuration
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | None |
| `NEWS_API_KEY` | NewsAPI.org key for news aggregation | None |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `DEBUG` | Debug mode | False |
| `AGENT_NAME` | Agent display name | Daily Digest |
| `MAX_NEWS_ITEMS` | Maximum news items per query | 10 |
| `ENABLE_RSS` | Enable RSS feeds | True |
| `ENABLE_NEWS_API` | Enable NewsAPI | True |

## 🏗️ Sentient API Compliance

This agent follows the **Sentient Agent API** standards:

✅ **Streaming Support** - Real-time updates via SSE
✅ **Event Types** - thinking, searching, analyzing, content, data, complete, error
✅ **Context Sharing** - Support for conversation history and cross-agent context
✅ **Capabilities Endpoint** - Clear description of agent abilities
✅ **Error Handling** - Graceful error responses
✅ **Multi-modal Events** - Text content + structured data

## 📊 Supported News Categories

- 🖥️ **Technology** - TechCrunch, The Verge, Wired
- 💰 **Crypto** - CoinTelegraph, CoinDesk
- 💵 **Finance** - Bloomberg, Yahoo Finance
- 🤖 **AI** - AI News, Machine Learning feeds
- 📰 **General** - New York Times, BBC News

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

## 🐛 Troubleshooting

### Agent returns no results
- Check your API keys in `.env`
- Verify RSS feeds are accessible
- Try different keywords or categories

### Streaming not working
- Ensure `stream: true` in request
- Check browser/client supports SSE
- Verify no proxy/firewall blocking streaming

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.10+ recommended)

## 📝 License

MIT License - feel free to use and modify for your projects.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review Sentient API standards

## 🔗 Resources

- [Sentient Agent Framework](https://github.com/sentient-agi/Sentient-Agent-Framework)
- [NewsAPI Documentation](https://newsapi.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

---

Built with ❤️ following Sentient Agent API standards
