"""Automate d'arbres ascendant (BUTA) générique. À COMPLÉTER : run, accepts,
product.  -> Jour 3 (E3.1, E3.4)."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Hashable


@dataclass(frozen=True)
class Term:
    symbol: str
    children: tuple["Term", ...] = ()
    label: Optional[str] = None


class _Reject:
    __slots__ = ()
    def __repr__(self):
        return "REJECT"


REJECT = _Reject()


class TreeAutomaton:
    def __init__(self, final_states):
        self.delta: dict[tuple[str, tuple], Hashable] = {}
        self.final: set = set(final_states)

    def add_rule(self, symbol: str, child_states, result) -> None:
        # FOURNI
        self.delta[(symbol, tuple(child_states))] = result

    def run(self, t: "Term"):
        # E3.1 : étiquetage POST-ORDRE (feuilles -> racine).
        child_states = tuple(self.run(c) for c in t.children)
        if any(cs is REJECT for cs in child_states):
            return REJECT
        return self.delta.get((t.symbol, child_states), REJECT)

    def accepts(self, t: "Term") -> bool:
        # E3.1 : accepté ssi la racine reçoit un état final.
        return self.run(t) in self.final


def product(a1: "TreeAutomaton", a2: "TreeAutomaton") -> "TreeAutomaton":
    # E3.4 : automate produit, L = L(a1) inter L(a2). États = paires ; règles
    # composante par composante (même symbole, même arité).
    finals = {(f1, f2) for f1 in a1.final for f2 in a2.final}
    P = TreeAutomaton(finals)
    for (sym1, cs1), r1 in a1.delta.items():
        for (sym2, cs2), r2 in a2.delta.items():
            if sym1 == sym2 and len(cs1) == len(cs2):
                P.add_rule(sym1, tuple(zip(cs1, cs2)), (r1, r2))
    return P


def minimize(A: "TreeAutomaton") -> "TreeAutomaton":
    """BONUS Jour 3 : minimisation d'un BUTA déterministe par quotient de la
    congruence de Myhill-Nerode sur les arbres (TATA, ch. 1).

    Deux états sont équivalents s'ils donnent le même verdict dans tout
    contexte. Raffinement : partition initiale finaux / non-finaux, puis on
    sépare q et q' dès qu'un contexte à un trou (symbole, position, blocs des
    autres enfants) les envoie dans des blocs différents — une règle absente
    vaut REJECT, donc un contexte présent d'un côté seulement sépare aussi."""
    states = set(A.final)
    for (sym, cs), r in A.delta.items():
        states.update(cs)
        states.add(r)
    block = {q: (0 if q in A.final else 1) for q in states}
    while True:
        sig = {q: set() for q in states}
        for (sym, cs), r in A.delta.items():
            for i, q in enumerate(cs):
                ctx = (sym, i,
                       tuple(block[c] for j, c in enumerate(cs) if j != i),
                       block[r])
                sig[q].add(ctx)
        keys: dict = {}
        new_block = {}
        for q in sorted(states, key=repr):
            k = (block[q], frozenset(sig[q]))
            if k not in keys:
                keys[k] = len(keys)
            new_block[q] = keys[k]
        if new_block == block:
            break
        block = new_block
    names = {b: f"B{b}" for b in set(block.values())}
    M = TreeAutomaton({names[block[f]] for f in A.final})
    for (sym, cs), r in A.delta.items():
        M.add_rule(sym, tuple(names[block[c]] for c in cs), names[block[r]])
    return M
