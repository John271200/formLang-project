"""Délimiteurs (FOURNI ; repose sur DelimiterPDA.accepts, E2.1)."""
from formlang.pda import DelimiterPDA

_PDA = DelimiterPDA()


def well_parenthesized(w: str) -> bool:
    return _PDA.accepts(w)
