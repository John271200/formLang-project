"""Calculatrice unaire. À COMPLÉTER.  -> Jour 4 (E4.3)."""
from .machines import ADD, SUB, MUL


def _ones(s: str) -> int:
    return s.count("1")


class Calculatrice:
    def addition(self, n: int, m: int) -> int:
        # '+' et '-' sont réalisés par de VRAIES machines de Turing.
        return _ones(ADD.run("1" * n + "+" + "1" * m).tape)

    def soustraction(self, n: int, m: int) -> int:   # tronquée à 0
        return _ones(SUB.run("1" * n + "-" + "1" * m).tape)

    def multiplication(self, n: int, m: int) -> int:
        # composition : n * m = additions répétées.
        total = 0
        for _ in range(m):
            total = self.addition(total, n)
        return total

    def multiplication_monolithique(self, n: int, m: int) -> int:
        # BONUS Jour 4 : une SEULE table de MT (MUL), aucune composition.
        return _ones(MUL.run("1" * n + "*" + "1" * m).tape)

    def division(self, n: int, m: int):              # -> (quotient, reste)
        if m == 0:
            raise ZeroDivisionError("division par zéro")
        q, r = 0, n
        while r >= m:
            r = self.soustraction(r, m)
            q += 1
        return (q, r)

    def chainer(self, v0: int, ops: list) -> int:
        v = v0
        for op, k in ops:
            if op == "+":
                v = self.addition(v, k)
            elif op == "-":
                v = self.soustraction(v, k)
            elif op == "*":
                v = self.multiplication(v, k)
            elif op == "/":
                v = self.division(v, k)[0]           # quotient
            else:
                raise ValueError(f"opérateur inconnu : {op}")
        return v
