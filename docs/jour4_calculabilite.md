<!-- Charte IUT/IFRI — bleu #1A3A6B / orange #E07B20 -->
# Jour 4 — Calculabilité : machine de Turing & machine universelle

**Modules produits :** `formlang/turing.py`, `formlang/utm.py`
**Application :** `apps/mtu/` (`machines.py`, `calculator.py`, `interpreter.py`)
**Tests cibles :** `tests/test_turing.py`, `tests/test_calc.py`
**Barème :** 4 pts (+1 bonus)

## Contexte
Aux jours précédents, la mémoire grandissait par paliers : **aucune** mémoire au-delà
de l'état (automate fini), puis une **pile** (hors-contexte), puis un **arbre**
d'états (jour 3). Aujourd'hui on lève la dernière limite : une mémoire **libre**,
lisible **et** ré-inscriptible n'importe où. C'est la machine de Turing — le modèle
de référence de « ce qui est calculable ». Et une fois qu'on a ce modèle, une idée
vertigineuse apparaît : **une seule** machine peut en simuler **toutes** les autres,
si on lui donne leur description en entrée. C'est la machine **universelle**, ancêtre
direct du processeur et de l'interpréteur.

## Notions nouvelles du jour

### 1. La machine de Turing (MT)
Une MT déterministe est un septuplet **M = (Q, Σ, Γ, δ, q₀, ␣, F)** :
- `Q` états, `q₀` initial, `F ⊆ Q` acceptants ;
- `Σ` alphabet d'entrée, `Γ ⊇ Σ` alphabet de ruban, `␣ ∈ Γ` le **blanc** ;
- `δ : Q × Γ → Q × Γ × {L, R, S}` la fonction de transition.

**Intuition.** Imaginez un ruban infini de cases, une **tête** qui lit/écrit une case
à la fois et se déplace à gauche (`L`), à droite (`R`) ou reste (`S`). À chaque pas :
« dans l'état `q`, je lis `a` → j'écris `b`, je bouge de `d`, je passe en `q'` ».
La différence essentielle avec la pile du jour 2 : ici on peut **relire et réécrire**
le passé autant de fois qu'on veut. C'est ce qui donne toute la puissance.

**Configuration.** L'état complet du calcul se note `α q β` : contenu de ruban `α`
à gauche, état `q`, contenu `β` à partir de la tête. Le calcul est la suite
`C₀ ⊢ C₁ ⊢ …`. La machine **s'arrête** quand elle atteint un état de `F` (ou qu'il
n'y a plus de transition applicable). *(Dans le code, le ruban est un `dict {i: symbole}`,
extensible des deux côtés — cf. `formlang/turing.py`.)*

**Mini-exemple.** La table `ADD` (jour 4, code) transforme `1ⁿ+1ᵐ` en `1ⁿ⁺ᵐ` :
elle traverse `n`, change le `+` en `1` (fusion), traverse `m`, fait demi-tour et
efface **un** `1` pour compenser. Une opération arithmétique **est** une MT.

### 2. Le codage d'une machine : ⟨M⟩
Puisqu'une MT n'est qu'une **table finie** de quintuplets, on peut l'écrire comme une
**chaîne de caractères** `⟨M⟩` (numéroter états et symboles, lister les
`(q, a) → (q', b, d)`). Un programme devient une **donnée**. Ce codage doit être
**injectif** (deux machines distinctes → chaînes distinctes) et **décodable** (on
reconstruit `M` à partir de `⟨M⟩`). *(Dans le code : `encode`/`decode`, linéarisation
JSON triée — cf. `formlang/utm.py`.)*

### 3. La machine universelle U — le programme enregistré
Une machine **universelle** `U` prend en entrée `⟨M⟩ ## w` et **simule** `M` sur `w` :
`U` accepte ⟺ `M` accepte, et le ruban final de `U` code celui de `M`. Autrement dit,
`U` est un **interpréteur** : elle lit un programme (`⟨M⟩`) rangé sur son ruban et
l'exécute pas à pas.

**Pourquoi c'est fondateur.** C'est exactement l'idée de von Neumann : programme et
données dans la **même** mémoire. Votre CPU est une machine universelle matérielle ;
Python est une machine universelle logicielle. Dans ce TP, `UniversalInterpreter`
(`apps/mtu/interpreter.py`) n'écrit **aucune** boucle de ruban : il encode `M` puis
délègue à `U` — la calculatrice est donc littéralement **exécutée par** la machine
universelle.

**Cycle de simulation (invariant).** À tout instant, `U` maintient sur son ruban :
`⟨M⟩` (figée), l'état simulé, le ruban simulé, la position de tête simulée. Un cycle =
*lire* le symbole courant → *chercher* la transition dans `⟨M⟩` → *écrire* → *déplacer*
→ *mettre à jour* l'état. On prouve la correction par récurrence sur le nombre de pas.

### 4. La thèse de Church–Turing
« Toute fonction **effectivement calculable** est calculable par une machine de
Turing. » Ce n'est **pas un théorème** (la notion de « effectivement calculable » est
informelle), mais une **thèse** solidement étayée : des modèles inventés indépendamment
— λ-calcul (Church), fonctions récursives (Gödel–Herbrand–Kleene), machines RAM — se
révèlent tous **équivalents** à la MT. C'est pourquoi la MT sert de définition de
référence du calcul.

