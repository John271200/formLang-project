<!-- Charte IUT/IFRI — bleu #1A3A6B / orange #E07B20 -->
# Vue d'ensemble

## Le fil rouge
Une seule question, posée à cinq niveaux de difficulté croissante :
**« reconnaître une structure »**, depuis un facteur dans un mot jusqu'à
n'importe quel calcul. À chaque étage :

> plus la structure à reconnaître est riche, plus il faut de **mémoire** — et il
> existe un seuil (la machine universelle) où l'on gagne l'universalité mais où
> l'on **perd la décidabilité**.

## Pourquoi « intégrateur » et pas « trois TP » ?
On construit **un cœur unique** (`formlang/`) et on le **réutilise** :
- `apps/morpho` et `apps/shield` instancient **le même** `formlang.tree` (BUTA) ;
- `apps/hashcons` partage la structure des **mêmes** `formlang.tree.Term` ;
- `apps/mtu` n'écrit aucune boucle d'exécution : il décrit des **tables** et les
  fait tourner par `formlang.turing` / `formlang.utm`.

## Arbre de dépendances
```
apps/morpho   ─┐
apps/shield   ─┼─► formlang.tree
apps/hashcons ─┘
apps/shield   ───► formlang.dfa, formlang.fst, formlang.pda
apps/mtu      ───► formlang.turing ─► formlang.utm
pipeline.py   ───► (toutes les apps)
```

## Compétences évaluées
1. Implémenter ET tester chaque famille d'automate.
2. **Justifier** pourquoi un étage inférieur échoue (pompage, mémoire bornée).
3. **Composer** des reconnaisseurs (produit d'arbres, composition de FST,
   sous-machines de Turing exécutées par U).
4. Relier théorie et code par des **traces**.
5. Discuter les **limites** (indécidabilité de l'arrêt).

## Lecture des fiches
`jour1` régulier+FST → `jour2` hors-contexte → `jour3` arbres + hash-consing
(pivot) → `jour4` calculabilité + machine universelle → `jour5` intégration +
Myhill–Nerode.
