"""EnhancedNormalizer (FOURNI une fois leet_fst complété en E1.4)."""
from formlang.fst import leet_fst, reverse_twoway

_LEET = None  # construit paresseusement (évite l'appel à l'import : E1.4)


def leet_normalize(w: str) -> str:
    global _LEET
    if _LEET is None:
        _LEET = leet_fst()
    return _LEET.transduce(w)


def reverse(w: str) -> str:
    return reverse_twoway(w)
