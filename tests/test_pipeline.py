from pipeline import analyze_word, analyze_morpho, demo_shield
from apps.morpho.corpora import corpus_A, corpus_B


def test_pipeline_word():
    r = analyze_word("4or")
    assert r["normalisé(FST)"] == "aor"
    assert r["facteur_or(AFD)"] is True
    assert r["délimiteurs_ok(PDA)"] is True


def test_pipeline_morpho():
    assert analyze_morpho("fafak", set(corpus_B()))["classe(BUTA)"] == "BARE"
    assert analyze_morpho("fafaklar", set(corpus_B()))["classe(BUTA)"] == "SUFFIXED"
    assert analyze_morpho("mufafak", set(corpus_A()))["classe(BUTA)"] == "PREFIXED"


def test_demo_shield_verdicts():
    v = dict(demo_shield())
    assert v["sys(role)"] is True
    assert v["role (isolé)"] is False
