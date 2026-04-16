"""
Context-Free Grammar tools: FIRST, FOLLOW, Predictive Parsing Table
"""
from typing import Dict, List, Set, Optional


class CFGTools:
    """Tools for working with Context-Free Grammars"""
    
    def __init__(self, productions: Dict[str, List[str]]):
        """
        Initialize CFG tools
        
        Args:
            productions: Dictionary mapping non-terminals to list of production rules
                        e.g., {"S": ["aSb", "ab"], "A": ["aA", "ε"]}
        """
        self.productions = productions
        self.non_terminals = set(productions.keys())
        self.terminals = self._extract_terminals()
        self.first_sets = {}
        self.follow_sets = {}
    
    def _extract_terminals(self) -> Set[str]:
        """Extract all terminal symbols from productions"""
        terminals = set()
        for rules in self.productions.values():
            for rule in rules:
                for char in rule:
                    if char not in self.non_terminals and char != 'ε':
                        terminals.add(char)
        return terminals
    
    def compute_first_sets(self) -> Dict[str, Set[str]]:
        """Compute FIRST sets for all non-terminals"""
        self.first_sets = {nt: set() for nt in self.non_terminals}
        changed = True
        
        while changed:
            changed = False
            for non_terminal, rules in self.productions.items():
                old_first = self.first_sets[non_terminal].copy()
                
                for rule in rules:
                    if rule == 'ε':
                        self.first_sets[non_terminal].add('ε')
                    else:
                        # Add FIRST of first symbol in rule
                        first_symbol = rule[0]
                        if first_symbol in self.terminals:
                            self.first_sets[non_terminal].add(first_symbol)
                        elif first_symbol in self.non_terminals:
                            # Add FIRST(non_terminal) - {ε}
                            first_without_epsilon = self.first_sets[first_symbol] - {'ε'}
                            self.first_sets[non_terminal].update(first_without_epsilon)
                            
                            # If ε in FIRST, check next symbols
                            if 'ε' in self.first_sets[first_symbol]:
                                for i in range(1, len(rule)):
                                    symbol = rule[i]
                                    if symbol in self.terminals:
                                        self.first_sets[non_terminal].add(symbol)
                                        break
                                    elif symbol in self.non_terminals:
                                        first_without_epsilon = self.first_sets[symbol] - {'ε'}
                                        self.first_sets[non_terminal].update(first_without_epsilon)
                                        if 'ε' not in self.first_sets[symbol]:
                                            break
                                    if i == len(rule) - 1:
                                        self.first_sets[non_terminal].add('ε')
                
                if self.first_sets[non_terminal] != old_first:
                    changed = True
        
        return self.first_sets
    
    def compute_follow_sets(self) -> Dict[str, Set[str]]:
        """Compute FOLLOW sets for all non-terminals"""
        if not self.first_sets:
            self.compute_first_sets()
        
        self.follow_sets = {nt: set() for nt in self.non_terminals}
        
        # Add $ to FOLLOW of start symbol (first non-terminal)
        start_symbol = list(self.non_terminals)[0]
        self.follow_sets[start_symbol].add('$')
        
        changed = True
        while changed:
            changed = False
            for non_terminal, rules in self.productions.items():
                for rule in rules:
                    for i, symbol in enumerate(rule):
                        if symbol in self.non_terminals:
                            old_follow = self.follow_sets[symbol].copy()
                            
                            # Get remaining part of rule after symbol
                            remaining = rule[i+1:]
                            
                            if remaining:
                                first_of_remaining = self._first_of_string(remaining)
                                first_without_epsilon = first_of_remaining - {'ε'}
                                self.follow_sets[symbol].update(first_without_epsilon)
                                
                                if 'ε' in first_of_remaining:
                                    self.follow_sets[symbol].update(self.follow_sets[non_terminal])
                            else:
                                # A is at end, add FOLLOW(A) to FOLLOW(B)
                                self.follow_sets[symbol].update(self.follow_sets[non_terminal])
                            
                            if self.follow_sets[symbol] != old_follow:
                                changed = True
        
        return self.follow_sets
    
    def _first_of_string(self, string: str) -> Set[str]:
        """Compute FIRST of a string"""
        if not string:
            return {'ε'}
        
        first_set = set()
        for i, symbol in enumerate(string):
            if symbol in self.terminals:
                first_set.add(symbol)
                break
            elif symbol in self.non_terminals:
                first_without_epsilon = self.first_sets[symbol] - {'ε'}
                first_set.update(first_without_epsilon)
                if 'ε' not in self.first_sets[symbol]:
                    break
                if i == len(string) - 1:
                    first_set.add('ε')
            else:  # ε
                first_set.add('ε')
                break
        
        return first_set
    
    def build_predictive_table(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Build predictive parsing table M[A, a]
        Returns: Dictionary mapping (non_terminal, terminal) to production rule
        """
        if not self.first_sets:
            self.compute_first_sets()
        if not self.follow_sets:
            self.compute_follow_sets()
        
        table = {}
        
        for non_terminal, rules in self.productions.items():
            table[non_terminal] = {}
            for rule in rules:
                first_of_rule = self._first_of_string(rule)
                first_without_epsilon = first_of_rule - {'ε'}
                
                # For each terminal a in FIRST(α), add A → α to M[A, a]
                for terminal in first_without_epsilon:
                    if terminal not in table[non_terminal]:
                        table[non_terminal][terminal] = []
                    table[non_terminal][terminal].append(rule)
                
                # If ε in FIRST(α), add A → α to M[A, b] for each b in FOLLOW(A)
                if 'ε' in first_of_rule:
                    for terminal in self.follow_sets[non_terminal]:
                        if terminal not in table[non_terminal]:
                            table[non_terminal][terminal] = []
                        table[non_terminal][terminal].append(rule)
        
        return table

