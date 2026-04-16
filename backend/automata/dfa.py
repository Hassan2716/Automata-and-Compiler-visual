"""
DFA (Deterministic Finite Automaton) implementation
"""
from typing import Set, List, Dict


class DFA:
    """Deterministic Finite Automaton"""
    
    def __init__(self, states: List[str], alphabet: List[str],
                 start_state: str, accept_states: List[str],
                 transitions: Dict[str, Dict[str, str]]):
        self.states = states
        self.alphabet = set(alphabet)
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions
        # Ensure all states are in transitions dict
        for state in self.states:
            if state not in self.transitions:
                self.transitions[state] = {}
    
    def accepts(self, string: str) -> bool:
        """Check if DFA accepts a string"""
        current_state = self.start_state
        
        for symbol in string:
            if current_state not in self.transitions:
                return False
            if symbol not in self.transitions[current_state]:
                return False
            current_state = self.transitions[current_state][symbol]
        
        return current_state in self.accept_states
    
    def get_transition(self, state: str, symbol: str) -> str:
        """Get next state from current state and symbol"""
        if state in self.transitions and symbol in self.transitions[state]:
            return self.transitions[state][symbol]
        return None

