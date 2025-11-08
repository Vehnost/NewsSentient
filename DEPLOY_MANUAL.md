# 🚀 Manual Deployment - CryptoNews AI

## Step-by-Step Guide

### Step 1: Initialize Git

```bash
git init
git add .
git commit -m "Initial commit - CryptoNews AI"
```

### Step 2: Create GitHub Repository

1. Go to: https://github.com/new
2. **Repository name:** `cryptonews-ai`
3. **Description:** `AI-powered crypto news aggregator`
4. **Public** ✅
5. **DO NOT** initialize with README
6. Click **Create repository**

### Step 3: Push to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/cryptonews-ai.git
git branch -M main
git push -u origin main
```

### Step 4: Enable GitHub Pages

1. Go to: https://github.com/YOUR_USERNAME/cryptonews-ai/settings/pages
2. **Source:** Deploy from a branch
3. **Branch:** main
4. **Folder:** / (root)
5. Click **Save**

Wait 2-3 minutes. Your frontend will be at:
```
https://YOUR_USERNAME.github.io/cryptonews-ai/
```

### Step 5: Deploy to Railway

1. Go to: https://railway.app/new
2. Sign in with GitHub
3. Click **"Deploy from GitHub repo"**
4. Select **cryptonews-ai**
5. Wait 2-3 minutes for deployment

### Step 6: Get Railway URL

In Railway dashboard:
- Go to **Settings** → **Domains**
- Copy your URL (e.g., `cryptonews-ai-production.up.railway.app`)

### Step 7: Update API URL

Open `examples/news_aggregator.html` in editor.

Find this line (around line 632):
```javascript
const API_URL = 'http://localhost:8000';
```

Change it to:
```javascript
const API_URL = 'https://YOUR-RAILWAY-URL.up.railway.app';
```

Save the file.

### Step 8: Push Changes

```bash
git add examples/news_aggregator.html
git commit -m "Update API URL to Railway"
git push
```

Wait 1-2 minutes for GitHub Pages to update.

### Step 9: Test!

**Test Backend:**
```bash
curl https://YOUR-RAILWAY-URL.up.railway.app/health
```

Should return: `{"status":"healthy"}`

**Test Frontend:**
Open in browser:
```
https://YOUR_USERNAME.github.io/cryptonews-ai/
```

## ✅ Done!

Your app is now live! 🎉

### Your URLs:

**Frontend:**
```
https://YOUR_USERNAME.github.io/cryptonews-ai/
```

**Backend API:**
```
https://YOUR-RAILWAY-URL.up.railway.app
```

---

## 🔄 Update Your App

After making changes:

```bash
git add .
git commit -m "Your changes"
git push
```

- Railway will auto-deploy backend
- GitHub Pages will auto-update frontend

---

## 🆘 Troubleshooting

### Git push fails
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/cryptonews-ai.git
git push -u origin main
```

### Railway deploy fails
- Check logs in Railway dashboard
- Ensure `railway.json` exists
- Verify all files are on GitHub

### GitHub Pages not working
- Wait 5 minutes
- Check Settings → Pages
- Ensure repository is Public

### API not responding
- Check Railway logs
- Test health endpoint
- Verify environment variables

---

## 💡 Tips

1. **Free Limits:**
   - Railway: 500 hours/month
   - GitHub Pages: Unlimited

2. **Custom Domain:**
   - Railway: Settings → Domains
   - GitHub: Settings → Pages → Custom domain

3. **Monitoring:**
   - Railway dashboard for logs
   - Can add Sentry for error tracking

4. **Security:**
   - Never commit `.env` file
   - Use Railway environment variables for secrets

---

## 🎉 Success!

Share your app with friends! 🚀

Your CryptoNews AI is now:
- ✅ Live 24/7
- ✅ Auto-updating
- ✅ Free to use
- ✅ Secure (HTTPS)
