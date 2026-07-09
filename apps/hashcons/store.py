"""Hash-consing : partage de structure (DAG) sur formlang.tree.Term. À COMPLÉTER.
-> TP arbres (E4 intern/partage, E5 round-trip, Q5 compression).

Règle « gate » : INSTANCIER formlang.tree.Term, ne pas le réécrire."""
from __future__ import annotations
from formlang.tree import Term

NodeId = int


class CompactStore:
    def __init__(self):
        self._nodes: list[tuple] = []          # id -> (symbol, label, kids_ids)
        self._table: dict[tuple, NodeId] = {}   # clé canonique -> id
        self._total = 0

    def intern(self, t: Term) -> NodeId:
        # E4 : partage maximal via une table canonique.
        kids_ids = tuple(self.intern(c) for c in t.children)
        self._total += 1
        key = (t.symbol, t.label, kids_ids)
        if key in self._table:
            return self._table[key]
        nid = len(self._nodes)
        self._nodes.append((t.symbol, t.label, kids_ids))
        self._table[key] = nid
        return nid

    def get(self, nid: NodeId) -> Term:
        # E5 : reconstruire l'arbre interné (round-trip exact).
        symbol, label, kids_ids = self._nodes[nid]
        children = tuple(self.get(k) for k in kids_ids)
        return Term(symbol, children, label)

    def total_nodes(self) -> int:
        return self._total

    def unique_nodes(self) -> int:
        return len(self._nodes)

    def compression(self) -> float:
        # Q5 : 1 - uniques/total (0 si total == 0).
        if self._total == 0:
            return 0.0
        return 1 - len(self._nodes) / self._total
