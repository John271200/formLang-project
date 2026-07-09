from apps.morpho.automaton import build_word
from apps.hashcons.store import CompactStore


def test_round_trip_exact():
    t = build_word(["re"], "structur", ["ation"])
    s = CompactStore()
    nid = s.intern(t)
    assert s.get(nid) == t


def test_sous_arbres_identiques_partages():
    s = CompactStore()
    a = build_word([], "structur", ["ation"])
    b = build_word([], "structur", ["ation"])
    assert s.intern(a) == s.intern(b)


def test_compression_positive():
    s = CompactStore()
    s.intern(build_word([], "structur", ["ation"]))
    s.intern(build_word(["re"], "structur", ["ation"]))
    assert s.unique_nodes() < s.total_nodes()
    assert s.compression() > 0.0
