from formlang.tree import Term, product
from apps.morpho.automaton import morpho_automaton, build_word, classify
from apps.shield.decomposer import (
    shield_automaton, is_blocked, txt, enc, ovr, role, seq, frame, sys,
)


def test_morpho_accept_et_classes():
    A = morpho_automaton()
    assert classify(A, build_word([], "livre", []))            == "BARE"
    assert classify(A, build_word([], "jou", ["er"]))          == "SUFFIXED"
    assert classify(A, build_word(["na"], "penda", []))        == "PREFIXED"
    assert classify(A, build_word(["a", "na"], "pend", ["a"])) == "CIRCUMFIXED"


def test_morpho_rejet():
    A = morpho_automaton()
    bad = Term("word", (Term("nil"),
                        Term("rest", (Term("suffix", label="er"), Term("nil")))))
    assert classify(A, bad) == "INVALID"


def test_shield_blocage():
    A = shield_automaton()
    assert is_blocked(A, seq(txt(), txt()))               is False
    assert is_blocked(A, role())                          is False
    assert is_blocked(A, sys(role()))                     is True
    assert is_blocked(A, seq(frame(ovr()), txt()))        is True
    assert is_blocked(A, sys(seq(txt(), frame(role()))))  is True
    assert is_blocked(A, seq(ovr(), role()))              is True


def _parite():
    from formlang.tree import TreeAutomaton
    A = TreeAutomaton(final_states={0})
    A.add_rule("a", (), 1)
    A.add_rule("b", (), 0)
    for x in (0, 1):
        for y in (0, 1):
            A.add_rule("c", (x, y), (x + y) % 2)
    return A


def _aumoins_un_a():
    from formlang.tree import TreeAutomaton
    A = TreeAutomaton(final_states={"yes"})
    A.add_rule("a", (), "yes")
    A.add_rule("b", (), "no")
    for x in ("yes", "no"):
        for y in ("yes", "no"):
            A.add_rule("c", (x, y), "yes" if "yes" in (x, y) else "no")
    return A


def test_produit_intersection():
    P = product(_parite(), _aumoins_un_a())
    assert P.accepts(Term("c", (Term("a"), Term("a")))) is True
    assert P.accepts(Term("c", (Term("a"), Term("b")))) is False


def test_shield_double_encodage_P45():
    from apps.shield.decomposer import (
        dangerous_and_double_encoded, enc, role, seq, sys,
    )
    P = dangerous_and_double_encoded()
    assert P.accepts(sys(seq(enc(), seq(enc(), role())))) is True
    assert P.accepts(sys(role())) is False
    assert P.accepts(seq(enc(), enc())) is False
