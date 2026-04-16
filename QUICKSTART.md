# Quick Start Guide

## Backend Setup (5 minutes)

### Quick Start (Recommended for Windows)

```powershell
# Navigate to backend
cd backend

# Run the all-in-one setup script
.\setup_and_start.ps1
```

This will automatically:
- Create virtual environment
- Install all dependencies
- Start the server

### Manual Setup

```powershell
# Navigate to backend
cd backend

# Install dependencies (creates venv and installs packages)
.\install_requirements.ps1

# Start the server
.\start_server.ps1
```

### Alternative: Manual Commands

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\activate
# Windows CMD:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Initialize database
python init_db.py

# Start the server
python main.py
```

Backend will run on `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

**Important:** 
- Keep the backend terminal window open while using the frontend!
- If you see "ModuleNotFoundError", run `.\install_requirements.ps1` first
- If frontend shows "Cannot connect", make sure backend is running

## Frontend Setup (3 minutes)

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

## Try It Out!

1. **Regex to NFA**: Enter `(a|b)*ab` in the REGEX tab and click "Convert to NFA"
2. **NFA to DFA**: Use the NFA tab to convert an NFA to DFA
3. **DFA Minimization**: Minimize a DFA using the DFA tab
4. **CFG Analysis**: Enter `S:aSb|ab` in the CFG tab and compute FIRST/FOLLOW sets

## Example Regex Patterns

- `a*` - Zero or more a's
- `(a|b)*` - Any string of a's and b's
- `(a|b)*ab` - Strings ending with "ab"
- `a+b+` - One or more a's followed by one or more b's

## Example CFG Productions

Format: `NonTerminal:rule1|rule2,NonTerminal2:rule1|rule2`

- `S:aSb|ab` - Balanced parentheses (a and b)
- `E:E+T|T,T:T*F|F,F:(E)|id` - Simple arithmetic expressions
- `S:aS|bS|ε` - Any string of a's and b's including empty string

