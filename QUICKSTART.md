# ⚡ Quick Start Guide

Get your Sentient News Agent up and running in 5 minutes!

## 🎯 What You'll Build

A fully functional AI-powered news agent that:
- ✅ Aggregates news from multiple sources
- ✅ Streams responses in real-time
- ✅ Follows Sentient Agent API standards
- ✅ Works with Sentient Chat interface

## 📦 Step 1: Install (2 minutes)

```bash
# Navigate to project
cd c:\python_projects\analyzerSentient

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Step 2: Configure (1 minute)

The agent works without API keys, but for best results:

```bash
# Open .env file and add (optional):
NEWS_API_KEY=your_key_here  # Get free key at https://newsapi.org
```

**Without API keys:** Agent uses RSS feeds only (still fully functional!)

## 🚀 Step 3: Run (30 seconds)

```bash
# Start the server
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## ✅ Step 4: Test (1 minute)

### Option A: Web Interface (Easiest)

1. Open `examples/web_client.html` in your browser
2. Click on any quick query button
3. Watch the magic happen! ✨

### Option B: Python Client

```bash
# In a new terminal
python test_client.py
```

### Option C: curl

```bash
# Test health
curl http://localhost:8000/health

# Simple query
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Latest AI news","stream":false}'
```

## 🎉 Success!

Your Sentient News Agent is now running! Try these queries:

- "Show me latest AI news"
- "What's happening in crypto?"
- "Latest technology trends"
- "Give me finance updates"

## 🔌 Connect to Sentient Chat

Your agent is now accessible at:
```
http://localhost:8000/v1/chat/stream
```

Use this URL in Sentient Chat to connect your agent.

## 📚 Next Steps

1. **Customize Categories**: Edit `news_sources.py` to add your favorite RSS feeds
2. **Add AI Features**: Configure OpenAI/Anthropic keys for enhanced analysis
3. **Deploy**: Check `DEPLOYMENT.md` for cloud deployment options
4. **Explore API**: Visit http://localhost:8000/docs for interactive API docs

## 🆘 Troubleshooting

**"Port already in use"?**
```bash
# Change port in .env
PORT=8001
```

**"Module not found"?**
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

**"No news found"?**
- Check internet connection
- Try different keywords
- Add NEWS_API_KEY in .env

## 🎓 Learning Resources

- **README.md** - Full documentation
- **examples/** - Code examples
- **DEPLOYMENT.md** - Production deployment
- **test_client.py** - Integration examples

## 💡 Pro Tips

1. **Add API Keys**: Dramatically improves news quality and quantity
2. **Use Streaming**: Enable `stream: true` for better UX
3. **Custom Categories**: Edit RSS feeds to match your interests
4. **Monitor Logs**: Watch terminal for debugging info

## 🚀 Ready to Build More?

This agent is just the beginning! Possible enhancements:

- 🤖 Add AI summarization with OpenAI
- 🌍 Multi-language support
- 📊 Sentiment analysis
- 🔔 Real-time notifications
- 💾 Save favorite articles
- 📈 Trending topics analysis

---

**Happy Building!** 🎉

Need help? Check the full README.md or create an issue.
