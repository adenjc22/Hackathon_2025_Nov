# Legacy Album Backend - Start Script

Write-Host "🚀 Starting Legacy Album Backend Services..." -ForegroundColor Green
Write-Host ""

# Check if Redis is running
Write-Host "📋 Checking Redis connection..." -ForegroundColor Yellow
try {
    $redisTest = redis-cli ping 2>$null
    if ($redisTest -eq "PONG") {
        Write-Host "✅ Redis is running" -ForegroundColor Green
    } else {
        Write-Host "❌ Redis is not responding" -ForegroundColor Red
        Write-Host "   Start Redis with: docker run -d -p 6379:6379 redis" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Redis is not installed or not in PATH" -ForegroundColor Red
    Write-Host "   Install: https://redis.io/download" -ForegroundColor Yellow
}

Write-Host ""

# Check Python virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Virtual environment active: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "⚠️  No virtual environment detected" -ForegroundColor Yellow
    Write-Host "   Activate with: .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
}

Write-Host ""

# Instructions
Write-Host "📝 To start the services:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Start FastAPI server (Terminal 1):" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   uvicorn main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start Celery worker (Terminal 2):" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   celery -A app.ai_pipeline worker --pool=solo --loglevel=info" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Optional - Start Celery Flower monitoring (Terminal 3):" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   celery -A app.ai_pipeline flower" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 URLs:" -ForegroundColor Cyan
Write-Host "   FastAPI: http://localhost:8000" -ForegroundColor Gray
Write-Host "   Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "   Flower: http://localhost:5555" -ForegroundColor Gray
Write-Host ""
