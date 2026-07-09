<!-- Charte IUT/IFRI — bleu #1A3A6B / orange #E07B20 -->
# Bibliographie (vérifiée)

> Reprise et consolidation des bibliographies des quatre TP d'origine. Les
> références marquées **(libre)** sont disponibles gratuitement en ligne. Toute
> borne de complexité citée dans le rapport doit renvoyer à l'une de ces sources
> (pas de constante « de mémoire »).

## Automates finis & langages formels (rappels)
- M. Sipser, *Introduction to the Theory of Computation*, 3ᵉ éd., Cengage, 2012.
- J. Hopcroft, R. Motwani, J. Ullman, *Introduction to Automata Theory, Languages,
  and Computation*, 3ᵉ éd., Pearson, 2006.
- J. Hopcroft, J. Ullman, *Introduction to Automata Theory, Languages, and
  Computation*, Addison-Wesley, 1979 — ch. 3 (pont AFD → arbre, minimisation).

## Automates d'arbres (cœur des jours 3 & 5)
- H. Comon, M. Dauchet, R. Gilleron, C. Löding, F. Jacquemard, D. Lugiez, S. Tison,
  M. Tommasi, *Tree Automata Techniques and Applications (TATA)*, 2007.
  **(libre : `tata.gforge.inria.fr`)** — la référence de base, complète.
- F. Gécseg, M. Steinby, *Tree Automata*, Akadémiai Kiadó, 1984 ; réédition
  **(libre : arXiv:1509.06233, 2015)**.
- J. W. Thatcher, J. B. Wright, « Generalized finite automata theory with an
  application to a decision problem of second-order logic », *Mathematical Systems
  Theory* 2(1):57–81, 1968. *(Article fondateur des automates d'arbres ascendants.)*
- J. Doner, « Tree acceptors and some of their applications », *Journal of Computer
  and System Sciences* 4(5):406–451, 1970.

## Applications des automates d'arbres
- M. Murata, D. Lee, M. Mani, K. Kawaguchi, « Taxonomy of XML schema languages using
  formal language theory », *ACM Trans. on Internet Technology* 5(4):660–704, 2005.
  *(Les schémas XML sont des langages d'arbres réguliers.)*
- A. V. Aho, M. Ganapathi, S. W. K. Tjiang, « Code generation using tree matching and
  dynamic programming », *ACM TOPLAS* 11(4):491–516, 1989. *(Filtrage d'arbres « twig ».)*
- A. Bouajjani, P. Habermehl, A. Rogalewicz, T. Vojnar, « Abstract Regular Tree Model
  Checking », *ENTCS* 149(1):37–48, 2006.

## Morphologie computationnelle (volet morpho)
- K. Koskenniemi, *Two-Level Morphology: A General Computational Model for Word-Form
  Recognition and Production*, Université d'Helsinki, 1983.
- K. R. Beesley, L. Karttunen, *Finite State Morphology*, CSLI Publications, 2003.
- Z. S. Harris, « From phoneme to morpheme », *Language* 31(2):190–222, 1955.
  *(Découverte d'affixes par alternance — l'heuristique de `discover`.)*
- J. Goldsmith, « Unsupervised learning of the morphology of a natural language »,
  *Computational Linguistics* 27(2):153–198, 2001.
- E. Roche, Y. Schabes (dir.), *Finite-State Language Processing*, MIT Press, 1997.

## Réduplication & limites (Q3.4)
- C. Culy, « The complexity of the vocabulary of Bambara », *Linguistics and
  Philosophy* 8:345–351, 1985. *(La réduplication peut dépasser le hors-contexte.)*
- B. Roark, R. Sproat, *Computational Approaches to Morphology and Syntax*, Oxford
  University Press, 2007.

## Hash-consing & partage de structure (DAG)
- J. Daciuk, S. Mihov, B. Watson, R. Watson, « Incremental construction of minimal
  acyclic finite-state automata », *Computational Linguistics* 26(1), 2000.
  *(Le pendant « mots » du DAG d'arbres.)*
- J.-C. Filliâtre, S. Conchon, « Type-safe modular hash-consing », *ML Workshop*, 2006.

## Calculabilité & machine universelle (jour 4)
- A. M. Turing, « On Computable Numbers, with an Application to the
  Entscheidungsproblem », *Proc. London Math. Soc.*, s2-42:230–265, 1936-37.
- M. Sipser, *op. cit.* — machine universelle, encodage, indécidabilité, réductions.
- F. C. Hennie, R. E. Stearns, « Two-Tape Simulation of Multitape Turing Machines »,
  *Journal of the ACM* 13(4):533–546, 1966. *(Ralentissement logarithmique — Q4.3.)*
- S. Arora, B. Barak, *Computational Complexity: A Modern Approach*, Cambridge
  University Press, 2009 — surcoûts de simulation, classes de complexité.
