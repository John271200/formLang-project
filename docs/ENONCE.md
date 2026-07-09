<!-- Charte IUT/IFRI — bleu #1A3A6B / orange #E07B20 -->
# Projet intégrateur — De l'automate fini à la machine universelle

**Établissement :** IUT / IFRI — Master Génie Logiciel
**Module :** Théorie des langages & calculabilité
**Auteur du sujet :** Dr. Mêton ATINDEHOU
**Durée :** 1 semaine (5 jours + soutenance) · **Binôme** · **Langage :** Python 3.10+
**Bibliothèque à construire :** `formlang`

> Chapeau du projet. Les énoncés détaillés sont dans les cinq fiches
> `jour1_regulier.md` … `jour5_integration.md`. Le corrigé (`CORRIGE.md`) est
> réservé à l'enseignant.

## 1. De quoi parle ce projet ?
Reconnaître **une structure**, de plus en plus riche :
- un **motif** dans un mot → automate fini (régulier) ;
- des **délimiteurs imbriqués** → automate à pile (hors-contexte) ;
- une **configuration dans un arbre** → automate d'arbres ;
- **n'importe quel calcul** → machine de Turing, puis **machine universelle**.

## 2. Le fil rouge : la hiérarchie de Chomsky
| Jour | Étage | Pouvoir | Ce que vous construisez |
|---|---|---|---|
| 1 | Régulier | langages réguliers | AFD, AFN, transducteur fini |
| 2 | Hors-contexte | langages algébriques | grammaire, automate à pile |
| 3 | **Arbres** | langages d'arbres réguliers | automate d'arbres ascendant + hash-consing |
| 4 | Calculable | récursivement énumérable | machine de Turing, **machine universelle** |
| 5 | Transversal | — | minimisation, congruence, intégration |

Un mot est un arbre dégénéré (branche unaire) ; un automate fini est un automate
d'arbres tout en arité 1. Vous le **vérifierez en code**.

## 3. Une bibliothèque, quatre applications
Principe **noté** : les applications n'ont pas le droit de réécrire un automate ;
elles **instancient** ceux de `formlang`.
- `apps/morpho` — morphologie (BUTA) ;
- `apps/shield` — AttackDecomposer (BUTA, 100 % structurel) ;
- `apps/hashcons` — partage de structure (DAG) sur `formlang.tree.Term` ;
- `apps/mtu` — machine universelle U + calculatrice unaire **exécutée par U**.

## 4. Convention
Entiers en unaire : `n = 1ⁿ` (0 = mot vide). Opérateurs `+ - * /`. Blanc `_`.

## 5. ⚠️ Cadre éthique (volet Shield) — non négociable
Le volet Shield porte **exclusivement** sur la **structure formelle** d'un système
de **défense**. Tous les *prompts* sont des suites de **jetons abstraits**
(`a, o, r, e, [, ], (, )`). **Aucune attaque réelle, aucun contenu sensible.**
Tout rendu contenant un exemple d'attaque réelle est hors-sujet et pénalisé.

## 6. Organisation de la semaine
| Jour | Fiche | Cœur produit | Tests cibles |
|---|---|---|---|
| 1 | jour1_regulier | dfa, nfa, fst + détecteur, normaliseur | test_regular |
| 2 | jour2_horscontexte | pda, cfg + délimiteurs | test_cfg_nerode, test_regular |
| 3 | jour3_arbres | tree + morpho + shield + hashcons | test_tree, test_hashcons |
| 4 | jour4_calculabilite | turing, utm + mtu (interpréteur + calculatrice) | test_turing, test_calc |
| 5 | jour5_integration | pipeline, myhill_nerode | test_pipeline, test_cfg_nerode |

## 7. Barème global (sur 20, + bonus)
| Jour | Thème | Points |
|---|---|---:|
| 1 | Régulier & transducteurs | 4 |
| 2 | Hors-contexte (pompage, CFG, PDA) | 4 |
| 3 | **Arbres** (BUTA, morpho + Shield, produit) + hash-consing | 5 |
| 4 | Calculabilité (MT, MTU, calculatrice exécutée par U) | 4 |
| 5 | Intégration & Myhill–Nerode | 3 |
| **Total** | | **20** |
| Bonus | Thompson, CYK, minimisation BUTA, infixation, variante binaire | +6 |

**Règles « gate » (pénalité forte) :**
- *Anti-copier-coller* : une app qui **redéfinit** un automate au lieu de
  l'instancier perd les points d'intégration.
- *Honnêteté intellectuelle* : toute borne de complexité **démontrée ou
  référencée** (jamais « de mémoire »). Reportez vos **vrais** chiffres.

## 8. Livrables
1. **Dépôt Git** `NOM1_NOM2_formlang/` : `formlang/`, `apps/`, `pipeline.py`,
   `tests/` complétés et **qui passent** (`pytest -q` → `… passed`) ; sorties
   `pytest -q > out_tests.txt` et `python pipeline.py > out_demo.txt`.
2. **Rapport** (PDF, gabarit `RAPPORT_TEMPLATE.md`).
3. **Soutenance** (10 min) : démo bout-en-bout + un cas par étage.

Le code s'exécute avec **Python 3.10+ et `pytest` seulement**.

## 9. Pré-requis (acquis du cours)
Langages formels ; expressions régulières ; grammaires ; automates finis (AFD/AFN) ;
déterminisation ; minimisation ; notions de calculabilité. Le projet **introduit**
les automates d'arbres comme généralisation des automates finis, et la machine
universelle comme aboutissement.

## 10. Références (toutes réelles, vérifiées)
La bibliographie complète et thématique est dans **`BIBLIOGRAPHIE.md`**. Principales :
- M. Sipser, *Introduction to the Theory of Computation*, 3ᵉ éd., Cengage, 2012.
- J. Hopcroft, R. Motwani, J. Ullman, *Introduction to Automata Theory, Languages,
  and Computation*, 3ᵉ éd., Pearson, 2006.
- H. Comon *et al.*, *Tree Automata Techniques and Applications (TATA)*, 2007
  (libre : `tata.gforge.inria.fr`).
- F. Gécseg, M. Steinby, *Tree Automata*, 1984 (rééd. arXiv:1509.06233, 2015).
- F. C. Hennie, R. E. Stearns, « Two-Tape Simulation of Multitape Turing
  Machines », *J. ACM* 13(4), 1966.
- A. M. Turing, « On Computable Numbers… », *Proc. London Math. Soc.*, s2-42, 1936-37.
- S. Arora, B. Barak, *Computational Complexity: A Modern Approach*, Cambridge, 2009.

*Fin du chapeau. Passez à `jour1_regulier.md`.*
