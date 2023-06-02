from .model.hierarchy import GlobalMark

# TODO try to find a better way than these hardcoded values...

# Here are the available choices for the user. These GlobalMark
# regroups several marks (like sub totals).
# To these attributes corresponds percentages on marks which are
# available below
VOLET1 = "Valeur globale"
VOLET2 = "Priorité d'invervention"

HIERARCHY_GLOBAL_MARKS = [
    GlobalMark(
        volet=VOLET1,
        attributes=[
            "Nulle à faible",
            "Moyenne",
            "Forte",
            "Très forte",
        ],
    ),
    GlobalMark(
        volet=VOLET1,
        rubrique="Interêt patrimonial",
        attributes=["Nul à faible", "Moyen", "Fort", "Très fort"],
    ),
    GlobalMark(
        volet=VOLET1,
        rubrique="Fonctions hydrologiques / biogéochimiques",
        attributes=["Non évaluées", "Nulles à faibles", "Moyennes", "Fortes"],
    ),
    GlobalMark(
        volet=VOLET1,
        rubrique="Valeurs socio-économiques",
        attributes=["Non évaluées", "Nulles à faibles", "Moyennes", "Fortes", "Très fortes"],
    ),
    GlobalMark(
        volet=VOLET2,
        attributes=["Nulle à faible", "Moyenne", "Forte", "Très forte"],
    ),
    GlobalMark(
        volet=VOLET2,
        rubrique="Statut et gestion",
        attributes=["Très fort", "Fort", "Moyen", "Nul à faible"],
    ),
    GlobalMark(
        volet=VOLET2,
        rubrique="État fonctionnel",
        attributes=[
            "Non évalué",
            "Pas ou peu dégradé",
            "Partiellement dégradé",
            "Dégradé",
            "Très dégradé",
        ],
    ),
]

# FIXME: ultra specific but no time to find a better
# way to do this...
# Correspondings percentages on marks
# Très fort	0	0% de la note max
# Fort	> 0% ≤ 25% de la note max
# Moyen	> 25% ≤ 50% de la note max
# Nul à faible > 50% de la note max

STATUS_COR_ATTR_PERC = {
    "Très fort": [0, 0],
    "Fort": [0, 25],
    "Moyen": [25, 50],
    "Nul à faible": [50, 100],
}

INT_PAT_COR_ATTR_PERC = {
    "Nul à faible": [0, 25],
    "Moyen": [25, 50],
    "Fort": [50, 75],
    "Très fort": [75, 100],
}

# Priorité
# Nulle à faible ≤ 25% de la note max
# Moyenne > 25% ≤ 50% de la note max
# Forte	> 50% ≤ 75% de la note max
# Très forte > 75% de la note max

OTHER_COR_ATTR_PERC = {
    "Nulle à faible": [0, 25],
    "Moyenne": [25, 50],
    "Forte": [50, 75],
    "Très forte": [75, 100],
}

# Corresponding label in database for these global marks
COR_VOLET = {
    VOLET1: "volet_1",
    VOLET2: "volet_2",
}

COR_RUB = {"Statut et gestion": "rub_statut", "Interêt patrimonial": "rub_interet_pat"}
