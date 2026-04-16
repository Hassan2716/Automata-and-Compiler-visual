Write-Host "=== Automata Visualizer Backend Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv\Scripts\activate.ps1") {
    Write-Host "Virtual environment found. Activating..." -ForegroundColor Green
    & .\venv\Scripts\activate.ps1
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment!" -ForegroundColor Red
        Write-Host "Make sure Python is installed and in your PATH." -ForegroundColor Yellow
        pause
        exit
    }
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & .\venv\Scripts\activate.ps1
}

Write-Host "`nUpdating pip, setuptools, and wheel..." -ForegroundColor Cyan
python -m pip install --upgrade pip setuptools wheel

Write-Host "`nInstalling requirements..." -ForegroundColor Cyan
Write-Host "Note: This may take a few minutes, especially for pydantic..." -ForegroundColor Yellow

# Install packages one by one to handle errors better
Write-Host "`nInstalling fastapi..." -ForegroundColor Cyan
pip install fastapi

Write-Host "Installing uvicorn..." -ForegroundColor Cyan
pip install uvicorn

Write-Host "Installing sqlalchemy..." -ForegroundColor Cyan
pip install sqlalchemy

Write-Host "Installing pydantic (this may take longer)..." -ForegroundColor Cyan
# Try installing pydantic - pip should get a pre-built wheel
pip install pydantic
if ($LASTEXITCODE -ne 0) {
    Write-Host "Pydantic installation encountered issues. Trying alternative..." -ForegroundColor Yellow
    # Try with upgraded pip and no build isolation
    python -m pip install --upgrade pip
    pip install pydantic --no-build-isolation
}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
    Write-Host "`nVerifying installation..." -ForegroundColor Cyan
    python -c "import fastapi; import uvicorn; print('All packages installed successfully!')"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nStarting server..." -ForegroundColor Green
        Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "API docs at: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow
        Write-Host ""
        python main.py
    } else {
        Write-Host "`nERROR: Package verification failed!" -ForegroundColor Red
        Write-Host "Please check the error messages above." -ForegroundColor Yellow
        pause
    }
} else {
    Write-Host "`n=== Setup Failed ===" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
    pause
}

