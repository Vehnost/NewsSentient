@echo off
echo ==========================================
echo CryptoNews AI - Simple Deployment
echo ==========================================
echo.

echo Initializing Git repository...
git init
git add .
git commit -m "Initial commit - CryptoNews AI"

echo.
echo ==========================================
echo NEXT STEPS:
echo ==========================================
echo.
echo 1. CREATE GITHUB REPO:
echo    Go to: https://github.com/new
echo    Name: cryptonews-ai
echo    Public, NO README
echo.
echo 2. PUSH CODE:
set /p USERNAME="   Enter your GitHub username: "
echo    Running: git push...
git remote add origin https://github.com/%USERNAME%/cryptonews-ai.git
git branch -M main
git push -u origin main
echo    Done!
echo.
echo 3. ENABLE GITHUB PAGES:
echo    https://github.com/%USERNAME%/cryptonews-ai/settings/pages
echo    Branch: main, Folder: / (root)
echo.
echo 4. DEPLOY TO RAILWAY:
echo    https://railway.app/new
echo    Deploy from GitHub: cryptonews-ai
echo.
echo 5. UPDATE API URL:
echo    After Railway deploys, manually edit:
echo    examples\news_aggregator.html
echo    Change: const API_URL = 'http://localhost:8000';
echo    To: const API_URL = 'https://YOUR-RAILWAY-URL';
echo    Then: git add . ^&^& git commit -m "Update URL" ^&^& git push
echo.
echo ==========================================
echo YOUR URLS:
echo ==========================================
echo Frontend: https://%USERNAME%.github.io/cryptonews-ai/
echo Backend: https://YOUR-APP.up.railway.app
echo ==========================================
echo.
pause
