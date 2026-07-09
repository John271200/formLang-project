"""Grammaire hors-contexte : génération bornée. À COMPLÉTER.  -> Jour 2 (E2.2).
BONUS : reconnaissance par CYK (mise en forme normale de Chomsky + table)."""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product as _iproduct


@dataclass
class CFG:
    rules: dict
    start: str
    nonterminals: set

    def generate(self, max_len: int) -> set:
        # E2.2 : énumérer les mots TERMINAUX dérivables de longueur <= max_len.
        # Piège : borner AUSSI le nombre de non-terminaux d'une forme (sinon
        # S -> S S engendre S, SS, SSS, ... sans jamais être élagué -> explosion).
        NT = self.nonterminals
        max_nt = 2 * max_len + 2
        results: set = set()
        seen: set = set()
        stack = [(self.start,)]
        while stack:
            form = stack.pop()
            if form in seen:
                continue
            seen.add(form)
            idx = next((i for i, s in enumerate(form) if s in NT), None)
            if idx is None:                       # forme entièrement terminale
                word = "".join(form)
                if len(word) <= max_len:
                    results.add(word)
                continue
            if sum(1 for s in form if s not in NT) > max_len:
                continue
            if sum(1 for s in form if s in NT) > max_nt:
                continue
            A = form[idx]
            for prod in self.rules[A]:
                stack.append(form[:idx] + tuple(prod) + form[idx + 1:])
        return results

    # ----- BONUS Jour 2 : reconnaissance par CYK ------------------------------
    def _cnf(self):
        """Forme normale de Chomsky : (règles binaires, règles terminales,
        nouvel axiome, eps accepté ?). Étapes : START, DEL(eps), UNIT, TERM, BIN."""
        NT = set(self.nonterminals)
        rules = {A: [tuple(p) for p in ps] for A, ps in self.rules.items()}
        S0 = "_S0"
        while S0 in NT:
            S0 += "'"
        rules[S0] = [(self.start,)]
        NT.add(S0)
        # DEL : symboles annulables (A =>* eps)
        nullable: set = set()
        changed = True
        while changed:
            changed = False
            for A, ps in rules.items():
                if A not in nullable and any(all(s in nullable for s in p) for p in ps):
                    nullable.add(A)
                    changed = True
        empty_ok = S0 in nullable
        # variantes de chaque règle en omettant les positions annulables
        no_eps = {A: set() for A in NT}
        for A, ps in rules.items():
            for p in ps:
                opts = [((s, None) if s in nullable else (s,)) for s in p]
                for combo in _iproduct(*opts):
                    q = tuple(s for s in combo if s is not None)
                    if q:
                        no_eps[A].add(q)
        # UNIT : clôture des paires unitaires A =>* B
        unit = {A: {A} for A in NT}
        changed = True
        while changed:
            changed = False
            for A in NT:
                for B in list(unit[A]):
                    for p in no_eps[B]:
                        if len(p) == 1 and p[0] in NT and p[0] not in unit[A]:
                            unit[A].add(p[0])
                            changed = True
        flat = {A: set() for A in NT}
        for A in NT:
            for B in unit[A]:
                for p in no_eps[B]:
                    if not (len(p) == 1 and p[0] in NT):
                        flat[A].add(p)
        # TERM + BIN : terminaux isolés dans les règles longues, puis découpage binaire
        term: dict = {}                    # NT -> set(terminal)
        binary: dict = {}                  # NT -> set((B, C))
        t_names: dict = {}
        counter = 0
        def _nt_of(a: str) -> str:
            if a not in t_names:
                T = f"_T{len(t_names)}"
                t_names[a] = T
                term.setdefault(T, set()).add(a)
            return t_names[a]
        for A in NT:
            for p in flat[A]:
                if len(p) == 1:            # A -> a
                    term.setdefault(A, set()).add(p[0])
                    continue
                syms = [s if s in NT else _nt_of(s) for s in p]
                cur = A
                while len(syms) > 2:
                    counter += 1
                    X = f"_X{counter}"
                    binary.setdefault(cur, set()).add((syms[0], X))
                    cur, syms = X, syms[1:]
                binary.setdefault(cur, set()).add((syms[0], syms[1]))
        return binary, term, S0, empty_ok

    def cyk(self, w: str) -> bool:
        """BONUS : w ∈ L(G) par programmation dynamique O(n³·|G|) sur la CNF."""
        binary, term, S0, empty_ok = self._cnf()
        if w == "":
            return empty_ok
        inv_term: dict = {}
        for A, ts in term.items():
            for a in ts:
                inv_term.setdefault(a, set()).add(A)
        inv_bin: dict = {}
        for A, ps in binary.items():
            for bc in ps:
                inv_bin.setdefault(bc, set()).add(A)
        n = len(w)
        # table[l][i] = non-terminaux dérivant w[i : i+l+1]
        table = [[set() for _ in range(n)] for _ in range(n)]
        for i, c in enumerate(w):
            table[0][i] = set(inv_term.get(c, ()))
        for l in range(2, n + 1):
            for i in range(n - l + 1):
                cell = table[l - 1][i]
                for k in range(1, l):
                    for B in table[k - 1][i]:
                        for C in table[l - k - 1][i + k]:
                            cell |= inv_bin.get((B, C), set())
        return S0 in table[n - 1][0]


def balanced_cfg() -> "CFG":
    # FOURNI : S -> S S | [ S ] | ( S ) | a | o | r | eps
    return CFG(
        rules={"S": [("S", "S"), ("[", "S", "]"), ("(", "S", ")"),
                     ("a",), ("o",), ("r",), ()]},
        start="S", nonterminals={"S"},
    )
