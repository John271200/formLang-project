"""AFD. À COMPLÉTER : run, accepts, minimize (Moore).  -> Jour 1 (E1.1, E1.2)."""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque


@dataclass
class DFA:
    transitions: dict            # (state, sym) -> state
    start: str
    accept: set
    alphabet: set = field(default_factory=set)

    def __post_init__(self):
        if not self.alphabet:
            self.alphabet = {a for (_, a) in self.transitions}

    def run(self, w: str):
        # E1.1 : suivre les transitions lettre par lettre ; None si l'une manque.
        s = self.start
        for c in w:
            s = self.transitions.get((s, c))
            if s is None:
                return None
        return s

    def accepts(self, w: str) -> bool:
        # E1.1 : accepté ssi l'état atteint est final (run peut renvoyer None).
        return self.run(w) in self.accept

    # ----- fourni : utilitaires pour la minimisation --------------------------
    def _reachable(self) -> set:
        seen, todo = {self.start}, deque([self.start])
        while todo:
            s = todo.popleft()
            for a in self.alphabet:
                t = self.transitions.get((s, a))
                if t is not None and t not in seen:
                    seen.add(t)
                    todo.append(t)
        return seen

    def _completed(self):
        SINK = "__sink__"
        trans = dict(self.transitions)
        states = self._reachable()
        need = False
        for s in states:
            for a in self.alphabet:
                if (s, a) not in trans:
                    trans[(s, a)] = SINK
                    need = True
        if need:
            states = states | {SINK}
            for a in self.alphabet:
                trans[(SINK, a)] = SINK
        return states, trans

    def minimize(self) -> "DFA":
        # E1.2 : raffinement de partition (Moore) sur l'automate complété.
        states, trans = self._completed()
        finals = frozenset(s for s in states if s in self.accept)
        blocks = [b for b in (finals, frozenset(states - finals)) if b]
        changed = True
        while changed:
            changed = False
            index = {s: i for i, b in enumerate(blocks) for s in b}
            new_blocks = []
            for b in blocks:
                groups: dict = {}
                for s in b:
                    sig = tuple(index[trans[(s, a)]] for a in sorted(self.alphabet))
                    groups.setdefault(sig, set()).add(s)
                if len(groups) > 1:
                    changed = True
                new_blocks.extend(frozenset(g) for g in groups.values())
            blocks = new_blocks
        # nommer chaque bloc et reconstruire l'AFD réduit
        name = {}
        for b in blocks:
            label = "{" + ",".join(sorted(map(str, b))) + "}"
            for s in b:
                name[s] = label
        new_trans = {}
        for b in blocks:
            s = next(iter(b))
            for a in sorted(self.alphabet):
                new_trans[(name[s], a)] = name[trans[(s, a)]]
        new_accept = {name[s] for s in states if s in self.accept}
        return DFA(new_trans, name[self.start], new_accept, set(self.alphabet))

    def num_states(self) -> int:
        st = {self.start}
        for (s, _), t in self.transitions.items():
            st.add(s)
            st.add(t)
        return len(st)
