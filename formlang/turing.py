"""Machine de Turing déterministe (ruban dict bi-infini). À COMPLÉTER : run.
-> Jour 4 (E4.1)."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TMResult:
    accepted: bool
    tape: str
    steps: int
    trace: list = field(default_factory=list)


@dataclass
class TuringMachine:
    transitions: dict           # (q, a) -> (q', b, d in {'L','R','S'})
    start: str
    accept: set
    blank: str = "_"
    reject: set = field(default_factory=set)

    # ----- fourni -------------------------------------------------------------
    def _read(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1)).strip(self.blank)

    def _window(self, tape: dict) -> str:
        if not tape:
            return ""
        lo, hi = min(tape), max(tape)
        return "".join(tape.get(i, self.blank) for i in range(lo, hi + 1))

    # ----- à compléter --------------------------------------------------------
    def run(self, word: str, max_steps: int = 1_000_000, trace: bool = False) -> "TMResult":
        # E4.1 : ruban dict ; arrêt sur état final / de rejet / transition absente.
        tape = {i: c for i, c in enumerate(word) if c != self.blank}
        head = 0
        state = self.start
        steps = 0
        tr: list = []
        while True:
            if trace:
                tr.append((steps, state, tape.get(head, self.blank)))
            if state in self.reject:
                return TMResult(False, self._read(tape), steps, tr)
            if state in self.accept:
                return TMResult(True, self._read(tape), steps, tr)
            sym = tape.get(head, self.blank)
            move = self.transitions.get((state, sym))
            if move is None:                       # transition absente -> arrêt
                return TMResult(state in self.accept, self._read(tape), steps, tr)
            q2, b, d = move
            if b == self.blank:
                tape.pop(head, None)
            else:
                tape[head] = b
            if d == "L":
                head -= 1
            elif d == "R":
                head += 1
            state = q2
            steps += 1
            if steps > max_steps:
                raise RuntimeError("TuringMachine.run : dépassement de max_steps (boucle ?)")
