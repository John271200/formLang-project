"""Opérations comme VRAIES machines de Turing. À COMPLÉTER : tables ADD, SUB.
-> Jour 4 (E4.3)."""
from formlang.turing import TuringMachine

# ADD : m+n en unaire. On fusionne les deux blocs (le '+' devient un '1'),
# puis on retire un '1' (le surplus). Trace de référence : 11+1 -> 111.
ADD = TuringMachine(
    transitions={
        ("q0", "1"): ("q0", "1", "R"),   # avancer sur m
        ("q0", "+"): ("q1", "1", "R"),   # '+' -> '1' : fusion des deux blocs
        ("q1", "1"): ("q1", "1", "R"),   # avancer sur n
        ("q1", "_"): ("q2", "_", "L"),   # blanc : demi-tour
        ("q2", "1"): ("qf", "_", "S"),   # effacer le dernier '1' -> accepté
    },
    start="q0", accept={"qf"},
)

# BONUS Jour 4 : table MONOLITHIQUE de la multiplication (une seule MT, pas de
# composition). Entrée "1^n * 1^m" ; sortie : ruban ne contenant que 1^(n*m).
#
# Idée : pour chaque 1 du bloc n (marqué X), recopier tout le bloc m (marqué Y
# le temps d'un cycle) dans une zone résultat après un séparateur '=', puis
# démarquer les Y et recommencer ; à la fin, tout effacer sauf le résultat.
# Phases : qi/qr init ('=' en fin de ruban) ; q0 marquage d'un 1 de n ;
# q1..q5 copie du bloc m (un 1 à la fois) ; q6/q7 démarquage + retour ;
# q8/q9 nettoyage final.
MUL = TuringMachine(
    transitions={
        # qi/qr : écrire '=' après l'entrée, revenir au début
        ("qi", "1"): ("qi", "1", "R"),
        ("qi", "*"): ("qi", "*", "R"),
        ("qi", "_"): ("qr", "=", "L"),
        ("qr", "1"): ("qr", "1", "L"),
        ("qr", "*"): ("qr", "*", "L"),
        ("qr", "_"): ("q0", "_", "R"),
        # q0 : chercher le prochain 1 non marqué du bloc n
        ("q0", "X"): ("q0", "X", "R"),
        ("q0", "1"): ("q1", "X", "R"),   # un 1 de n consommé -> une copie de m
        ("q0", "*"): ("q8", "_", "L"),   # bloc n épuisé -> nettoyage
        # q1 : rejoindre le bloc m
        ("q1", "1"): ("q1", "1", "R"),
        ("q1", "*"): ("q2", "*", "R"),
        # q2 : chercher le prochain 1 non marqué du bloc m
        ("q2", "Y"): ("q2", "Y", "R"),
        ("q2", "1"): ("q3", "Y", "R"),   # marquer, aller écrire un 1 au résultat
        ("q2", "="): ("q6", "=", "L"),   # bloc m entièrement copié ce cycle
        # q3/q4 : traverser jusqu'au premier blanc après le résultat
        ("q3", "1"): ("q3", "1", "R"),
        ("q3", "="): ("q4", "=", "R"),
        ("q4", "1"): ("q4", "1", "R"),
        ("q4", "_"): ("q5", "1", "L"),   # écrire le 1 copié
        # q5 : revenir au dernier Y et reprendre la copie
        ("q5", "1"): ("q5", "1", "L"),
        ("q5", "="): ("q5", "=", "L"),
        ("q5", "Y"): ("q2", "Y", "R"),
        # q6 : démarquer les Y (fin d'un cycle), q7 : revenir au début du bloc n
        ("q6", "Y"): ("q6", "1", "L"),
        ("q6", "*"): ("q7", "*", "L"),
        ("q7", "1"): ("q7", "1", "L"),
        ("q7", "X"): ("q7", "X", "L"),
        ("q7", "_"): ("q0", "_", "R"),
        # q8 : effacer les X vers la gauche ; q9 : effacer m et '=' vers la droite
        ("q8", "X"): ("q8", "_", "L"),
        ("q8", "_"): ("q9", "_", "R"),
        ("q9", "_"): ("q9", "_", "R"),
        ("q9", "1"): ("q9", "_", "R"),
        ("q9", "="): ("qf", "_", "S"),   # seul le résultat 1^(n*m) subsiste
    },
    start="qi", accept={"qf"},
)

# SUB : m-n tronquée à 0. On efface une '1' de n (à droite) et une '1' de m
# (à gauche), en boucle, jusqu'à épuiser n ; si m s'épuise avant, résultat 0.
SUB = TuringMachine(
    transitions={
        # q0 : aller à l'extrémité droite
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "-"): ("q0", "-", "R"),
        ("q0", "_"): ("q1", "_", "L"),
        # q1 : examiner le symbole le plus à droite
        ("q1", "1"): ("q2", "_", "L"),   # une '1' de n : l'effacer, apparier à gauche
        ("q1", "-"): ("qf", "_", "S"),   # n épuisé : effacer '-' -> reste m-n
        # q2 : revenir à l'extrémité gauche
        ("q2", "1"): ("q2", "1", "L"),
        ("q2", "-"): ("q2", "-", "L"),
        ("q2", "_"): ("q3", "_", "R"),
        # q3 : examiner le symbole le plus à gauche
        ("q3", "1"): ("q0", "_", "R"),   # une '1' de m : l'effacer, recommencer
        ("q3", "-"): ("q5", "_", "R"),   # m épuisé (m < n) : résultat 0
        # q5 : m < n, tout effacer -> ruban vide
        ("q5", "1"): ("q5", "_", "R"),
        ("q5", "_"): ("qf", "_", "S"),
    },
    start="q0", accept={"qf"},
)
