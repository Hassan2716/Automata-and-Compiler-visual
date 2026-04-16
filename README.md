** Automata & Compiler Visualizer**

A full-stack educational web application for visualizing and working with Finite Automata (NFA, DFA) and Context-Free Grammars (CFG).

Built using React, D3.js, FastAPI, and Python, this project helps students understand core concepts of Automata Theory and Compiler Design through interactive visualizations and algorithmic implementations.

📌 Overview

The Automata & Compiler Visualizer is designed as an interactive learning tool for computer science students. It combines theoretical algorithms with graphical visualization to make complex concepts easier to understand.

The system allows users to:

Convert Regular Expressions → NFA

Convert NFA → DFA

Minimize a DFA

Compute FIRST & FOLLOW sets

Generate LL(1) Predictive Parsing Tables

The backend handles algorithmic computation, while the frontend provides an interactive graph-based interface for visualization.

🚀 Key Features
🔄 Automata Visualization
1️⃣ Regex to NFA

Implements Thompson’s Construction Algorithm

Supports operators: *, +, |, (), ε

Automatically generates epsilon transitions

Interactive state graph visualization

2️⃣ NFA to DFA

Uses Subset Construction Algorithm

Computes epsilon-closures

Generates deterministic automata from non-deterministic ones

Displays resulting DFA visually

3️⃣ DFA Minimization

Implements State Partitioning Algorithm

Merges equivalent states

Reduces number of states while preserving language recognition

🎨 Interactive Graph Features

Draggable nodes

Zoom & pan functionality

Color-coded states:

🟢 Start state

🔵 Accept states

⚪ Normal states

📐 Context-Free Grammar (CFG) Tools
1️⃣ FIRST Set Computation

Handles epsilon productions

Works with recursive grammar rules

Uses fixed-point iteration method

2️⃣ FOLLOW Set Computation

Computes terminal symbols that follow non-terminals

Uses FIRST sets internally

Handles epsilon propagation correctly

3️⃣ Predictive Parsing Table

Generates LL(1) parsing table

Detects grammar conflicts

Displays structured parsing matrix

🧠 Algorithms Implemented
Algorithm	Purpose
Thompson’s Construction	Convert Regex → NFA
Subset Construction	Convert NFA → DFA
State Partitioning	Minimize DFA
FIRST Set Algorithm	Compute FIRST sets
FOLLOW Set Algorithm	Compute FOLLOW sets
LL(1) Table Construction	Build Predictive Parsing Table
🛠 Tech Stack
🔹 Frontend

React.js

D3.js (Graph visualization)

Tailwind CSS

Vite

Axios

🔹 Backend

FastAPI

Python 3.8+

Pydantic (Data validation)

Uvicorn (ASGI server)

📂 Project Structure
automata-visualizer/
│
├── backend/                          # Backend API (FastAPI + Algorithms)
│   ├── main.py                       # API entry point
│   ├── requirements.txt              # Python dependencies
│   │
│   ├── automata/                     # Core algorithm implementations
│   │   ├── regex_parser.py           # Regex → NFA
│   │   ├── nfa.py                    # NFA → DFA conversion
│   │   ├── dfa.py                    # DFA implementation
│   │   ├── minimizer.py              # DFA minimization
│   │   └── cfg_tools.py              # FIRST, FOLLOW, Parsing table
│   │
│   └── models/                       # Optional database models
│
├── frontend/                         # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Controls.jsx          # Input controls
│   │   │   ├── GraphView.jsx         # D3 visualization
│   │   │   └── CFGView.jsx           # CFG result display
│   │   ├── App.jsx                   # Main application
│   │   ├── api.js                    # API communication
│   │   └── main.jsx                  # React entry
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md

⚙️ Installation & Setup
1️⃣ Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# or source venv/bin/activate (Mac/Linux)

pip install -r requirements.txt
python main.py


Backend runs at:

http://localhost:8000


API Documentation:

http://localhost:8000/docs

2️⃣ Frontend Setup
cd frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5173

📡 Available API Endpoints

POST /regex/to-nfa

POST /nfa/to-dfa

POST /dfa/minimize

POST /cfg/first-follow

POST /cfg/predictive-table

🎓 Educational Purpose

This project is ideal for:

Automata Theory coursework

Compiler Design classes

Academic demonstrations

Algorithm visualization learning

Understanding formal languages

It bridges the gap between theoretical concepts and practical implementation.
