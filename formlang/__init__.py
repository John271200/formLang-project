"""formlang — squelette étudiant."""
from .tree import Term, TreeAutomaton, product, REJECT
from .turing import TuringMachine, TMResult
from .utm import UniversalTM, encode, decode

__all__ = [
    "Term", "TreeAutomaton", "product", "REJECT",
    "TuringMachine", "TMResult", "UniversalTM", "encode", "decode",
]
