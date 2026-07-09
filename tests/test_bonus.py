"""Tests des BONUS : Thompson (J1), CYK (J2), infixation + minimisation BUTA (J3),
table monolithique de la multiplication (J4)."""
from itertools import product as iproduct

from formlang.thompson import thompson
from formlang.cfg import balanced_cfg
from formlang.pda import DelimiterPDA
from formlang.tree import TreeAutomaton, Term, minimize
from formlang.utm import UniversalTM, encode
from apps.shield.detector import contains_or
from apps.morpho.automaton import (
    morpho_automaton, morpho_automaton_infix, classify, classify_infix,
    build_word, build_infixed_word,
)
from apps.mtu.machines import MUL
from apps.mtu.calculator import Calculatrice


# ----- J1 : construction de Thompson (regex -> AFN) ---------------------------
def test_thompson_equivaut_au_detecteur():
    N = thompson("(a|o|r)*or(a|o|r)*")
    for w in ["", "a", "or", "ora", "aor", "oar", "aoa", "ror", "oro",
              "orr", "aaaor", "oorr", "raro"]:
        assert N.accepts(w) == contains_or(w), w


def test_thompson_afn_afd_minimal_3_etats():
    # boucle complète : regex -> AFN (Thompson) -> AFD (sous-ensembles)
    # -> minimal (Moore) : on doit retrouver les 3 états du jour 1.
    N = thompson("(a|o|r)*or(a|o|r)*")
    assert N.to_dfa().minimize().num_states() == 3


def test_thompson_operateurs():
    assert thompson("a+").accepts("aaa") and not thompson("a+").accepts("")
    assert thompson("ab?a").accepts("aa") and thompson("ab?a").accepts("aba")
    assert not thompson("a|b").accepts("ab")


# ----- J2 : reconnaissance par CYK --------------------------------------------
def test_cyk_mots_equilibres():
    G = balanced_cfg()
    assert G.cyk("") and G.cyk("[]") and G.cyk("()") and G.cyk("[a(r)]")
    assert G.cyk("aaa") and G.cyk("[[]]")
    assert not G.cyk("[") and not G.cyk("([)]") and not G.cyk(")(")


def test_cyk_equivalent_au_pda():
    # validation croisée : CYK == PDA sur TOUS les mots de longueur <= 3 de Σ3
    G, P = balanced_cfg(), DelimiterPDA()
    sigma = "aor[]()"
    for n in range(4):
        for tup in iproduct(sigma, repeat=n):
            w = "".join(tup)
            assert G.cyk(w) == P.accepts(w), w


# ----- J3 : infixation (s‹um›ulat) --------------------------------------------
def test_infixation():
    t = build_infixed_word([], "s", "um", "ulat", [])
    # hors du langage de base : preuve qu'il fallait étendre Delta
    assert morpho_automaton().accepts(t) is False
    A = morpho_automaton_infix()
    assert classify_infix(A, t) == "INFIXED"
    # l'extension ne change rien aux mots déjà couverts
    b = build_word(["a", "na"], "pend", ["a"])
    assert classify_infix(A, b) == classify(A, b) == "CIRCUMFIXED"


# ----- J3 : minimisation d'un BUTA (quotient par congruence) --------------------
def _nstates(X: TreeAutomaton) -> int:
    st = set(X.final)
    for (sym, cs), r in X.delta.items():
        st.update(cs)
        st.add(r)
    return len(st)


def _unary(w: str) -> Term:
    # un mot est un arbre unaire : e (feuille) puis une lettre par étage
    t = Term("e")
    for c in w:
        t = Term(c, (t,))
    return t


def test_minimisation_buta():
    # automate unaire « contient or » avec un état C dupliqué en D (C ~ D)
    A = TreeAutomaton(final_states={"C", "D"})
    A.add_rule("e", (), "A")
    for (s, a), t in {("A", "a"): "A", ("A", "o"): "B", ("A", "r"): "A",
                      ("B", "a"): "A", ("B", "o"): "B", ("B", "r"): "C",
                      ("C", "a"): "D", ("C", "o"): "D", ("C", "r"): "D",
                      ("D", "a"): "C", ("D", "o"): "C", ("D", "r"): "C"}.items():
        A.add_rule(a, (s,), t)
    M = minimize(A)
    assert _nstates(A) == 4 and _nstates(M) == 3
    # le quotient reconnaît le même langage (comparé aussi à l'AFD du jour 1)
    for w in ["", "or", "aoa", "aor", "orr", "roro", "oar", "ooor"]:
        assert M.accepts(_unary(w)) == A.accepts(_unary(w)) == contains_or(w), w


# ----- J4 : table monolithique de la multiplication ---------------------------
def test_mul_monolithique_directe():
    assert MUL.run("11*111").tape.count("1") == 6
    c = Calculatrice()
    for n in range(5):
        for m in range(5):
            assert c.multiplication_monolithique(n, m) == n * m, (n, m)


def test_mul_monolithique_via_utm():
    # « validée par le simulateur » : aussi via la machine universelle U
    assert UniversalTM().run(encode(MUL), "111*11").tape.count("1") == 6
