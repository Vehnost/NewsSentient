# 🚀 Deployment Guide

Comprehensive guide for deploying Sentient News Agent to production.

## 📋 Prerequisites

- Python 3.10 or higher
- Virtual environment (venv or conda)
- API keys (optional but recommended):
  - NewsAPI.org key for enhanced news aggregation
  - OpenAI/Anthropic key for AI features (future)

## 🔧 Local Development

### 1. Setup

```bash
# Clone or navigate to project
cd c:\python_projects\analyzerSentient

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# Add API keys if available
```

### 3. Run Development Server

```bash
# Option 1: Direct Python
python main.py

# Option 2: With Uvicorn (recommended)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option 3: With custom settings
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
```

### 4. Test the Server

```bash
# Run test client
python test_client.py

# Or open web client
# Open examples/web_client.html in browser

# Or use curl
curl http://localhost:8000/health
```

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Commands

```bash
# Build image
docker build -t sentient-news-agent .

# Run container
docker run -p 8000:8000 --env-file .env sentient-news-agent

# Run with docker-compose
docker-compose up -d
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  sentient-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - DEBUG=False
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## ☁️ Cloud Deployment

### Heroku

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create sentient-news-agent

# Set environment variables
heroku config:set NEWS_API_KEY=your_key_here

# Deploy
git push heroku main

# Open app
heroku open
```

Create `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### AWS EC2

```bash
# SSH to EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Python and dependencies
sudo apt update
sudo apt install python3.10 python3-pip

# Clone repository
git clone <your-repo-url>
cd analyzerSentient

# Install dependencies
pip3 install -r requirements.txt

# Run with systemd
sudo nano /etc/systemd/system/sentient-agent.service
```

systemd service file:
```ini
[Unit]
Description=Sentient News Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/analyzerSentient
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable sentient-agent
sudo systemctl start sentient-agent
sudo systemctl status sentient-agent
```

### DigitalOcean App Platform

1. Create new app in DigitalOcean dashboard
2. Connect GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `uvicorn main:app --host 0.0.0.0 --port 8000`
4. Add environment variables
5. Deploy

### Google Cloud Run

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Set project
gcloud config set project your-project-id

# Deploy
gcloud run deploy sentient-news-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔒 Security Best Practices

### 1. Environment Variables

Never commit `.env` file or API keys to Git:

```bash
# Ensure .gitignore includes
echo ".env" >> .gitignore
```

### 2. API Key Management

Use environment variables or secret managers:
- AWS Secrets Manager
- Google Cloud Secret Manager
- Azure Key Vault
- HashiCorp Vault

### 3. HTTPS

Always use HTTPS in production:

```python
# In main.py, add:
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
```

### 4. Rate Limiting

Add rate limiting to prevent abuse:

```bash
pip install slowapi

# In main.py:
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/v1/chat")
@limiter.limit("10/minute")
async def chat(request: Request, ...):
    ...
```

## 📊 Monitoring

### Logging

Configure structured logging:

```python
from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stdout,
    format="{time} {level} {message}",
    level="INFO"
)
logger.add(
    "logs/sentient-agent.log",
    rotation="500 MB",
    retention="10 days",
    level="INFO"
)
```

### Health Checks

Implement comprehensive health checks:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow(),
        "services": {
            "rss": "ok",
            "news_api": "ok" if settings.news_api_key else "disabled"
        }
    }
```

### Metrics

Use Prometheus for metrics:

```bash
pip install prometheus-fastapi-instrumentator

# In main.py:
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## 🔄 CI/CD

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest
      
      - name: Deploy to production
        run: |
          # Your deployment commands
```

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Linux/Mac

# Kill process
taskkill /PID <pid> /F  # Windows
kill -9 <pid>  # Linux/Mac
```

**Module not found:**
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

**API key errors:**
```bash
# Check .env file exists
cat .env

# Verify environment variables loaded
python -c "from config import settings; print(settings.news_api_key)"
```

## 📈 Performance Optimization

### 1. Caching

Implement Redis caching:

```bash
pip install redis

# In news_sources.py:
import redis
cache = redis.Redis(host='localhost', port=6379)
```

### 2. Connection Pooling

Configure connection limits:

```python
# In news_sources.py:
self.client = httpx.AsyncClient(
    timeout=30.0,
    limits=httpx.Limits(
        max_keepalive_connections=20,
        max_connections=100
    )
)
```

### 3. Workers

Run multiple workers:

```bash
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
```

## 🔐 Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Configure proper logging
- [ ] Set up HTTPS/SSL
- [ ] Add rate limiting
- [ ] Configure CORS properly
- [ ] Set up monitoring/alerting
- [ ] Implement health checks
- [ ] Configure backup strategy
- [ ] Test error handling
- [ ] Document API endpoints
- [ ] Set up CI/CD pipeline
- [ ] Configure auto-scaling
- [ ] Test load capacity
- [ ] Secure API keys
- [ ] Add request validation
- [ ] Set up domain name

## 📞 Support

For deployment issues:
1. Check logs: `tail -f logs/sentient-agent.log`
2. Verify configuration: `python -c "from config import settings; print(vars(settings))"`
3. Test endpoints: `curl http://localhost:8000/health`
4. Review documentation

---

**Ready to deploy!** 🚀
