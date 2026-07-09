<!-- Charte IUT/IFRI — bleu #1A3A6B / orange #E07B20 -->
# Jour 1 — Étage régulier : automates finis & transducteurs

**Modules produits :** `formlang/dfa.py`, `formlang/nfa.py`, `formlang/fst.py`
**Applications :** `apps/shield/detector.py`, `apps/shield/normalizer.py`
**Tests cibles :** `tests/test_regular.py` · **Barème :** 4 pts (+1 bonus)

> ⚠️ Cadre éthique : alphabet abstrait `{a, o, r}` (+ chiffres *leet*). Aucun contenu réel.

## Contexte
Le premier réflexe d'un détecteur est de repérer un **motif** : « le mot contient
le facteur `or` » — un langage **régulier**. Avant de détecter, on **normalise**
(défaire le *leetspeak* `4→a, 0→o…`) : une relation **rationnelle** réalisée par un
**transducteur fini**. Rappel : un mot `a₁…aₙ` est un arbre dégénéré (branche unaire) ;
l'automate fini est le cas « tout en arité 1 » du jour 3.


## Notions nouvelles du jour

### 1. AFD et AFN
Un **automate fini déterministe** (AFD) lit un mot de gauche à droite ; dans chaque
état, chaque lettre mène à **un** état. Un **automate fini non déterministe** (AFN)
autorise **plusieurs** transitions (voire des ε-transitions) : plusieurs « chemins »
coexistent, et on accepte s'il en **existe** un acceptant. L'AFN est souvent plus
petit et plus lisible ; l'AFD est directement exécutable.

### 2. Déterminisation (construction des sous-ensembles)
Tout AFN se convertit en AFD équivalent : un état de l'AFD est un **ensemble** d'états
de l'AFN (ceux où l'on « pourrait être »). On part de la ε-fermeture de l'état initial,
et pour chaque lettre on calcule l'ensemble atteignable. *(Cf. `NFA.to_dfa`.)*

### 3. Minimisation (raffinement de Moore)
Deux états sont **équivalents** s'ils acceptent exactement les mêmes suffixes. La
minimisation **fusionne** ces états : on part de la partition finaux / non-finaux et
on **raffine** tant que deux états d'un même bloc mènent à des blocs différents.
Le résultat est l'AFD **minimal** (unique). *(Cf. `DFA.minimize` ; lien direct avec
Myhill–Nerode, jour 5.)*

### 4. Transducteur fini (FST)
Un AFD **reconnaît** ; un **transducteur** **traduit** : à chaque transition, il émet
une sortie. On l'utilise pour **normaliser** (défaire le *leetspeak* `4→a, 0→o…`).
La relation réalisée est **rationnelle**. *(Cf. `SequentialFST.transduce`, `leet_fst`.)*

### 5. One-way vs two-way
Un transducteur **one-way** lit l'entrée une fois, de gauche à droite, avec une
mémoire **bornée** (états finis). Le renversement `w ↦ wᴿ` lui est **impossible** (il
faudrait mémoriser tout `w` avant d'émettre). Une tête **two-way** (qui peut revenir en
arrière) le permet. C'est un premier exemple concret de **limite due à la mémoire** —
le fil rouge du projet.

## A. Théorie (à rédiger) — 2 pts
On pose `Σ = {a, o, r}` et `L₁ = { w | w contient le facteur « or » }`.

**Q1.1 (0,5).** Donner une expression régulière dénotant `L₁`.
**Q1.2 (1).** Construire un AFN pour `L₁`, le **déterminiser** (sous-ensembles)
puis le **minimiser** (Moore/Hopcroft). Donner la table de l'AFD minimal, le
**dessiner**, indiquer le nombre d'états.
**Q1.3 (0,5).** Soit `L₁' = { w | w contient un o suivi, pas forcément
immédiatement, d'un r }`. Donner sa regex, expliquer la différence avec `L₁`,
préciser l'inclusion `L₁ ⊆ L₁'`.

## B. Pratique — 2 pts
**E1.1 (0,75).** `apps/shield/detector.py` : implémenter `contains_or(w)` **sous
forme d'AFD** (table `δ`, pas l'opérateur `in`). États `A` (init), `B` (`o` vu,
« armé »), `C` (accepté, absorbant). Compléter aussi `DFA.run` / `DFA.accepts`.
*Test : `test_detector_or`.*
**E1.2 (0,5).** `DFA.minimize` (raffinement de Moore). *Test : `test_minimisation_3_etats`.*
**E1.3 (0,5).** `NFA.to_dfa` (construction des sous-ensembles). *Test :
`test_nfa_to_dfa_equivalence`.*
**E1.4 (0,25).** `leet_fst` + `SequentialFST.transduce` (identité sur les symboles
non listés). *Tests : `test_leet_idempotent`, `test_fst_composition`.*

> **Miroir (théorie, dans le rapport).** Le renversement `w ↦ wᴿ` est-il réalisable
> par un FST **one-way** ? Justifier (mémoire bornée), puis expliquer pourquoi un
> transducteur **two-way** le permet. (`reverse_twoway` est fourni.)

## Sorties de référence
```
$ pytest -q tests/test_regular.py
7 passed
```

## Mini-barème
| Item | Détail | Pts |
|---|---|---:|
| Q1.1–Q1.3 | regex, AFN→AFD→min, facteur vs sous-séquence | 2 |
| E1.1 | détecteur AFD (`contains_or`) | 0,75 |
| E1.2 | minimisation 3 états | 0,5 |
| E1.3 | déterminisation | 0,5 |
| E1.4 | FST leet + composition | 0,25 |
| **Bonus** | construction de Thompson (regex → AFN explicite) | +1 |

> *Gate :* `detector.py` instancie `formlang.dfa.DFA` ; il ne teste pas `"or" in w`.

## Références
- M. Sipser, *Introduction to the Theory of Computation*, 3ᵉ éd., 2012 — réguliers,
  déterminisation, minimisation.
- J. Hopcroft, R. Motwani, J. Ullman, *Introduction to Automata Theory…*, 3ᵉ éd., 2006.
- Pour le miroir (one-way vs two-way) : tout cours standard sur les transducteurs
  rationnels et les transducteurs bidirectionnels.

*Fin du jour 1 → `jour2_horscontexte.md`.*
