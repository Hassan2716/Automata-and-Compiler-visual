"""
NFA (Nondeterministic Finite Automaton) implementation
"""
from typing import Set, List, Dict, Optional
from automata.dfa import DFA


class NFA:
    """Nondeterministic Finite Automaton"""
    
    def __init__(self, states: List[str], alphabet: List[str], 
                 start_state: str, accept_states: List[str],
                 transitions: Dict[str, Dict[str, List[str]]]):
        self.states = states
        self.alphabet = set(alphabet)
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = transitions
        # Ensure all states are in transitions dict
        for state in self.states:
            if state not in self.transitions:
                self.transitions[state] = {}
    
    def epsilon_closure(self, states: Set[str]) -> Set[str]:
        """Compute epsilon closure of a set of states"""
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            if state in self.transitions and 'ε' in self.transitions[state]:
                for next_state in self.transitions[state]['ε']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        
        return closure
    
    def move(self, states: Set[str], symbol: str) -> Set[str]:
        """Move from states on symbol"""
        result = set()
        for state in states:
            if state in self.transitions and symbol in self.transitions[state]:
                result.update(self.transitions[state][symbol])
        return result
    
    def to_dfa(self) -> DFA:
        """Convert NFA to DFA using subset construction"""
        dfa_states = []
        dfa_transitions = {}
        dfa_start = None
        dfa_accept = []
        state_map = {}  # Maps DFA state (frozenset) to state name
        
        # Initialize with start state
        start_closure = self.epsilon_closure({self.start_state})
        start_set = frozenset(start_closure)
        
        if start_set:
            state_name = self._set_to_state_name(start_set)
            state_map[start_set] = state_name
            dfa_states.append(state_name)
            dfa_start = state_name
            
            # Check if start state is accepting
            if any(state in self.accept_states for state in start_closure):
                dfa_accept.append(state_name)
        
        # Process queue of unprocessed states
        unprocessed = [start_set]
        processed = set()
        
        while unprocessed:
            current_set = unprocessed.pop(0)
            if current_set in processed:
                continue
            processed.add(current_set)
            
            current_state_name = state_map[current_set]
            dfa_transitions[current_state_name] = {}
            
            # For each symbol in alphabet (excluding epsilon)
            for symbol in self.alphabet:
                if symbol == 'ε':
                    continue
                
                # Move and epsilon closure
                moved = self.move(current_set, symbol)
                closure = self.epsilon_closure(moved)
                
                if closure:
                    closure_set = frozenset(closure)
                    
                    # Create new DFA state if needed
                    if closure_set not in state_map:
                        state_name = self._set_to_state_name(closure_set)
                        state_map[closure_set] = state_name
                        dfa_states.append(state_name)
                        unprocessed.append(closure_set)
                        
                        # Check if accepting
                        if any(state in self.accept_states for state in closure):
                            dfa_accept.append(state_name)
                    
                    dfa_transitions[current_state_name][symbol] = state_map[closure_set]
        
        # If no transitions, ensure start state has empty transitions dict
        if dfa_start and dfa_start not in dfa_transitions:
            dfa_transitions[dfa_start] = {}
        
        return DFA(
            states=dfa_states,
            alphabet=list(self.alphabet - {'ε'}),
            start_state=dfa_start or dfa_states[0] if dfa_states else '',
            accept_states=dfa_accept,
            transitions=dfa_transitions
        )
    
    def _set_to_state_name(self, state_set: frozenset) -> str:
        """Convert a set of NFA states to a DFA state name"""
        sorted_states = sorted(list(state_set))
        return '{' + ','.join(sorted_states) + '}'
    
    def accepts(self, string: str) -> bool:
        """Check if NFA accepts a string (simulation)"""
        current_states = self.epsilon_closure({self.start_state})
        
        for symbol in string:
            current_states = self.epsilon_closure(self.move(current_states, symbol))
            if not current_states:
                return False
        
        return any(state in self.accept_states for state in current_states)

