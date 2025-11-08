@echo off
echo ==========================================
echo CryptoNews AI - Complete Deployment
echo ==========================================
echo.

echo Step 1: Initialize Git
git init
git add .
git commit -m "Initial commit - CryptoNews AI Agent"

echo.
echo ==========================================
echo Step 2: Create GitHub Repository
echo ==========================================
echo.
echo Go to: https://github.com/new
echo.
echo Repository name: cryptonews-ai
echo Description: AI-powered crypto news aggregator with 40+ sources
echo Public (required for GitHub Pages)
echo DO NOT initialize with README
echo.
pause

echo.
echo Step 3: Push to GitHub
set /p GITHUB_USERNAME="Enter your GitHub username: "
git remote add origin https://github.com/%GITHUB_USERNAME%/cryptonews-ai.git
git branch -M main
git push -u origin main

echo.
echo Code pushed to GitHub!
echo.

echo ==========================================
echo Step 4: Enable GitHub Pages
echo ==========================================
echo.
echo 1. Go to: https://github.com/%GITHUB_USERNAME%/cryptonews-ai/settings/pages
echo 2. Source: Deploy from a branch
echo 3. Branch: main
echo 4. Folder: / (root)
echo 5. Click Save
echo.
echo Your frontend will be at:
echo https://%GITHUB_USERNAME%.github.io/cryptonews-ai/
echo.
pause

echo.
echo ==========================================
echo Step 5: Deploy Backend on Railway
echo ==========================================
echo.
echo 1. Go to: https://railway.app/new
echo 2. Click Deploy from GitHub repo
echo 3. Select cryptonews-ai
echo 4. Railway will auto-deploy!
echo.
echo Wait 2-3 minutes for deployment...
echo.
pause

echo.
echo ==========================================
echo Step 6: Get Railway URL
echo ==========================================
echo.
set /p RAILWAY_URL="Enter your Railway app URL (e.g., cryptonews-ai-production.up.railway.app): "

echo.
echo ==========================================
echo Step 7: Update Frontend
echo ==========================================
echo.

echo Updating API URL in news_aggregator.html...
powershell -Command "(Get-Content examples\news_aggregator.html) -replace 'const API_URL = ''http://localhost:8000'';', 'const API_URL = ''https://%RAILWAY_URL%'';' | Set-Content examples\news_aggregator.html"

git add examples\news_aggregator.html
git commit -m "Update API URL to Railway deployment"
git push

echo.
echo Frontend updated and pushed!
echo.

echo ==========================================
echo DEPLOYMENT COMPLETE!
echo ==========================================
echo.
echo Backend API: https://%RAILWAY_URL%
echo Frontend App: https://%GITHUB_USERNAME%.github.io/cryptonews-ai/
echo.
echo Test your API:
echo curl https://%RAILWAY_URL%/health
echo.
pause
