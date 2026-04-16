"""
DFA Minimizer using partitioning algorithm
"""
from automata.dfa import DFA
from typing import Set, List, Dict, Tuple


class DFAMinimizer:
    """Minimize DFA using state partitioning algorithm"""
    
    def minimize(self, dfa: DFA) -> DFA:
        """Minimize the given DFA"""
        # Initial partition: accepting and non-accepting states
        partition = []
        
        accepting = set(dfa.accept_states)
        non_accepting = set(dfa.states) - accepting
        
        if accepting:
            partition.append(accepting)
        if non_accepting:
            partition.append(non_accepting)
        
        if not partition:
            return dfa
        
        # Refine partition until no changes
        changed = True
        while changed:
            changed = False
            new_partition = []
            
            for group in partition:
                if len(group) == 1:
                    new_partition.append(group)
                    continue
                
                # Split group based on transitions
                subgroups = self._split_group(group, partition, dfa)
                if len(subgroups) > 1:
                    changed = True
                    new_partition.extend(subgroups)
                else:
                    new_partition.append(group)
            
            partition = new_partition
        
        # Create minimized DFA
        return self._build_minimized_dfa(dfa, partition)
    
    def _split_group(self, group: Set[str], partition: List[Set[str]], 
                     dfa: DFA) -> List[Set[str]]:
        """Split a group of states into subgroups based on transitions"""
        if len(group) == 1:
            return [group]
        
        # Group states by their transition behavior
        behavior_map = {}
        
        for state in group:
            behavior = []
            for symbol in sorted(dfa.alphabet):
                next_state = dfa.transitions.get(state, {}).get(symbol)
                # Find which partition group the next state belongs to
                group_index = self._find_group_index(next_state, partition)
                behavior.append((symbol, group_index))
            
            behavior_key = tuple(behavior)
            if behavior_key not in behavior_map:
                behavior_map[behavior_key] = set()
            behavior_map[behavior_key].add(state)
        
        return list(behavior_map.values())
    
    def _find_group_index(self, state: str, partition: List[Set[str]]) -> int:
        """Find which partition group a state belongs to"""
        if state is None:
            return -1  # Dead state
        for i, group in enumerate(partition):
            if state in group:
                return i
        return -1
    
    def _build_minimized_dfa(self, dfa: DFA, partition: List[Set[str]]) -> DFA:
        """Build the minimized DFA from partition"""
        # Map each state to its representative (first state in its group)
        state_to_rep = {}
        representatives = {}
        
        for i, group in enumerate(partition):
            rep = min(group)  # Use lexicographically smallest state as rep
            representatives[rep] = group
            for state in group:
                state_to_rep[state] = rep
        
        # Find start state representative
        start_rep = state_to_rep.get(dfa.start_state)
        
        # Find accepting states representatives
        accept_reps = set()
        for acc_state in dfa.accept_states:
            accept_reps.add(state_to_rep[acc_state])
        
        # Build transitions
        minimized_transitions = {}
        minimized_states = list(representatives.keys())
        
        for rep in minimized_states:
            minimized_transitions[rep] = {}
            # Get any state from the group to check transitions
            sample_state = min(representatives[rep])
            
            for symbol in dfa.alphabet:
                if sample_state in dfa.transitions:
                    if symbol in dfa.transitions[sample_state]:
                        next_state = dfa.transitions[sample_state][symbol]
                        if next_state:
                            next_rep = state_to_rep.get(next_state)
                            if next_rep:
                                minimized_transitions[rep][symbol] = next_rep
        
        return DFA(
            states=minimized_states,
            alphabet=list(dfa.alphabet),
            start_state=start_rep,
            accept_states=list(accept_reps),
            transitions=minimized_transitions
        )

