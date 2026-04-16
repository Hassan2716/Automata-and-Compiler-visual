Write-Host "Checking virtual environment..." -ForegroundColor Cyan

# Check if virtual environment exists
if (Test-Path "venv\Scripts\activate.ps1") {
    Write-Host "Virtual environment found. Activating..." -ForegroundColor Green
    .\venv\Scripts\activate.ps1
} else {
    Write-Host "Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    .\venv\Scripts\activate.ps1
}

Write-Host "`nUpdating pip, setuptools, and wheel..." -ForegroundColor Green
python -m pip install --upgrade pip setuptools wheel

Write-Host "`nInstalling requirements (using pre-built wheels)..." -ForegroundColor Green
# Use --only-binary to force pre-built wheels and avoid compilation
pip install --only-binary :all: -r requirements.txt

# If that fails, try without --only-binary but with upgraded pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "Retrying with standard installation..." -ForegroundColor Yellow
    pip install --upgrade pip
    pip install -r requirements.txt
}

Write-Host "`nInstallation complete!" -ForegroundColor Green
Write-Host "You can now start the server with: python main.py" -ForegroundColor Cyan

