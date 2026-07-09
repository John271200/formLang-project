"""Automate morphologique (instancie formlang.tree). À COMPLÉTER : règles Delta.
-> Jour 3 (E3.2). Constructeurs et classify FOURNIS."""
from formlang.tree import Term, TreeAutomaton


# ----- constructeurs FOURNIS ------------------------------------------------
def prefix(s): return Term("prefix", label=s)
def root(s):   return Term("root",   label=s)
def suffix(s): return Term("suffix", label=s)
def nil():     return Term("nil")
def prefixes(h, t): return Term("prefixes", (h, t))
def suffixes(h, t): return Term("suffixes", (h, t))
def rest(r, s):     return Term("rest", (r, s))
def word(p, r):     return Term("word", (p, r))


def build_word(pres, root_str, sufs) -> Term:
    pc = nil()
    for p in reversed(pres):
        pc = prefixes(prefix(p), pc)
    sc = nil()
    for s in reversed(sufs):
        sc = suffixes(suffix(s), sc)
    return word(pc, rest(root(root_str), sc))


# ----- à compléter ----------------------------------------------------------
def morpho_automaton() -> TreeAutomaton:
    # E3.2 : le label des feuilles est ignoré (seule la structure compte).
    A = TreeAutomaton(final_states={"WORD"})
    # feuilles
    A.add_rule("prefix", (), "PRE")
    A.add_rule("root", (), "ROOT")
    A.add_rule("suffix", (), "SUF")
    A.add_rule("nil", (), "NIL")
    # listes de préfixes / suffixes (récursives, terminées par nil)
    A.add_rule("prefixes", ("PRE", "NIL"), "PREFS")
    A.add_rule("prefixes", ("PRE", "PREFS"), "PREFS")
    A.add_rule("suffixes", ("SUF", "NIL"), "SUFS")
    A.add_rule("suffixes", ("SUF", "SUFS"), "SUFS")
    # racine + suffixes
    A.add_rule("rest", ("ROOT", "NIL"), "REST")
    A.add_rule("rest", ("ROOT", "SUFS"), "REST")
    # mot complet (avec ou sans préfixes)
    A.add_rule("word", ("NIL", "REST"), "WORD")
    A.add_rule("word", ("PREFS", "REST"), "WORD")
    return A


# ----- FOURNI ---------------------------------------------------------------
def _contains(t: Term, sym: str) -> bool:
    if t.symbol == sym:
        return True
    return any(_contains(c, sym) for c in t.children)


def classify(A: TreeAutomaton, t: Term) -> str:
    if not A.accepts(t):
        return "INVALID"
    p, s = _contains(t, "prefix"), _contains(t, "suffix")
    if p and s:
        return "CIRCUMFIXED"
    if s:
        return "SUFFIXED"
    if p:
        return "PREFIXED"
    return "BARE"


# ----- BONUS Jour 3 : infixation (ex. tagalog s‹um›ulat) ----------------------
def infix(s):
    return Term("infix", label=s)


def iroot(left, inf, right):
    """Racine infixée : la racine est coupée en deux autour de l'infixe."""
    return Term("iroot", (root(left), infix(inf), root(right)))


def build_infixed_word(pres, root_left, inf, root_right, sufs) -> Term:
    pc = nil()
    for p in reversed(pres):
        pc = prefixes(prefix(p), pc)
    sc = nil()
    for s in reversed(sufs):
        sc = suffixes(suffix(s), sc)
    return word(pc, rest(iroot(root_left, inf, root_right), sc))


def morpho_automaton_infix() -> TreeAutomaton:
    """Étend Δ : une racine infixée iroot(ROOT, INF, ROOT) se comporte comme
    une ROOT ordinaire — le reste de l'automate est INCHANGÉ (même instance)."""
    A = morpho_automaton()
    A.add_rule("infix", (), "INF")
    A.add_rule("iroot", ("ROOT", "INF", "ROOT"), "ROOT")
    return A


def classify_infix(A: TreeAutomaton, t: Term) -> str:
    if not A.accepts(t):
        return "INVALID"
    if _contains(t, "infix"):
        return "INFIXED"
    return classify(A, t)