### 5. Composer des machines (macro-machines)
On n'a pas besoin d'une table monolithique pour `×` ou `÷` : on les obtient en
**enchaînant** des MT plus simples (multiplication = additions répétées ; division =
soustractions répétées). Composer des MT est légitime — c'est précisément ce que fait
`U` quand elle orchestre des sous-programmes. *(Cf. `apps/mtu/calculator.py`.)*

### 6. La limite : l'indécidabilité
Le revers de l'universalité : **on gagne tout le pouvoir de calcul, mais on perd la
décidabilité**. Le **problème de l'arrêt** (`HALT` : « `M` s'arrête-t-elle sur `w` ? »)
est **indécidable** (Turing, 1936). Par réduction, « `U` s'arrête sur `⟨M⟩##w` » l'est
aussi. Universel ne veut pas dire omniscient : `U` peut tout **simuler**, mais aucune
machine ne peut **prédire** en général si une autre va s'arrêter.

> **Convention (unaire).** `n = 1ⁿ` (donc `0` = mot vide). Opérateurs `+ - * /`, blanc `_`.

## A. Théorie (à rédiger) — 2 pts
**Q4.1 (0,5).** Détailler le schéma d'encodage `⟨M⟩` (numéroter états/symboles,
linéariser `δ`) et **justifier** qu'il est injectif et décodable.
**Q4.2 (0,5).** Décrire `U` et son **cycle de simulation** (invariant + un tour complet).
**Q4.3 (0,5).** **Surcoût** (à **sourcer**, sans constante inventée) : multi-ruban en
`O(t·|⟨M⟩|)` ; multi→mono ≤ quadratique ; citer Hennie–Stearns (ralentissement
logarithmique atteignable).
**Q4.4 (0,5).** **Indécidabilité** : réduction depuis `HALT` montrant que
« `U` s'arrête sur `⟨M⟩##w` » est indécidable. Commenter « universel ≠ omniscient ».

## B. Pratique — 2 pts
**E4.1 (0,5).** `TuringMachine.run` (ruban `dict`, arrêt sur état final / transition
absente, option `trace`). *Test : `test_trace_disponible`.*
**E4.2 (0,5).** `encode` / `decode` (réciproques exactes) + `UniversalTM.run` (décode
puis délègue à `TuringMachine.run`). *Tests : `test_round_trip_encodage`,
`test_utm_simule_comme_la_machine`.*
**E4.3 (0,75).** Tables `ADD`/`SUB` (vraies MT) + `Calculatrice` (`+`,`-` par les MT ;
`*`,`/` par **composition** ; `chainer`). *Tests : `test_add_sub_machines_directes`,
`test_calculatrice_exhaustif`, `test_chainage`, `test_division_par_zero`.*
**E4.4 (0,25).** `apps/mtu/interpreter.py` : `UniversalInterpreter.run(M, w)` encode
`M` puis **délègue à `UniversalTM`** ; `addition_via_utm`/`soustraction_via_utm`
calculent **par U**. *Test : `test_interpreteur_universel`.*

> **À expliquer dans le rapport (lecture d'une table δ).** Grille : *où suis-je* (état =
> phase + mémoire finie), *que vois-je*, *que fais-je* (écris, bouge), *où vais-je*.
> Pour `SUB`, justifier : les phases `q0…q4` ; pourquoi `(q0,X)→R` et `(q1,X)→R` (la
> table doit gérer ses **propres marques**) ; le barrage de `n` **droite→gauche** (sortie
> contiguë) ; la fin de `m` détectée par un **blanc** (le ruban compte, pas un compteur).
> Donner les traces `2+1` et `3−2`, et les cas-limites `n=m→0`, `m=0→n`, `n=0`.

## Sorties de référence
```
$ pytest -q tests/test_turing.py tests/test_calc.py
... passed
>>> from apps.mtu.calculator import Calculatrice
>>> c = Calculatrice()
>>> c.addition(3,2), c.soustraction(4,2), c.multiplication(3,2), c.division(7,3)
(5, 2, 6, (2, 1))
>>> from apps.mtu.interpreter import addition_via_utm
>>> addition_via_utm(3, 2)
5
```

## Mini-barème
| Item | Détail | Pts |
|---|---|---:|
| Q4.1–Q4.4 | encodage, cycle U, surcoût **sourcé**, indécidabilité | 2 |
| E4.1 | MT générique (ruban, arrêt, trace) | 0,5 |
| E4.2 | encode/decode + `UniversalTM` | 0,5 |
| E4.3 | calculatrice (tests exhaustifs + chaînage) | 0,75 |
| E4.4 | interpréteur universel (calc exécutée par U) | 0,25 |
| **Bonus** | table **monolithique** de `*` validée par le simulateur | +1 |

> *Gate :* `apps/mtu` ne réécrit pas de boucle de MT — il décrit des **tables** et les
> fait tourner via `formlang.turing` / `formlang.utm`. *Honnêteté :* surcoût **référencé**.

## Références
- A. M. Turing, « On Computable Numbers… », *Proc. London Math. Soc.*, s2-42, 1936-37.
- M. Sipser, *Introduction to the Theory of Computation* — MTU, encodage,
  indécidabilité, réductions. *(À consulter pour Q4.3/Q4.4 avant de citer une borne.)*
- F. C. Hennie, R. E. Stearns, « Two-Tape Simulation of Multitape Turing Machines »,
  *J. ACM* 13(4):533–546, 1966 — pour Q4.3 : citer la source, **pas** de constante de mémoire.
- S. Arora, B. Barak, *Computational Complexity: A Modern Approach*, Cambridge, 2009.

*Fin du jour 4 → `jour5_integration.md`.*
