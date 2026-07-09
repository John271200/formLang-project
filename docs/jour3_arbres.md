<!-- Charte IUT/IFRI — bleu #1A3A6B / orange #E07B20 -->
# Jour 3 — Automates d'arbres (pivot) + hash-consing

**Module produit :** `formlang/tree.py`
**Applications :** `apps/morpho/automaton.py`, `apps/shield/decomposer.py`,
`apps/hashcons/store.py`
**Tests cibles :** `tests/test_tree.py`, `tests/test_hashcons.py`
**Barème :** 5 pts (+2 bonus)

> ⚠️ Cadre éthique : volet Shield 100 % structurel (jetons abstraits).

## Contexte
C'est le **pivot** du projet. Une séquence plate `p p r s` ne dit pas **comment** le
mot est construit : la morphologie (préfixes, racine, suffixes) est **hiérarchique**,
donc naturellement un **arbre**. On généralise l'automate fini du jour 1 : au lieu de
suivre une **chaîne** d'états le long d'un mot, on **fusionne** les états des enfants
d'un nœud pour en calculer l'état. Deux applications très différentes — la morphologie
et le pare-feu structurel (Shield) — et le hash-consing instancieront **le même**
`formlang.tree`. Côté morphologie, la **découverte** d'affixes (`apps/morpho/
discover.py`) repose sur l'heuristique classique d'alternance d'un affixe avec ∅
(Harris 1955 ; Goldsmith 2001) : `X` et `X+suf` tous deux attestés ⇒ `suf` est un
suffixe candidat.

## Notions nouvelles du jour

### 1. Alphabet classé (ranked) et termes
Un **alphabet classé** associe à chaque symbole une **arité** (nombre d'enfants). Un
**terme** (= arbre) est soit une **feuille** (arité 0 : `root`, `prefix`, `suffix`,
`nil`, ou côté Shield `txt`, `enc`, `ovr`, `role`), soit un symbole d'arité `k`
appliqué à `k` sous-termes (`word(_, _)`, `rest(_, _)`, `seq(_, _)`, `sys(_)`…).
*(Dans le code : `Term(symbol, children, label)` — cf. `formlang/tree.py`.)*

### 2. L'automate d'arbres ascendant déterministe (BUTA)
Un **BUTA** est `A = (Q, Σ, Q_f, Δ)` où `Δ` contient des règles de la forme
`f(q₁, …, qₙ) → q` : « si le symbole `f` a ses `n` enfants dans les états `q₁…qₙ`,
alors ce nœud reçoit l'état `q` ». Une feuille `a` reçoit un état par une règle
`a → q`. On **accepte** un arbre si sa **racine** reçoit un état de `Q_f`.

**Intuition (c'est l'AFD généralisé).** Un AFD lit un mot de gauche à droite : c'est
le cas particulier « tout en arité 1 » (chaque nœud a un seul enfant → une chaîne).
Le BUTA, lui, part des **feuilles** et **remonte** vers la racine ; à un nœud à
plusieurs enfants, il ne « suit » pas une transition, il **combine** les états déjà
calculés des enfants. La mémoire n'est plus une position dans une chaîne, mais un
**état par nœud** de l'arbre.

**Exécution ascendante (bottom-up).** On étiquette chaque nœud en **post-ordre** :
d'abord tous les enfants, puis le nœud lui-même via la règle correspondante. Si un
enfant est rejeté, ou si aucune règle ne s'applique, le nœud est **REJETÉ**. *(Dans le
code : `TreeAutomaton.run` renvoie l'état de la racine ou `REJECT` ; `accepts` teste
l'appartenance à `Q_f`.)*

**Mini-exemple (Shield).** Feuilles : `role → ROLE`. Règle unaire : `sys(x) → SAFE`
si `x = SAFE`, sinon `DANGER`. Donc `sys(role())` remonte `ROLE` puis `DANGER` :
un « rôle » enfermé dans un bloc système est **bloqué**. Aucune notion de contenu
réel n'intervient — que de la **structure**.

### 3. Déterminisme et coût
`Δ` est une **table** indexée par `(symbole, états des enfants)` avec **au plus une**
image par clé : l'exécution est donc **unique** et une lecture de table coûte `O(1)`.
Comme `run` visite chaque nœud **une seule fois**, la reconnaissance est en `O(n)`
(`n` = nombre de nœuds) — à comparer à une recherche linéaire dans une liste de règles.

### 4. Pourquoi un AFD *de mots* échoue ici
La **frontière** (le *yield*, la suite des feuilles) d'un arbre **ne détermine pas**
sa structure : deux arbres différents peuvent avoir la même frontière (par ex. selon
que `pend` est la racine ou qu'un `a` initial est un préfixe). Un AFD ne lit que la
frontière : il est **aveugle** à la hiérarchie. Il faut un automate qui voit l'**arbre**.

### 5. Le théorème du yield (le pont vers le jour 1)
Réciproquement, l'ensemble des **frontières** des arbres acceptés par un automate
d'arbres régulier forme un **langage hors-contexte** ; et pour l'automate
morphologique, cette frontière est exactement `p* r s*` — le **langage régulier** du
jour 1. C'est le pont explicite **arbres (structure) ↔ mots (surface)**.

### 6. Clôture par intersection : le produit d'automates
Les langages d'arbres réguliers sont **clos par intersection**. On construit
l'automate **produit** `A₁ × A₂` dont les états sont des **paires** `(q₁, q₂)` ; chaque
règle s'applique **composante par composante**, et les états acceptants sont les paires
de finaux. Alors `L(A₁ × A₂) = L(A₁) ∩ L(A₂)`. *(Cf. `formlang.tree.product`.)*

### 7. Hash-consing : partager la structure (DAG)
Un arbre contient souvent des **sous-arbres identiques** (mêmes suffixes, mêmes
racines). Le **hash-consing** attribue à chaque sous-arbre structurellement distinct
un **identifiant unique** : deux sous-arbres identiques **partagent** le même id.
L'arbre devient un **DAG** (graphe orienté acyclique) — on ne stocke chaque structure
qu'**une fois**.

**Deux propriétés à retenir :** (a) **round-trip** — reconstruire depuis l'id redonne
l'arbre exact (`get(intern(t)) == t`) ; (b) **compression** — `1 − uniques/total`
mesure ce qu'on économise. Plus une langue est **agglutinante** (turc, finnois, avec
de longues chaînes de suffixes très partagées), plus le partage est élevé ; l'anglais
isolant partage moins. *(Cf. `apps/hashcons/store.py` ; c'est le pendant « arbres » des
dictionnaires morphologiques minimaux, Daciuk et al. 2000.)*

## A. Théorie (à rédiger) — 2 pts
**Q3.1 (0,5).** Montrer que `morpho_automaton` et `shield_automaton` sont
**déterministes** (au plus une règle par `(symbole, états enfants)`) — conséquence sur
l'unicité de l'exécution et le coût `O(n)`.
**Q3.2 (0,5).** Pourquoi un AFD **de mots** échoue à valider la structure ? Donner
deux arbres de même frontière.
**Q3.3 (0,5).** **Théorème du yield** : montrer que la frontière d'un mot
morphologique accepté est `p* r s*`, et le lien avec le langage régulier du jour 1.
**Q3.4 (0,5).** La **réduplication** (copie d'une partie de la racine) engendre-t-elle
un langage d'arbres **régulier** ? Intuition via `{ww}` (non régulier) et conséquence
pour un automate à états finis. *(Indice linguistique réel : Culy 1985 montre que la
réduplication du bambara sort même du hors-contexte.)*

## B. Pratique — 3 pts
**E3.1 (1).** `TreeAutomaton.run` (post-ordre ; `REJECT` si un enfant rejette ou si
aucune règle) + `accepts`. *Débloque `tests/test_tree.py`.*
**E3.2 (0,5).** `morpho_automaton` : règles Δ (feuilles `prefix/root/suffix/nil` ;
chaînes `prefixes`/`suffixes` ; `rest`, `word`). *Tests : `test_morpho_accept_et_classes`,
`test_morpho_rejet`.*
**E3.3 (0,5).** `_seq` + `shield_automaton` : feuilles `txt/enc→SAFE`, `ovr→OVR`,
`role→ROLE` ; `seq` fusionne (DANGER si l'un est DANGER ou si `{OVR,ROLE}`) ;
`frame`/`sys` : SAFE si enfant SAFE sinon DANGER. *Test : `test_shield_blocage`.*
**E3.4 (0,5).** `product(A₁,A₂)` : automate produit, `L = L(A₁) ∩ L(A₂)`. *Test :
`test_produit_intersection`.*
**E3.5 — hash-consing (0,5).** `apps/hashcons/store.py` : `CompactStore.intern`
(partage des sous-arbres identiques → même id) et `get` (round-trip exact) sur
`formlang.tree.Term`. *Tests : `test_round_trip_exact`,
`test_sous_arbres_identiques_partages`.*

> **Q3.5 (compression, dans le rapport).** `compression() = 1 − uniques/total`. Pour
> quelle famille de langues (anglais isolant vs turc/finnois agglutinants) attend-on le
> plus de partage de sous-arbres suffixaux ? Reportez vos **vrais** chiffres. *Test :
> `test_compression_positive`.*

## Sorties de référence
```
$ pytest -q tests/test_tree.py tests/test_hashcons.py
7 passed
$ python pipeline.py
== démo Shield (AttackDecomposer) ==
  OK      seq(txt,txt)
  OK      role (isolé)
  BLOQUÉ  sys(role)
  BLOQUÉ  seq(frame(ovr),txt)
  BLOQUÉ  sys(seq(txt,frame(role)))
