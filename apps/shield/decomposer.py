"""AttackDecomposer (instancie formlang.tree). À COMPLÉTER : règles Delta.
-> Jour 3 (E3.3). 100% structurel. Constructeurs FOURNIS."""
from formlang.tree import Term, TreeAutomaton, product

SAFE, OVR, ROLE, DANGER = "safe", "ovr", "role", "danger"
_SEV = {SAFE: 0, OVR: 1, ROLE: 2}
_BY_SEV = {0: SAFE, 1: OVR, 2: ROLE}
_ALL = (SAFE, OVR, ROLE, DANGER)


def _seq(x, y):
    # E3.3 : DANGER si l'un est DANGER, ou si le couple est {OVR, ROLE} ;
    # sinon on garde la sévérité maximale.
    if x == DANGER or y == DANGER:
        return DANGER
    if {x, y} == {OVR, ROLE}:
        return DANGER
    return _BY_SEV[max(_SEV[x], _SEV[y])]


def shield_automaton() -> TreeAutomaton:
    A = TreeAutomaton(final_states={DANGER})
    # feuilles
    A.add_rule("txt", (), SAFE)
    A.add_rule("enc", (), SAFE)
    A.add_rule("ovr", (), OVR)
    A.add_rule("role", (), ROLE)
    # séquence : produit cartésien complet des états
    for x in _ALL:
        for y in _ALL:
            A.add_rule("seq", (x, y), _seq(x, y))
    # cadre / système : tout contenu non SAFE devient DANGER
    for x in _ALL:
        esc = SAFE if x == SAFE else DANGER
        A.add_rule("frame", (x,), esc)
        A.add_rule("sys", (x,), esc)
    return A


# ----- constructeurs FOURNIS ------------------------------------------------
def txt():  return Term("txt")
def enc():  return Term("enc")
def ovr():  return Term("ovr")
def role(): return Term("role")
def seq(a, b): return Term("seq", (a, b))
def frame(a):  return Term("frame", (a,))
def sys(a):    return Term("sys", (a,))


def is_blocked(A: TreeAutomaton, t: Term) -> bool:
    return A.accepts(t)

# ----- P4.5 : « dangereux ET doublement encodé » (produit A x A_enc) ---------
def enc_automaton() -> TreeAutomaton:
    # E3.6 : compte les feuilles `enc` (plafonné à 2), final = {2}.
    #   feuilles txt/ovr/role -> 0, enc -> 1
    #   seq(x,y) -> min(2, x+y) ; frame(x) -> x ; sys(x) -> x
    A = TreeAutomaton(final_states={2})
    A.add_rule("txt", (), 0)
    A.add_rule("ovr", (), 0)
    A.add_rule("role", (), 0)
    A.add_rule("enc", (), 1)
    for x in (0, 1, 2):
        for y in (0, 1, 2):
            A.add_rule("seq", (x, y), min(2, x + y))
    for x in (0, 1, 2):
        A.add_rule("frame", (x,), x)
        A.add_rule("sys", (x,), x)
    return A


def dangerous_and_double_encoded() -> TreeAutomaton:
    # E3.6 : intersection = dangereux ET au moins deux encodages.
    return product(shield_automaton(), enc_automaton())
