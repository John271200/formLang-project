<!-- Charte IUT/IFRI — bleu #1A3A6B / orange #E07B20 -->
# Jour 5 — Intégration & Myhill–Nerode

**Modules produits :** `pipeline.py`, `formlang/myhill_nerode.py`
**Tests cibles :** `tests/test_pipeline.py`, `tests/test_cfg_nerode.py`
**Barème :** 3 pts (+1 bonus)

## Contexte
Le dernier jour a deux visages. D'abord **assembler** : jusqu'ici chaque étage
vivait seul (un AFD ici, un PDA là, un automate d'arbres ailleurs) ; on les fait
maintenant **coopérer** dans un `pipeline` qui traite une entrée de bout en bout.
Ensuite **boucler la boucle théorique** : on revient sur la toute première question
du projet — « combien d'états faut-il vraiment ? » — avec l'outil qui y répond
exactement, la **congruence de Myhill–Nerode**. C'est le pont entre le code (l'AFD
minimal du jour 1) et la théorie (pourquoi 3 états, ni plus ni moins).

## Notions nouvelles du jour

### 1. Intégration : composer la pile complète
Un `pipeline` ne réinvente rien : il **appelle les applications**, qui elles-mêmes
**instancient** le cœur `formlang`. Deux chaînes de traitement l'illustrent :
- `analyze_word(raw)` : **normaliser** (FST leet) → **détecter** le facteur `or`
  (AFD) → **valider** les délimiteurs (PDA). Trois étages de la hiérarchie enchaînés
  sur une même entrée.
- `analyze_morpho(word, vocab)` : **découvrir** les affixes du vocabulaire
  (heuristique d'alternance, Harris/Goldsmith) → **segmenter** le mot en
  `(préfixes, racine, suffixes)` → **construire l'arbre** et le **classer** par le
  BUTA (`BARE/SUFFIXED/PREFIXED/CIRCUMFIXED`).

**Ce qu'on évalue ici** n'est pas un nouvel algorithme, mais l'**architecture** : le
respect de la règle « gate » (le pipeline orchestre, il ne reprogramme aucun automate)
et la cohérence des interfaces entre modules.

### 2. La congruence de Myhill–Nerode
On dit que deux mots `u` et `v` sont **équivalents pour `L`**, noté `u ≈_L v`, s'ils
sont **indistinguables par la suite** : pour **tout** suffixe `w`,
`uw ∈ L ⟺ vw ∈ L`. Autrement dit, une fois qu'on a lu `u` ou `v`, l'avenir (tout ce
qu'on pourra encore accepter) est **identique**.

**Intuition.** Deux mots sont dans la même classe s'ils laissent l'automate « dans le
même état d'esprit » : peu importe ce qui a été lu, seule compte la **capacité future**
d'accepter. Cette relation est une équivalence **invariante à droite**
(`u ≈_L v ⟹ ua ≈_L va`) : c'est ce qui permet d'en faire les **états** d'un automate.

**Le théorème (le cœur du jour).** `L` est régulier **si et seulement si** `≈_L` a un
**nombre fini** de classes ; et ce nombre — l'**indice** de `≈_L` — est **exactement**
le nombre d'états de l'**AFD minimal** de `L`. La minimisation du jour 1 n'était donc
rien d'autre que le **calcul de ces classes** : fusionner deux états, c'est constater
que les mots qui y mènent sont indistinguables.

**Mini-exemple (le fil rouge se referme).** Pour `L₁ = {w contient « or »}`, il y a
**exactement trois** classes : (A) « rien de spécial », (B) « je viens de voir un `o`,
un `r` me suffirait », (C) « j'ai déjà vu `or`, c'est joué ». Trois classes ⟺ trois
états de l'AFD minimal du jour 1. *(Dans le code : `nerode_classes` regroupe les mots
par **signature** sur une batterie de suffixes témoins — cf. `formlang/myhill_nerode.py`.)*

**Pourquoi une approximation par suffixes témoins ?** Comparer sur *tous* les suffixes
est infini ; en pratique on choisit un **jeu fini de suffixes distinctifs** suffisant
pour séparer les classes attendues. C'est une version **testable** du critère théorique.

### 3. Ouverture : Myhill–Nerode pour les arbres (bonus)
La même idée se transpose aux arbres : deux sous-arbres sont équivalents s'ils
donnent le même verdict **dans tout contexte** (arbre « à trou »). C'est le fondement
de la **minimisation d'un automate d'arbres**, et le lien direct avec le hash-consing
du jour 3 (partager, c'est identifier des sous-structures équivalentes).

## A. Théorie (à rédiger) — 1 pt
**Q5.1 (0,5).** Énoncer la congruence de Myhill–Nerode ; relier le **nombre de classes**
de `L₁` au nombre d'états de l'AFD minimal du jour 1.
**Q5.2 (0,5).** Expliquer le critère « indistinguables par tous les suffixes témoins »
et son lien avec la **fusion d'états** à la minimisation.

## B. Pratique — 2 pts
**E5.1 (1).** `pipeline.py` : `analyze_word(raw)` (FST → AFD → PDA) et
`analyze_morpho(word, vocab)` (`discover` PRE/SUF → `segment_to_tree` → `classify`).
*Tests : `test_pipeline_word`, `test_pipeline_morpho`.*
**E5.3 (1).** `nerode_classes(accepts, words, suffixes)` : regrouper les mots par
signature `tuple(accepts(w+s) for s in suffixes)`. *Test : `test_nerode_trois_classes`.*

## Sorties de référence
```
$ pytest -q
28 passed                      # version enseignant (toutes apps complétées)
$ python pipeline.py --word 4or
                  brut : 4or
        normalisé(FST) : aor
       facteur_or(AFD) : True
   délimiteurs_ok(PDA) : True
$ python pipeline.py --morpho mufafak
{'mot': 'mufafak', 'classe(BUTA)': 'PREFIXED'}
```

## Mini-barème
| Item | Détail | Pts |
|---|---|---:|
| Q5.1–Q5.2 | Myhill–Nerode + lien minimisation | 1 |
| E5.1 | pipeline (mot + morpho) bout-en-bout | 1 |
| E5.3 | classes de Nerode | 1 |
| **Bonus** | mesure hash-consing sur 10 000 mots (total/uniques/compression) | +1 |

> *Gate :* le pipeline **appelle les apps** (qui instancient le cœur) ; il ne
> reprogramme aucun automate.

## Références
- J. Hopcroft, R. Motwani, J. Ullman, *Introduction to Automata Theory…* — théorème
  de Myhill–Nerode, minimisation.
- H. Comon *et al.*, *TATA* (2007) — congruence de Myhill–Nerode pour les arbres (bonus).
- (Bonus mesure) J.-C. Filliâtre, S. Conchon, « Type-safe modular hash-consing », 2006.

*Fin du projet. Rendez le dépôt + le rapport (gabarit `RAPPORT_TEMPLATE.md`).*
