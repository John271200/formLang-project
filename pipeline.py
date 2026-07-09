"""Pipeline intégrateur. À COMPLÉTER : assemblage.  -> Jour 5 (E5.1)."""
from __future__ import annotations
import argparse

from apps.shield.normalizer import leet_normalize
from apps.shield.detector import contains_or
from apps.shield.delimiters import well_parenthesized
from apps.morpho.automaton import morpho_automaton, classify
from apps.morpho.discover import discover, segment_to_tree
from apps.shield.decomposer import (
    shield_automaton, is_blocked, txt, ovr, role, seq, frame, sys,
)


def analyze_word(raw: str) -> dict:
    # E5.1 : normaliser (FST) puis détecter 'or' (AFD) puis délimiteurs (PDA).
    norm = leet_normalize(raw)
    return {
        "normalisé(FST)": norm,
        "facteur_or(AFD)": contains_or(norm),
        "délimiteurs_ok(PDA)": well_parenthesized(norm),
    }


def analyze_morpho(word: str, vocab: set) -> dict:
    # E5.1 : discover(PRE/SUF) -> segment_to_tree -> classify(BUTA).
    PRE = discover(vocab, prefix_side=True)
    SUF = discover(vocab, prefix_side=False)
    tree = segment_to_tree(word, PRE, SUF)
    A = morpho_automaton()
    return {"classe(BUTA)": classify(A, tree)}


def demo_shield() -> list:
    # FOURNI
    A = shield_automaton()
    cases = {
        "seq(txt,txt)": seq(txt(), txt()),
        "role (isolé)": role(),
        "sys(role)": sys(role()),
        "seq(frame(ovr),txt)": seq(frame(ovr()), txt()),
        "sys(seq(txt,frame(role)))": sys(seq(txt(), frame(role()))),
    }
    return [(name, is_blocked(A, t)) for name, t in cases.items()]


def main(argv=None):
    p = argparse.ArgumentParser(description="Pipeline formlang")
    p.add_argument("--word")
    p.add_argument("--morpho")
    args = p.parse_args(argv)
    if args.word:
        for k, v in analyze_word(args.word).items():
            print(f"{k:>22} : {v}")
    if args.morpho:
        from apps.morpho.corpora import corpus_A
        print(analyze_morpho(args.morpho, set(corpus_A())))
    if not args.word and not args.morpho:
        print("== démo Shield (AttackDecomposer) ==")
        for name, blocked in demo_shield():
            print(f"  {'BLOQUÉ ' if blocked else 'OK     '} {name}")


if __name__ == "__main__":
    main()
