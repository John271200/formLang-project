"""SingularityDetector. À COMPLÉTER : table de l'AFD 'or'.  -> Jour 1 (E1.1)."""
from formlang.dfa import DFA

_DFA_OR = DFA(
    transitions={
        # E1.1 : AFD minimal reconnaissant « contient le facteur or »
        ("A", "a"): "A", ("A", "r"): "A", ("A", "o"): "B",
        ("B", "o"): "B", ("B", "a"): "A", ("B", "r"): "C",
        ("C", "a"): "C", ("C", "o"): "C", ("C", "r"): "C",
    },
    start="A", accept={"C"}, alphabet={"a", "o", "r"},
)


def contains_or(w: str) -> bool:
    return _DFA_OR.accepts(w)


def detector_dfa() -> DFA:
    return _DFA_OR
