"""Automate à pile (acceptation pile vide). À COMPLÉTER.  -> Jour 2 (E2.1)."""
from __future__ import annotations


class DelimiterPDA:
    def __init__(self, pairs=(("[", "]"), ("(", ")")), ignore=("a", "o", "r", "e")):
        self.open = {o for o, _ in pairs}
        self.match = {c: o for o, c in pairs}     # fermant -> ouvrant attendu
        self.ignore = set(ignore)

    def accepts(self, w: str) -> bool:
        # E2.1 : pile (list). Empiler sur ouvrant ; sur fermant, le sommet doit
        # correspondre (sinon rejet) ; ignorer a/o/r/e ; accepter si pile vide.
        stack = []
        for c in w:
            if c in self.open:
                stack.append(c)
            elif c in self.match:
                if not stack or stack[-1] != self.match[c]:
                    return False
                stack.pop()
            # sinon : symbole ignoré (a, o, r, e, ...)
        return not stack
