# Troubleshooting Guide

## Error: "Rust not found" or "pydantic-core" compilation error

**Problem:** Pydantic 2.x requires `pydantic-core` which is written in Rust. On Windows, if pre-built wheels aren't available, it tries to compile from source and fails.

**Solution 1: Use the simple installer (Recommended)**
```powershell
.\install_requirements_simple.ps1
```

**Solution 2: Install pydantic-core separately**
```powershell
.\venv\Scripts\activate
pip install --upgrade pip
pip install pydantic-core
pip install pydantic
```

**Solution 3: Use an older pydantic version temporarily**
Edit `requirements.txt` and change:
```
pydantic==2.0.0
```
Then run:
```powershell
pip install -r requirements.txt
```

**Solution 4: Install packages without version constraints**
```powershell
.\venv\Scripts\activate
pip install --upgrade pip wheel setuptools
pip install fastapi uvicorn sqlalchemy pydantic
```

## Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Dependencies aren't installed. Run:
```powershell
.\install_requirements.ps1
```

## Error: "Cannot connect to backend server"

**Solution:** Backend isn't running. Start it with:
```powershell
.\start_server.ps1
```

Make sure you see: `Uvicorn running on http://0.0.0.0:8000`

## Virtual Environment Issues

**Error:** "venv\Scripts\activate : The term 'venv\Scripts\activate' is not recognized"

**Solution:** Use PowerShell's call operator:
```powershell
& .\venv\Scripts\activate.ps1
```

Or create a new virtual environment:
```powershell
python -m venv venv
& .\venv\Scripts\activate.ps1
```

## Permission Errors

**Error:** Execution policy restrictions

**Solution:** Run PowerShell as Administrator, then:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try the scripts again.

## Still Having Issues?

1. Make sure Python 3.8+ is installed: `python --version`
2. Make sure pip is up to date: `python -m pip install --upgrade pip`
3. Try installing packages one by one to identify the problematic package
4. Check Python version compatibility (Python 3.8-3.11 recommended)

