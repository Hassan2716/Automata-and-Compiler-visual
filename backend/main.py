from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn

from automata.regex_parser import RegexParser
from automata.nfa import NFA
from automata.dfa import DFA
from automata.minimizer import DFAMinimizer
from automata.cfg_tools import CFGTools

app = FastAPI(title="Automata & Compiler Visualizer API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Models
class RegexRequest(BaseModel):
    regex: str


class NFATransition(BaseModel):
    from_state: str
    symbol: str
    to_states: List[str]


class NFARequest(BaseModel):
    states: List[str]
    alphabet: List[str]
    start_state: str
    accept_states: List[str]
    transitions: Dict[str, Dict[str, List[str]]]


class DFARequest(BaseModel):
    states: List[str]
    alphabet: List[str]
    start_state: str
    accept_states: List[str]
    transitions: Dict[str, Dict[str, str]]


class CFGRequest(BaseModel):
    productions: Dict[str, List[str]]


@app.get("/")
async def root():
    return {"message": "Automata & Compiler Visualizer API"}


@app.post("/regex/to-nfa")
async def regex_to_nfa(request: RegexRequest):
    """Convert regex to NFA"""
    try:
        parser = RegexParser()
        nfa = parser.regex_to_nfa(request.regex)
        
        result = {
            "states": nfa.states,
            "alphabet": list(nfa.alphabet),
            "start_state": nfa.start_state,
            "accept_states": nfa.accept_states,
            "transitions": nfa.transitions,
            "steps": ["Parsed regex", "Constructed NFA"]
        }
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e), "message": "Invalid regex expression"}
        )


@app.post("/nfa/to-dfa")
async def nfa_to_dfa(request: NFARequest):
    """Convert NFA to DFA"""
    try:
        nfa = NFA(
            states=request.states,
            alphabet=request.alphabet,
            start_state=request.start_state,
            accept_states=request.accept_states,
            transitions=request.transitions
        )
        dfa = nfa.to_dfa()
        
        result = {
            "states": dfa.states,
            "alphabet": list(dfa.alphabet),
            "start_state": dfa.start_state,
            "accept_states": dfa.accept_states,
            "transitions": dfa.transitions,
            "steps": ["Converted NFA to DFA using subset construction"]
        }
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e), "message": "Error converting NFA to DFA"}
        )


@app.post("/dfa/minimize")
async def minimize_dfa(request: DFARequest):
    """Minimize DFA"""
    try:
        dfa = DFA(
            states=request.states,
            alphabet=request.alphabet,
            start_state=request.start_state,
            accept_states=request.accept_states,
            transitions=request.transitions
        )
        minimizer = DFAMinimizer()
        minimized_dfa = minimizer.minimize(dfa)
        
        result = {
            "states": minimized_dfa.states,
            "alphabet": list(minimized_dfa.alphabet),
            "start_state": minimized_dfa.start_state,
            "accept_states": minimized_dfa.accept_states,
            "transitions": minimized_dfa.transitions,
            "steps": ["Minimized DFA using state partitioning algorithm"]
        }
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e), "message": "Error minimizing DFA"}
        )


@app.post("/cfg/first-follow")
async def cfg_first_follow(request: CFGRequest):
    """Calculate FIRST and FOLLOW sets for CFG"""
    try:
        # Validate productions
        if not request.productions or len(request.productions) == 0:
            return JSONResponse(
                status_code=422,
                content={"error": "Productions cannot be empty", "message": "Please provide at least one production rule"}
            )
        
        cfg_tools = CFGTools(request.productions)
        first_sets = cfg_tools.compute_first_sets()
        follow_sets = cfg_tools.compute_follow_sets()
        
        # Convert sets to lists for JSON serialization
        first_sets_serialized = {k: list(v) for k, v in first_sets.items()}
        follow_sets_serialized = {k: list(v) for k, v in follow_sets.items()}
        
        result = {
            "first_sets": first_sets_serialized,
            "follow_sets": follow_sets_serialized,
            "steps": ["Computed FIRST sets", "Computed FOLLOW sets"]
        }
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e), "message": "Error computing FIRST and FOLLOW sets"}
        )


@app.post("/cfg/predictive-table")
async def cfg_predictive_table(request: CFGRequest):
    """Generate predictive parsing table"""
    try:
        # Validate productions
        if not request.productions or len(request.productions) == 0:
            return JSONResponse(
                status_code=422,
                content={"error": "Productions cannot be empty", "message": "Please provide at least one production rule"}
            )
        
        cfg_tools = CFGTools(request.productions)
        first_sets = cfg_tools.compute_first_sets()
        follow_sets = cfg_tools.compute_follow_sets()
        parsing_table = cfg_tools.build_predictive_table()
        
        # Convert sets to lists for JSON serialization
        first_sets_serialized = {k: list(v) for k, v in first_sets.items()}
        follow_sets_serialized = {k: list(v) for k, v in follow_sets.items()}
        
        result = {
            "parsing_table": parsing_table,
            "first_sets": first_sets_serialized,
            "follow_sets": follow_sets_serialized,
            "steps": ["Built predictive parsing table"]
        }
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e), "message": "Error building predictive parsing table"}
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

