"""BONUS Jour 1 : construction de Thompson (regex -> AFN avec eps-transitions).

Grammaire des regex supportée (descente récursive) :
    alt    := cat ('|' cat)*
    cat    := star*
    star   := base ('*' | '+' | '?')*
    base   := '(' alt ')' | lettre

Chaque fragment est un couple (entrée, sortie) ; les opérateurs ne relient les
fragments que par des eps-transitions (la construction de Thompson classique).
Le résultat instancie formlang.nfa.NFA (eps = '')."""
from __future__ import annotations
from .nfa import NFA

_OPS = {"|", "*", "+", "?", "(", ")"}


def thompson(regex: str) -> NFA:
    pos = 0
    counter = 0
    trans: dict = {}                     # (state, sym|'') -> set(states)

    def new() -> str:
        nonlocal counter
        s = f"t{counter}"
        counter += 1
        return s

    def add(s, a, t) -> None:
        trans.setdefault((s, a), set()).add(t)

    def peek():
        return regex[pos] if pos < len(regex) else None

    def eat() -> str:
        nonlocal pos
        c = regex[pos]
        pos += 1
        return c

    def parse_alt():
        frags = [parse_cat()]
        while peek() == "|":
            eat()
            frags.append(parse_cat())
        if len(frags) == 1:
            return frags[0]
        s, f = new(), new()
        for fs, ff in frags:             # union : eps vers chaque branche
            add(s, "", fs)
            add(ff, "", f)
        return s, f

    def parse_cat():
        frags = []
        while peek() is not None and peek() not in ("|", ")"):
            frags.append(parse_star())
        if not frags:                     # mot vide (eps)
            s = new()
            return s, s
        s, f = frags[0]
        for ns, nf in frags[1:]:          # concaténation : eps de sortie en entrée
            add(f, "", ns)
            f = nf
        return s, f

    def parse_star():
        frag = parse_base()
        while peek() in ("*", "+", "?"):
            op = eat()
            fs, ff = frag
            s, f = new(), new()
            if op == "*":                 # zéro ou plus
                add(s, "", fs); add(s, "", f)
                add(ff, "", fs); add(ff, "", f)
            elif op == "+":               # un ou plus
                add(s, "", fs)
                add(ff, "", fs); add(ff, "", f)
            else:                         # '?' : zéro ou un
                add(s, "", fs); add(s, "", f)
                add(ff, "", f)
            frag = (s, f)
        return frag

    def parse_base():
        c = peek()
        if c == "(":
            eat()
            frag = parse_alt()
            if peek() != ")":
                raise ValueError(f"')' attendue en position {pos} de {regex!r}")
            eat()
            return frag
        if c is None or c in _OPS:
            raise ValueError(f"symbole inattendu {c!r} en position {pos} de {regex!r}")
        eat()
        s, f = new(), new()               # une lettre : deux états, une transition
        add(s, c, f)
        return s, f

    start, final = parse_alt()
    if pos != len(regex):
        raise ValueError(f"regex mal formée : reste {regex[pos:]!r}")
    return NFA(transitions=trans, start=start, accept={final})
