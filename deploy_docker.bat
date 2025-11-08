@echo off
echo ==========================================
echo Docker Deployment - News AI Agent
echo ==========================================
echo.

echo Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker is installed! ✓
echo.

echo Building and starting containers...
docker-compose up --build -d

echo.
echo ==========================================
echo Deployment Complete! 🚀
echo ==========================================
echo.
echo Your News AI Agent is now running!
echo.
echo API: http://localhost:8000
echo Health: http://localhost:8000/health
echo Capabilities: http://localhost:8000/capabilities
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo To stop:
echo   docker-compose down
echo.
echo Open the web interface:
echo   examples\news_aggregator.html
echo.
pause
