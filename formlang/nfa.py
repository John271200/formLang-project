"""AFN (eps = ''). À COMPLÉTER : to_dfa par sous-ensembles.  -> Jour 1 (E1.3)."""
from __future__ import annotations
from dataclasses import dataclass, field
from .dfa import DFA


@dataclass
class NFA:
    transitions: dict            # (state, sym|'') -> set(states)
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions if a != ""}

    # ----- fourni -------------------------------------------------------------
    def _eps_closure(self, states: frozenset) -> frozenset:
        stack, clos = list(states), set(states)
        while stack:
            s = stack.pop()
            for t in self.transitions.get((s, ""), ()):
                if t not in clos:
                    clos.add(t)
                    stack.append(t)
        return frozenset(clos)

    def _move(self, states: frozenset, a: str) -> frozenset:
        out = set()
        for s in states:
            out |= self.transitions.get((s, a), set())
        return frozenset(out)

    def accepts(self, w: str) -> bool:
        cur = self._eps_closure(frozenset({self.start}))
        for c in w:
            cur = self._eps_closure(self._move(cur, c))
        return any(s in self.accept for s in cur)

    # ----- à compléter --------------------------------------------------------
    def to_dfa(self) -> DFA:
        # E1.3 : construction des sous-ensembles (un état AFD = un frozenset d'AFN).
        start = self._eps_closure(frozenset({self.start}))
        names = {start: "S0"}
        trans = {}
        accept = set()
        todo = [start]
        counter = 1
        while todo:
            S = todo.pop()
            if any(s in self.accept for s in S):
                accept.add(names[S])
            for a in self.alphabet:
                T = self._eps_closure(self._move(S, a))
                if not T:            # sous-ensemble vide = rejet (transition absente)
                    continue
                if T not in names:
                    names[T] = f"S{counter}"
                    counter += 1
                    todo.append(T)
                trans[(names[S], a)] = names[T]
        return DFA(trans, names[start], accept, set(self.alphabet))