```

## Mini-barème
| Item | Détail | Pts |
|---|---|---:|
| Q3.1–Q3.4 | déterminisme, yield, réduplication | 2 |
| E3.1 | `run`/`accepts` du BUTA | 1 |
| E3.2 | automate morphologique + `classify` | 0,5 |
| E3.3 | AttackDecomposer | 0,5 |
| E3.4 | produit (intersection) | 0,5 |
| E3.5 | hash-consing (intern + round-trip) | 0,5 |
| **Bonus** | infixation `s‹um›ulat` (étendre Δ) | +1 |
| **Bonus** | minimisation d'un BUTA (quotient par congruence) | +1 |

> *Gate (le plus important) :* les apps **instancient** `formlang.tree.TreeAutomaton`
> / `formlang.tree.Term`. Toute réimplémentation perd les points d'intégration.

## Références
**Automates d'arbres :**
- H. Comon *et al.*, *TATA — Tree Automata Techniques and Applications* (2007),
  ch. 1 — BUTA, déterminisme, clôtures (intersection par produit), minimisation.
  **(libre : `tata.gforge.inria.fr`)**
- F. Gécseg, M. Steinby, *Tree Automata* (1984 ; rééd. arXiv:1509.06233, 2015).
- J. W. Thatcher, J. B. Wright, *Math. Systems Theory* 2(1):57–81, 1968 *(fondateur)* ;
  J. Doner, *JCSS* 4(5):406–451, 1970.

**Morphologie (volet morpho, `discover`/segmentation) :**
- Z. S. Harris, « From phoneme to morpheme », *Language* 31(2):190–222, 1955 —
  découverte d'affixes par alternance (l'heuristique utilisée).
- J. Goldsmith, *Computational Linguistics* 27(2):153–198, 2001 — apprentissage non
  supervisé de la morphologie.
- K. R. Beesley, L. Karttunen, *Finite State Morphology*, CSLI, 2003 ;
  E. Roche, Y. Schabes (dir.), *Finite-State Language Processing*, MIT Press, 1997.

**Réduplication (Q3.4) :** C. Culy, « The complexity of the vocabulary of Bambara »,
*Linguistics and Philosophy* 8:345–351, 1985 — la réduplication sort du hors-contexte.

**Hash-consing (E3.5) :** J.-C. Filliâtre, S. Conchon, « Type-safe modular
hash-consing », *ML Workshop*, 2006 ; J. Daciuk *et al.*, *Computational Linguistics*
26(1), 2000 (pendant « mots » du DAG).

*Fin du jour 3 → `jour4_calculabilite.md`.*
