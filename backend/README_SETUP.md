# Backend Setup Instructions

## Quick Start (Recommended)

Run this single command to set up everything and start the server:

```powershell
.\setup_and_start.ps1
```

This will:
1. Create a virtual environment (if needed)
2. Install all dependencies
3. Start the backend server

## Manual Setup

If you prefer to set up manually:

### Step 1: Install Dependencies

```powershell
.\install_requirements.ps1
```

This will:
- Create/activate virtual environment
- Install all required packages

### Step 2: Start the Server

```powershell
.\start_server.ps1
```

Or manually:
```powershell
.\venv\Scripts\activate
python main.py
```

## Troubleshooting

### Error: "No module named 'fastapi'"

**Solution:** Run the installation script:
```powershell
.\install_requirements.ps1
```

### Error: "Cannot connect to backend server"

**Solution:** Make sure the backend is running:
1. Check if you see "Uvicorn running on http://0.0.0.0:8000" in the terminal
2. Open http://localhost:8000/docs in your browser to verify
3. If not running, start it with `.\start_server.ps1`

### Virtual Environment Issues

If you get permission errors, run PowerShell as Administrator, or use:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Verify Installation

To check if everything is installed correctly:
```powershell
.\venv\Scripts\activate
python -c "import fastapi; import uvicorn; print('All packages installed!')"
```

## Server URLs

Once running:
- **API Server:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Frontend:** http://localhost:3000 (run from frontend folder)

