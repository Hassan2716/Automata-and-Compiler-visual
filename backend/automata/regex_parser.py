"""
Regex to NFA converter using Thompson's construction algorithm
"""
from automata.nfa import NFA
from typing import Set, List, Dict
import re


class RegexParser:
    """Parse regular expressions and convert to NFA"""
    
    def __init__(self):
        self.state_counter = 0
    
    def _new_state(self) -> str:
        """Generate a new unique state name"""
        state = f"q{self.state_counter}"
        self.state_counter += 1
        return state
    
    def _char_nfa(self, char: str) -> NFA:
        """Create NFA for a single character"""
        start = self._new_state()
        end = self._new_state()
        
        states = {start, end}
        transitions = {start: {char: [end]}}
        
        return NFA(
            states=list(states),
            alphabet=[char],
            start_state=start,
            accept_states=[end],
            transitions=transitions
        )
    
    def _union_nfa(self, nfa1: NFA, nfa2: NFA) -> NFA:
        """Create NFA for union (a|b)"""
        start = self._new_state()
        end = self._new_state()
        
        # Combine states
        states = {start, end} | set(nfa1.states) | set(nfa2.states)
        
        # Combine transitions
        transitions = {}
        for state in states:
            transitions[state] = {}
        
        # Copy nfa1 transitions
        for state, trans in nfa1.transitions.items():
            transitions[state].update(trans)
        
        # Copy nfa2 transitions
        for state, trans in nfa2.transitions.items():
            if state in transitions:
                for symbol, to_states in trans.items():
                    if symbol in transitions[state]:
                        transitions[state][symbol].extend(to_states)
                    else:
                        transitions[state][symbol] = to_states.copy()
        
        # Add epsilon transitions from new start
        transitions[start] = transitions.get(start, {})
        if 'ε' in transitions[start]:
            transitions[start]['ε'].extend([nfa1.start_state, nfa2.start_state])
        else:
            transitions[start]['ε'] = [nfa1.start_state, nfa2.start_state]
        
        # Add epsilon transitions to new end
        for acc_state in nfa1.accept_states:
            if acc_state not in transitions:
                transitions[acc_state] = {}
            if 'ε' in transitions[acc_state]:
                transitions[acc_state]['ε'].append(end)
            else:
                transitions[acc_state]['ε'] = [end]
        
        for acc_state in nfa2.accept_states:
            if acc_state not in transitions:
                transitions[acc_state] = {}
            if 'ε' in transitions[acc_state]:
                transitions[acc_state]['ε'].append(end)
            else:
                transitions[acc_state]['ε'] = [end]
        
        # Combine alphabets
        alphabet = set(nfa1.alphabet) | set(nfa2.alphabet) | {'ε'}
        
        return NFA(
            states=list(states),
            alphabet=list(alphabet),
            start_state=start,
            accept_states=[end],
            transitions=transitions
        )
    
    def _concat_nfa(self, nfa1: NFA, nfa2: NFA) -> NFA:
        """Create NFA for concatenation (ab)"""
        states = set(nfa1.states) | set(nfa2.states)
        transitions = {}
        
        # Copy nfa1 transitions
        for state, trans in nfa1.transitions.items():
            transitions[state] = {k: v.copy() for k, v in trans.items()}
        
        # Copy nfa2 transitions
        for state, trans in nfa2.transitions.items():
            if state in transitions:
                for symbol, to_states in trans.items():
                    if symbol in transitions[state]:
                        transitions[state][symbol].extend(to_states)
                    else:
                        transitions[state][symbol] = to_states.copy()
            else:
                transitions[state] = {k: v.copy() for k, v in trans.items()}
        
        # Add epsilon transitions from nfa1 accept states to nfa2 start
        for acc_state in nfa1.accept_states:
            if acc_state not in transitions:
                transitions[acc_state] = {}
            if 'ε' in transitions[acc_state]:
                transitions[acc_state]['ε'].append(nfa2.start_state)
            else:
                transitions[acc_state]['ε'] = [nfa2.start_state]
        
        alphabet = set(nfa1.alphabet) | set(nfa2.alphabet) | {'ε'}
        
        return NFA(
            states=list(states),
            alphabet=list(alphabet),
            start_state=nfa1.start_state,
            accept_states=nfa2.accept_states,
            transitions=transitions
        )
    
    def _kleene_nfa(self, nfa: NFA) -> NFA:
        """Create NFA for Kleene star (a*)"""
        start = self._new_state()
        end = self._new_state()
        
        states = {start, end} | set(nfa.states)
        transitions = {}
        
        # Copy original transitions
        for state, trans in nfa.transitions.items():
            transitions[state] = {k: v.copy() for k, v in trans.items()}
        
        # Initialize new states
        transitions[start] = {}
        if end not in transitions:
            transitions[end] = {}
        
        # Epsilon from new start to old start and new end
        transitions[start]['ε'] = [nfa.start_state, end]
        
        # Epsilon from old accept states to old start and new end
        for acc_state in nfa.accept_states:
            if 'ε' in transitions[acc_state]:
                transitions[acc_state]['ε'].extend([nfa.start_state, end])
            else:
                transitions[acc_state]['ε'] = [nfa.start_state, end]
        
        alphabet = set(nfa.alphabet) | {'ε'}
        
        return NFA(
            states=list(states),
            alphabet=list(alphabet),
            start_state=start,
            accept_states=[end],
            transitions=transitions
        )
    
    def _preprocess_regex(self, regex: str) -> str:
        """Add explicit concatenation operators"""
        result = []
        for i, char in enumerate(regex):
            if i > 0:
                prev_char = regex[i-1]
                # Add concatenation if needed
                if ((prev_char not in '|(' and char not in '|)*') or
                    (prev_char == ')' and char not in '|)*') or
                    (prev_char not in '|(' and char == '(')):
                    result.append('.')
            result.append(char)
        return ''.join(result)
    
    def _infix_to_postfix(self, regex: str) -> str:
        """Convert infix regex to postfix using Shunting Yard algorithm"""
        precedence = {'|': 1, '.': 2, '*': 3}
        output = []
        operators = []
        
        i = 0
        while i < len(regex):
            char = regex[i]
            
            if char == '(':
                operators.append(char)
            elif char == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Remove '('
            elif char in precedence:
                while (operators and operators[-1] != '(' and
                       precedence.get(operators[-1], 0) >= precedence[char]):
                    output.append(operators.pop())
                operators.append(char)
            else:  # Regular character
                output.append(char)
            i += 1
        
        while operators:
            output.append(operators.pop())
        
        return ''.join(output)
    
    def regex_to_nfa(self, regex: str) -> NFA:
        """Convert regex to NFA using Thompson's construction"""
        if not regex:
            # Empty string NFA
            start = self._new_state()
            return NFA(
                states=[start],
                alphabet=[],
                start_state=start,
                accept_states=[start],
                transitions={start: {}}
            )
        
        # Preprocess and convert to postfix
        preprocessed = self._preprocess_regex(regex)
        postfix = self._infix_to_postfix(preprocessed)
        
        stack = []
        
        for char in postfix:
            if char == '*':
                nfa = stack.pop()
                stack.append(self._kleene_nfa(nfa))
            elif char == '|':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self._union_nfa(nfa1, nfa2))
            elif char == '.':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self._concat_nfa(nfa1, nfa2))
            else:
                stack.append(self._char_nfa(char))
        
        if not stack:
            raise ValueError("Invalid regex expression")
        
        return stack[0]

