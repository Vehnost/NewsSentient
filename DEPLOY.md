# 🚀 Deployment Guide - News AI Agent

## Quick Deploy Options

### 🎯 Option 1: Railway.app (Recommended - Easiest & Free)

1. **Create account** at [Railway.app](https://railway.app/)

2. **Deploy from GitHub:**
   ```bash
   # Push your code to GitHub first
   git init
   git add .
   git commit -m "Ready for deployment"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

3. **In Railway dashboard:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect `railway.json` and deploy!

4. **Set environment variables** (optional):
   - `NEWS_API_KEY` - if you have NewsAPI key
   - Other vars are already configured in railway.json

5. **Get your URL:**
   - Railway will give you a URL like: `https://your-app.railway.app`
   - Update it in your HTML files

**Cost:** FREE for 500 hours/month

---

### 🎨 Option 2: Render.com (Free Tier)

1. **Create account** at [Render.com](https://render.com/)

2. **Push to GitHub** (same as above)

3. **In Render dashboard:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`
   - Click "Create Web Service"

4. **Environment variables** are already set in `render.yaml`

5. **Your app URL:**
   - Will be like: `https://your-app.onrender.com`

**Cost:** FREE (with auto-sleep after 15 min inactivity)

---

### 🐳 Option 3: Docker (Local or VPS)

**Local testing:**
```bash
# Build and run
docker-compose up --build

# Access at http://localhost:8000
```

**Deploy to VPS (DigitalOcean, AWS, etc):**
```bash
# On your server
git clone YOUR_REPO_URL
cd analyzerSentient

# Create .env file
cp .env.example .env
nano .env  # Edit as needed

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

### ☁️ Option 4: DigitalOcean App Platform

1. **Create account** at [DigitalOcean](https://www.digitalocean.com/)

2. **Create new App:**
   - Go to Apps → "Create App"
   - Connect GitHub repository
   - Detect Dockerfile automatically
   - Configure:
     - Name: news-ai-agent
     - Region: Choose closest to users
     - Plan: Basic ($5/month)

3. **Environment variables:**
   - Add from `.env.example`

4. **Deploy!**

**Cost:** Starting at $5/month

---

## 🔧 Pre-Deployment Checklist

✅ **Files ready for deployment:**
- [x] `Dockerfile` - Docker configuration
- [x] `docker-compose.yml` - Local Docker orchestration
- [x] `railway.json` - Railway.app config
- [x] `render.yaml` - Render.com config
- [x] `Procfile` - Heroku/Railway process
- [x] `runtime.txt` - Python version
- [x] `requirements.txt` - Dependencies

✅ **Configuration:**
- [x] CORS enabled for your domain
- [x] Health check endpoint: `/health`
- [x] Environment variables documented in `.env.example`

---

## 📝 After Deployment

### Update Frontend URLs

After deployment, update the API URL in your HTML files:

**In `examples/news_aggregator.html`:**
```javascript
// Change this line:
const API_URL = 'http://localhost:8000';

// To your deployed URL:
const API_URL = 'https://your-app.railway.app';
// or
const API_URL = 'https://your-app.onrender.com';
```

### Host Frontend Files

You can host your HTML files on:
- **GitHub Pages** (free)
- **Netlify** (free)
- **Vercel** (free)
- Same server as backend

---

## 🧪 Test Your Deployment

```bash
# Test health endpoint
curl https://your-app-url.com/health

# Test capabilities
curl https://your-app-url.com/capabilities

# Test news query
curl -X POST https://your-app-url.com/v1/query/news \
  -H "Content-Type: application/json" \
  -d '{
    "categories": ["crypto"],
    "max_results": 10
  }'
```

---

## 🔒 Security Notes

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** - Automatically handled by Railway/Render
4. **Set DEBUG=False** in production
5. **Limit CORS** to your frontend domain (optional)

---

## 📊 Monitoring

### Railway:
- Built-in logs viewer
- Metrics dashboard
- Automatic health checks

### Render:
- Real-time logs
- Auto-deploy on git push
- Health monitoring

### Docker:
```bash
# View logs
docker-compose logs -f sentient-news-agent

# Check status
docker-compose ps

# Restart
docker-compose restart
```

---

## 🆘 Troubleshooting

**Problem: App crashes on startup**
```bash
# Check logs
docker-compose logs sentient-news-agent

# Common issues:
# - Missing dependencies in requirements.txt
# - Port already in use
# - Invalid environment variables
```

**Problem: RSS feeds fail**
- Check network connectivity
- Verify RSS URLs are accessible
- Some feeds may require User-Agent header (already configured)

**Problem: Out of memory**
- Reduce MAX_NEWS_ITEMS in .env
- Increase container memory limit
- Use fewer RSS sources

---

## 🎉 Recommended: Railway.app

**Why Railway?**
- ✅ Easiest deployment (3 clicks)
- ✅ Free tier: 500 hours/month
- ✅ Auto-deploy on git push
- ✅ Built-in PostgreSQL/Redis if needed
- ✅ Great developer experience
- ✅ Automatic HTTPS
- ✅ No credit card required for free tier

**Deploy now:**
1. Push to GitHub
2. Go to [Railway.app](https://railway.app/)
3. "New Project" → "Deploy from GitHub"
4. Done! 🚀

---

## 📚 Resources

- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)
- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🔄 CI/CD (Optional)

For automatic deployments, Railway and Render auto-deploy on git push to main branch.

No additional configuration needed! 🎉
