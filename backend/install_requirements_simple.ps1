# Simple installation script that installs packages individually
# This helps identify which package is causing issues

Write-Host "Installing dependencies one by one..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv\Scripts\activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & .\venv\Scripts\activate.ps1
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    & .\venv\Scripts\activate.ps1
}

Write-Host "`nUpdating pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

Write-Host "`nInstalling packages..." -ForegroundColor Cyan

Write-Host "1. Installing fastapi..." -ForegroundColor Yellow
pip install fastapi
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR installing fastapi!" -ForegroundColor Red; pause; exit }

Write-Host "2. Installing uvicorn..." -ForegroundColor Yellow
pip install uvicorn
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR installing uvicorn!" -ForegroundColor Red; pause; exit }

Write-Host "3. Installing pydantic..." -ForegroundColor Yellow
# Upgrade pip first to get the latest version that can handle pydantic better
pip install --upgrade pip wheel setuptools
# Try installing pydantic - pip should get a pre-built wheel
pip install pydantic
if ($LASTEXITCODE -ne 0) { 
    Write-Host "Pydantic installation had issues. Trying alternative methods..." -ForegroundColor Yellow
    # Try with no build isolation
    pip install pydantic --no-build-isolation
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Trying to install pydantic-core first..." -ForegroundColor Yellow
        # Sometimes installing pydantic-core separately helps
        pip install pydantic-core --only-binary :all:
        pip install pydantic
    }
}

Write-Host "4. Installing sqlalchemy..." -ForegroundColor Yellow
pip install sqlalchemy
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR installing sqlalchemy!" -ForegroundColor Red; pause; exit }

Write-Host "`n=== Installation Complete! ===" -ForegroundColor Green
Write-Host "`nVerifying installation..." -ForegroundColor Cyan
python -c "import fastapi; import uvicorn; import pydantic; import sqlalchemy; print('All packages installed successfully!')"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✓ All dependencies are installed correctly!" -ForegroundColor Green
} else {
    Write-Host "`n✗ Verification failed. Some packages may not be installed correctly." -ForegroundColor Red
}

pause

