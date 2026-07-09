"""Machine universelle. À COMPLÉTER : encode/decode et run.  -> Jour 4 (E4.2)."""
from __future__ import annotations
import json
from .turing import TuringMachine, TMResult


def encode(machine: "TuringMachine") -> str:
    # E4.2 : linéarisation INJECTIVE de M en JSON (transitions TRIÉES -> déterministe).
    trans = sorted([q, a, q2, b, d] for (q, a), (q2, b, d) in machine.transitions.items())
    obj = {
        "transitions": trans,
        "start": machine.start,
        "accept": sorted(machine.accept),
        "reject": sorted(machine.reject),
        "blank": machine.blank,
    }
    return json.dumps(obj, sort_keys=True)


def decode(desc: str) -> "TuringMachine":
    # E4.2 : réciproque exacte de encode.
    obj = json.loads(desc)
    trans = {(q, a): (q2, b, d) for q, a, q2, b, d in obj["transitions"]}
    return TuringMachine(
        transitions=trans,
        start=obj["start"],
        accept=set(obj["accept"]),
        blank=obj["blank"],
        reject=set(obj["reject"]),
    )


class UniversalTM:
    def run(self, encoded_machine: str, word: str, **kw) -> "TMResult":
        # E4.2 : U décode <M> puis simule M sur w (programme enregistré).
        machine = decode(encoded_machine)
        return machine.run(word, **kw)
