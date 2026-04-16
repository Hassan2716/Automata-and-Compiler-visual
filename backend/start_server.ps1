Write-Host "Starting Automata Visualizer Backend Server..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists and activate it
if (Test-Path "venv\Scripts\activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & .\venv\Scripts\activate.ps1
} else {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup_and_start.ps1 first to set up the environment." -ForegroundColor Yellow
    Write-Host "Or run: .\install_requirements.ps1" -ForegroundColor Yellow
    pause
    exit
}

# Check if requirements are installed
Write-Host "Checking if dependencies are installed..." -ForegroundColor Cyan
python -c "import fastapi; import uvicorn" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Dependencies not found. Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies!" -ForegroundColor Red
        pause
        exit
    }
}

Write-Host "`nStarting server..." -ForegroundColor Green
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API docs at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow
Write-Host ""
python main.py

