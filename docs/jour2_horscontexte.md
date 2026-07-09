<!-- Charte IUT/IFRI — bleu #1A3A6B / orange #E07B20 -->
# Jour 2 — Étage hors-contexte : grammaires & automate à pile

**Modules produits :** `formlang/pda.py`, `formlang/cfg.py`
**Application :** `apps/shield/delimiters.py`
**Tests cibles :** `tests/test_cfg_nerode.py` (CFG), `tests/test_regular.py` (PDA)
**Barème :** 4 pts (+1 bonus)

> ⚠️ Cadre éthique : `Σ₃ = {a, o, r, [, ], (, )}`. Aucun contenu réel.

## Contexte
Les **faux délimiteurs** imitent un bloc `[ … ]` ou un cadre `( … )`,
éventuellement imbriqués. Vérifier l'imbrication **bien formée** = reconnaître un
langage de type **Dyck** : c'est **hors-contexte**, hors de portée d'un automate
fini. La nouveauté est la **pile** : mémoire non bornée mais disciplinée (LIFO).


## Notions nouvelles du jour

### 1. Le lemme de l'étoile (pompage)
C'est l'outil pour **prouver qu'un langage n'est pas régulier**. Il dit : si `L` est
régulier, il existe une longueur `p` telle que tout mot assez long se décompose
`xyz` (`|xy| ≤ p`, `y ≠ ε`) avec `xyⁱz ∈ L` pour tout `i`. Pour montrer qu'un langage
**n'est pas** régulier, on exhibe un mot que l'on **ne peut pas pomper** sans en sortir.
Intuition : un automate fini a une mémoire **bornée** ; il ne peut pas « compter »
indéfiniment.

### 2. La pile : une mémoire non bornée mais disciplinée
Le nouvel ingrédient de l'étage hors-contexte est la **pile** (LIFO). Contrairement à
l'état fini d'un AFD, elle est **non bornée** — mais on n'y accède qu'au **sommet**
(empiler / dépiler). C'est exactement ce qu'il faut pour suivre une **profondeur
d'imbrication** de délimiteurs `[ … ]`, `( … )`.

### 3. Grammaire hors-contexte (CFG)
Une CFG engendre les mots par **règles de réécriture** `A → …`. C'est le pendant
« génératif » du PDA (qui, lui, **reconnaît**). Les deux décrivent la même classe :
les **langages algébriques**. *(Cf. `CFG.generate`, `DelimiterPDA`.)*

### 4. Automate à pile (PDA)
Un **PDA** = automate fini **+ pile**. Ici on utilise l'**acceptation par pile vide** :
on empile sur chaque délimiteur ouvrant, on dépile sur le fermant s'il correspond au
sommet, et on accepte si la pile est vide à la fin. *(Cf. `DelimiterPDA.accepts`.)*

### 5. Ambiguïté & langage de Dyck
Une grammaire est **ambiguë** si un même mot admet **plusieurs** arbres de dérivation
(ex. `S → S S` non associée). Le langage des parenthésages bien formés est le **langage
de Dyck**, l'exemple canonique d'un langage hors-contexte non régulier.

## A. Théorie (à rédiger) — 2,5 pts
**Q2.1 (1,5).** Soit `D = { [ⁿ ]ⁿ | n ≥ 0 }`. Montrer **par le lemme de l'étoile**
que `D` n'est pas régulier. Conclure : le `SingularityDetector` (AFD) ne peut pas
vérifier l'imbrication.
**Q2.2 (0,5).** Donner une grammaire `G` des *prompts* bien parenthésés sur `Σ₃`
(`a, o, r` libres entre les délimiteurs).
**Q2.3 (0,5).** `G` est-elle **ambiguë** ? Si oui, deux arbres de dérivation pour
`aaa` ; proposer une grammaire non ambiguë équivalente.

## B. Pratique — 1,5 pt
**E2.1 (1).** `apps/shield/delimiters.py` : `well_parenthesized(w)` **avec une pile**
(acceptation par pile vide) en instanciant `formlang.pda.DelimiterPDA` : empiler sur
`[`/`(`, dépiler sur `]`/`)` ssi le sommet correspond, ignorer `a, o, r, e`.
*Test : `test_delimiters_pda`.*
**E2.2 (0,5).** `CFG.generate(max_len)` : énumérer les mots terminaux dérivables de
longueur ≤ `max_len` (BFS/DFS sur les formes sententielles). *Test :
`test_cfg_engendre_des_mots_equilibres`.*

> ⚠️ Piège (à discuter) : avec `S → S S | … | ε`, des formes purement
> non-terminales (`S`, `SS`, `SSS`…) ont **0 terminal** et ne sont jamais élaguées
> par la seule borne sur les terminaux → explosion. Borner aussi le nombre de
> non-terminaux (cf. corrigé).

## Sorties de référence
```
$ pytest -q tests/test_cfg_nerode.py tests/test_regular.py
... passed
```

## Mini-barème
| Item | Détail | Pts |
|---|---|---:|
| Q2.1 | pompage `{[ⁿ]ⁿ}` | 1,5 |
| Q2.2 | grammaire bien parenthésée | 0,5 |
| Q2.3 | ambiguïté + désambiguïsation | 0,5 |
| E2.1 | PDA `well_parenthesized` | 1 |
| E2.2 | génération bornée | 0,5 |
| **Bonus** | reconnaissance par **CYK** | +1 |

> *Gate :* `delimiters.py` instancie `formlang.pda.DelimiterPDA`.

## Références
- J. Hopcroft, R. Motwani, J. Ullman, *Introduction to Automata Theory…*, 3ᵉ éd., 2006
  — lemme de l'étoile, grammaires hors-contexte, automates à pile, ambiguïté.
- Langage de Dyck et équivalence PDA ↔ CFG : tout cours standard de théorie des langages.

*Fin du jour 2 → `jour3_arbres.md` (le pivot).*
