@echo off
echo ==========================================
echo Railway.app Deployment Helper
echo ==========================================
echo.

echo Step 1: Initialize Git repository
git init
git add .
git commit -m "Initial commit - News AI Agent ready for deployment"

echo.
echo Step 2: Create GitHub repository
echo Go to: https://github.com/new
echo Repository name: news-ai-agent
echo Make it public or private
echo DO NOT initialize with README (we already have files)
echo.
pause

echo.
echo Step 3: Push to GitHub
set /p GITHUB_URL="Enter your GitHub repository URL (e.g., https://github.com/username/news-ai-agent.git): "
git remote add origin %GITHUB_URL%
git branch -M main
git push -u origin main

echo.
echo Step 4: Deploy on Railway
echo 1. Go to: https://railway.app/
echo 2. Click "New Project"
echo 3. Select "Deploy from GitHub repo"
echo 4. Choose 'news-ai-agent' repository
echo 5. Railway will auto-deploy!
echo.
echo That's it! Your app will be live in 2-3 minutes.
echo.
pause
