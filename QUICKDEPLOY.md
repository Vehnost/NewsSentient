# ⚡ Quick Deploy - News AI Agent

## 🎯 Fastest Option: Railway.app (3 Minutes)

### Step 1: Run Deploy Script
```bash
.\deploy_railway.bat
```

### Step 2: Create GitHub Repo
Go to: https://github.com/new
- Name: `news-ai-agent`
- Public or Private
- **DON'T** initialize with README

### Step 3: Deploy on Railway
1. Go to https://railway.app/
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `news-ai-agent`
5. Wait 2 minutes ☕

### Step 4: Get Your URL
Railway will give you: `https://your-app.railway.app`

### Step 5: Update Frontend
Open `examples/news_aggregator.html` and change:
```javascript
const API_URL = 'https://your-app.railway.app';
```

### Step 6: Deploy Frontend (Optional)
Upload `news_aggregator.html` to:
- GitHub Pages
- Netlify (drag & drop)
- Vercel

**Done! 🎉**

---

## 🐳 Alternative: Docker (Local)

```bash
# Run the deploy script
.\deploy_docker.bat

# Or manually:
docker-compose up --build -d

# Access at http://localhost:8000
# Open examples/news_aggregator.html in browser
```

---

## 📋 What You Get

✅ 40+ News Sources (Crypto, AI, Tech, Finance)
✅ AI Chat Agent
✅ Real-time News Feed
✅ Image Support
✅ Auto-refresh
✅ Mobile Responsive
✅ Free Hosting (Railway)

---

## 🆘 Need Help?

See full guide: [DEPLOY.md](DEPLOY.md)

**Common Issues:**
- **Git not installed?** Download: https://git-scm.com/
- **Docker not working?** Install: https://www.docker.com/products/docker-desktop
- **Railway timeout?** Check logs in Railway dashboard

---

## 🎯 Choose Your Path

| Option | Time | Cost | Difficulty |
|--------|------|------|-----------|
| Railway.app | 3 min | FREE | ⭐ Easy |
| Render.com | 5 min | FREE | ⭐ Easy |
| Docker Local | 2 min | FREE | ⭐⭐ Medium |
| DigitalOcean | 10 min | $5/mo | ⭐⭐⭐ Advanced |

**Recommendation:** Start with Railway.app! 🚀
