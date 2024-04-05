import unicodedata

from ref_geo.models import BibAreasTypes, LAreas
from geonature.utils.env import DB
from pypnnomenclature.models import TNomenclatures
from sqlalchemy import and_, desc, func, or_
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import aliased
from utils_flask_sqla.generic import GenericQuery

from .api_error import ZHApiError
from .constants import (
    COR_RUB,
    COR_VOLET,
    INT_PAT_COR_ATTR_PERC,
    OTHER_COR_ATTR_PERC,
    STATUS_COR_ATTR_PERC,
    VOLET1,
    VOLET2,
)
from .model.zh_schema import (
    TZH,
    BibHierCategories,
    BibHierPanes,
    CorRbRules,
    CorZhNotes,
    TFunctions,
    THydroArea,
    TManagementPlans,
    TManagementStructures,
    TOwnership,
    TRiverBasin,
    TRules,
)


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def main_search(query, json):
    for key in json.keys():
        if key in TZH.__table__.columns:
            query = query.where(getattr(TZH, key) == json[key])
    sdage = json.get("sdage")
    if sdage is not None:
        query = filter_sdage(query, sdage)

    nameorcode = json.get("nameorcode")
    if nameorcode is not None:
        query = filter_nameorcode(query, nameorcode)

    ensemble = json.get("ensemble")
    if ensemble is not None:
        query = filter_ensemble(query, ensemble)

    area = json.get("ha_area")
    if area is not None:
        query = filter_area_size(query, area)

    departement = json.get("departement")
    communes = json.get("communes")

    if departement and communes is None:
        query = filter_area(query, departement, type_code="DEP")
    if communes is not None:
        query = filter_area(query, communes, type_code="COM")

    # TODO: Bassin versant and Zones hydrographiques
    basin = json.get("basin")
    zones = json.get("zones")

    if basin is not None and zones is None:
        query = filter_basin(query, basin)
    if zones is not None:
        query = filter_hydro(query, zones)

    # --- Advanced search
    hydro = json.get("hydro")
    if hydro is not None:
        query = filter_fct(query, hydro, "FONCTIONS_HYDRO")

    bio = json.get("bio")
    if bio is not None:
        query = filter_fct(query, bio, "FONCTIONS_BIO")

    socio = json.get("socio")
    if socio is not None:
        query = filter_fct(query, socio, "VAL_SOC_ECO")

    interet = json.get("interet")
    if interet is not None:
        query = filter_fct(query, interet, "INTERET_PATRIM")

    statuts = json.get("statuts")
    if statuts is not None:
        query = filter_statuts(query, statuts)
        query = filter_plans(query, statuts)
        query = filter_strategies(query, statuts)

    evaluations = json.get("evaluations")
    if evaluations is not None:
        query = filter_evaluations(query, evaluations)

    # --- Hierarchy search
    hierarchy = json.get("hierarchy")
    if hierarchy is not None and basin is not None:
        query = filter_hierarchy(query, json=hierarchy, basin=basin[0].get("name"))

    return query


def filter_sdage(query, json: dict):
    ids = [obj.get("id_nomenclature") for obj in json]
    return query.where(TZH.id_sdage.in_(ids))


def filter_nameorcode(query, json: dict):
    # Checks if the code OR the name is already taken
    if json:
        json = strip_accents(json)
        # TODO: create index with another function to make unaccent immutable
        unaccent_fullname = func.lower(func.unaccent(TZH.fullname))
        subq = (
            select(TZH.id_zh, func.similarity(unaccent_fullname, json).label("idx_trgm"))
            .where(unaccent_fullname.ilike("%" + json + "%"))
            .order_by(desc("idx_trgm"))
            .subquery()
        )
        return query.where(TZH.id_zh == subq.c.id_zh)
    return query


def filter_ensemble(query, json: dict):
    ids = [obj.get("id_site_space") for obj in json]
    return query.where(TZH.id_site_space.in_(ids))


def filter_area_size(query, json: dict):
    ha = json.get("ha", None)
    symbol = json.get("symbol", None)
    if symbol is None or ha is None:
        return query

    # TZH.area is already in ha
    if symbol == "=":
        query = query.where(TZH.area == ha)
    elif symbol == "≥":
        query = query.where(TZH.area >= ha)
    elif symbol == "≤":
        query = query.where(TZH.area <= ha)

    return query


def filter_area(query, json: dict, type_code: str):
    codes = [area.get("code", None) for area in json]
    if any(code is None for code in codes):
        return query

    # Filter on departments
    subquery = (
        select(LAreas)
        .with_only_columns(LAreas.area_name, LAreas.geom, LAreas.id_type, BibAreasTypes.type_code)
        .join(BibAreasTypes, LAreas.id_type == BibAreasTypes.id_type)
        .where(BibAreasTypes.type_code == type_code)
        .where(LAreas.area_code.in_(codes))
        .subquery()
    )

    # Filter on geom.
    # Need to use (c) on subquery to get the column
    query = query.where(
        func.ST_Transform(func.ST_SetSRID(TZH.geom, 4326), 2154).ST_Intersects(subquery.c.geom)
    )

    return query


def filter_hydro(query, json):
    codes = [area.get("code", None) for area in json]

    if codes and all(code is not None for code in codes):
        subquery = (
            select(THydroArea)
            .with_only_columns(THydroArea.id_hydro, THydroArea.geom)
            .where(THydroArea.id_hydro.in_(codes))
            .subquery()
        )

        # SET_SRID does not return a valid geom...
        query = query.where(
            func.ST_Transform(func.ST_SetSRID(TZH.geom, 4326), 4326).ST_Intersects(subquery.c.geom)
        )

    return query


def filter_basin(query, json):
    codes = [area.get("code", None) for area in json]

    if codes is not None:
        subquery = (
            select(TRiverBasin)
            .with_only_columns(
                TRiverBasin.id_rb,
                TRiverBasin.geom,
            )
            .where(TRiverBasin.id_rb.in_(codes))
            .subquery()
        )
        # SET_SRID does not return a valid geom...
        query = query.where(
            func.ST_Transform(func.ST_SetSRID(TZH.geom, 4326), 4326).ST_Intersects(subquery.c.geom)
        )

    return query


def filter_fct(query, json: dict, type_: str):
    known_types = [
        "FONCTIONS_HYDRO",
        "FONCTIONS_BIO",
        "INTERET_PATRIM",
        "VAL_SOC_ECO",
        "FONCTIONS_QUALIF",
        "FONCTIONS_CONNAISSANCE",
    ]
    if type_ not in known_types:
        raise ZHApiError(message="Filter type not appropriate", code=500)

    ids_fct = [f.get("id_nomenclature") for f in json.get("functions", [])]
    ids_qual = [f.get("id_nomenclature") for f in json.get("qualifications", [])]
    ids_conn = [f.get("id_nomenclature") for f in json.get("connaissances", [])]

    subquery = (
        select(TFunctions.id_zh)
        .with_only_columns(
            TFunctions.id_zh,
            TFunctions.id_function,
            TFunctions.id_qualification,
            TFunctions.id_knowledge,
            TNomenclatures.id_type,
            TNomenclatures.id_nomenclature,
            TZH.id_zh.label("id"),
        )
        .join(TFunctions, TFunctions.id_zh == TZH.id_zh)
        .join(TNomenclatures, TNomenclatures.id_nomenclature == TFunctions.id_function)
        .filter_by(id_type=select(func.ref_nomenclatures.get_id_nomenclature_type(type_)))
    )

    if ids_fct and all(id_ is not None for id_ in ids_fct):
        subquery = subquery.where(TFunctions.id_function.in_(ids_fct))

    if ids_qual and all(id_ is not None for id_ in ids_qual):
        subquery = subquery.where(TFunctions.id_qualification.in_(ids_qual))

    if ids_conn and all(id_ is not None for id_ in ids_conn):
        subquery = subquery.where(TFunctions.id_knowledge.in_(ids_conn))

    query = query.where(TZH.id_zh == subquery.subquery().c.id_zh).distinct()

    return query


def filter_statuts(query, json: dict):
    ids_statuts = [f.get("id_nomenclature") for f in json.get("statuts", [])]

    if ids_statuts:
        subquery = (
            select(TOwnership.id_zh)
            .with_only_columns(TOwnership.id_zh, TOwnership.id_status)
            .where(TOwnership.id_status.in_(ids_statuts))
        )
        query = query.where(TZH.id_zh == subquery.subquery().c.id_zh).distinct()

    return query


def filter_plans(query, json: dict):
    ids_plans = [f.get("id_nomenclature") for f in json.get("plans", [])]

    if ids_plans and all(id_ is not None for id_ in ids_plans):
        subquery = (
            select(TManagementStructures.id_zh)
            .with_only_columns(
                TManagementPlans.id_nature,
                TManagementPlans.id_structure,
                TManagementStructures.id_structure,
                TManagementStructures.id_zh,
            )
            .join(
                TManagementStructures,
                TManagementPlans.id_structure == TManagementStructures.id_structure,
            )
            .where(TManagementPlans.id_nature.in_(ids_plans))
        )

        query = query.where(TZH.id_zh == subquery.subquery().c.id_zh).distinct()

    return query


def filter_strategies(query, json: dict):
    ids_strategies = [f.get("id_nomenclature") for f in json.get("strategies", [])]
    if ids_strategies:
        query = query.where(TZH.id_strat_gestion.in_(ids_strategies)).distinct()
    return query


def filter_evaluations(query, json: dict):
    ids_hydros = [f.get("id_nomenclature") for f in json.get("hydros", [])]
    ids_bios = [f.get("id_nomenclature") for f in json.get("bios", [])]
    ids_menaces = [f.get("id_nomenclature") for f in json.get("menaces", [])]

    if ids_hydros and all(id_ is not None for id_ in ids_hydros):
        query = query.where(TZH.id_diag_hydro.in_(ids_hydros))

    if ids_bios and all(id_ is not None for id_ in ids_bios):
        query = query.where(TZH.id_diag_bio.in_(ids_bios))

    if ids_menaces and all(id_ is not None for id_ in ids_menaces):
        query = query.where(TZH.id_thread.in_(ids_menaces))

    return query


def filter_hierarchy(query, json: dict, basin: str):
    global_notes = get_global_notes(basin)

    and_ = json.get("and", False)
    hierarchy = json.get("hierarchy")
    if hierarchy is None:
        return query
    filters = []
    for hier in hierarchy:
        knowledges = hier.get("knowledges")
        if knowledges is None:
            attributes = hier.get("attributes", [])
            # Little trick to know if the attribute is a GlobalMark or not
            if any(attribute.get("cor_rule_id") is None for attribute in attributes):
                subquery = generate_global_attributes_subquery(
                    attributes=attributes, global_notes=global_notes
                )
            else:
                subquery = generate_attributes_subquery(attributes=attributes)
        else:
            subquery = generate_attributes_subquery(attributes=knowledges)

        filters.append(TZH.id_zh.in_(subquery))
    if not and_:
        query = query.where(or_(*filters))
    else:
        query = query.where(*filters)
    return query


def get_global_notes(basin: str):
    if basin is None:
        raise AttributeError("Basin must not be None")
    query = GenericQuery(
        DB=DB,
        tableName="rb_notes_summary",
        schemaName="pr_zh",
        filters={"bassin_versant": basin, "orderby": "bassin_versant"},
        limit=1,
    )

    results = query.return_query()

    return [note for note in results.get("items", [])][0]


def generate_global_attributes_subquery(attributes: list, global_notes: dict):
    """
    Generates the subquery taking care only on "GlobalMarks"
    """
    subquery = select(CorZhNotes.id_zh)
    note_query = func.sum(CorZhNotes.note)

    subquery = subquery.join(CorRbRules, CorRbRules.cor_rule_id == CorZhNotes.cor_rule_id).join(
        TRules, TRules.rule_id == CorRbRules.rule_id
    )
    volet = attributes[0].get("volet")
    rub = attributes[0].get("rubrique")
    attribute_list = [attribute.get("attribut") for attribute in attributes]

    if rub is None:
        subquery = generate_volet(
            subquery=subquery,
            volet=volet,
            attribute_list=attribute_list,
            global_notes=global_notes,
            note_query=note_query,
        )
    else:
        subquery = generate_rub(
            subquery=subquery,
            rub=rub,
            attribute_list=attribute_list,
            global_notes=global_notes,
            note_query=note_query,
        )

    return subquery.group_by(CorZhNotes.id_zh).subquery()


def generate_volet(subquery, volet: str, attribute_list: list, global_notes: dict, note_query):
    if volet.lower() in [VOLET1.lower(), VOLET2.lower()]:
        subquery = subquery.join(BibHierPanes, BibHierPanes.pane_id == TRules.pane_id).where(
            BibHierPanes.label == volet
        )
        subquery = generate_volet_subquery(
            subquery=subquery,
            volet=volet,
            attribute_list=attribute_list,
            global_notes=global_notes,
            note_query=note_query,
        )
    else:
        raise AttributeError(volet)

    return subquery


def generate_volet_subquery(subquery, volet, attribute_list: list, global_notes: dict, note_query):
    """
    Subquery for "volet"
    """
    volet_nb = COR_VOLET[volet]
    max_note = global_notes[volet_nb]
    and_query = []
    for attribute in attribute_list:
        min_, max_ = (item * max_note / 100.0 for item in OTHER_COR_ATTR_PERC[attribute])
        and_query.append(and_(note_query > min_, note_query <= max_))

    # Necessary to have "having" instead of "filter" by because we cannot have a "filter" with
    # a "func" inside it (which is the case with the note_query)
    return subquery.having(or_(*and_query))


def generate_rub(subquery, rub: str, attribute_list: list, global_notes: dict, note_query):
    subquery = subquery.join(BibHierCategories, BibHierCategories.cat_id == TRules.cat_id).where(
        BibHierCategories.label == rub
    )
    # Takes care of the several attributes choosen by the user.
    # All the and queries on func.sum are compiled into and_query to be able to put an "or"
    # between each of them
    and_query = []

    # TODO: to make more generic...
    if rub.lower() == "statut et gestion":
        rub_nb = COR_RUB[rub]
        max_note = global_notes[rub_nb]
        for attribute in attribute_list:
            min_, max_ = (item * max_note / 100 for item in STATUS_COR_ATTR_PERC[attribute])
            and_query.append(and_(note_query > min_, note_query <= max_))
    elif rub.lower() == "interêt patrimonial":
        rub_nb = COR_RUB[rub]
        max_note = global_notes[rub_nb]
        for attribute in attribute_list:
            min_, max_ = (item * max_note / 100 for item in INT_PAT_COR_ATTR_PERC[attribute])
            and_query.append(and_(note_query > min_, note_query <= max_))
    elif rub.lower() in ["valeurs socio-économiques", "état fonctionnel"]:
        for attribute in attribute_list:
            if attribute in ["Non évalué", "Non évaluées"]:
                # subquery = subquery.filter(CorZhNotes.note == 10)
                and_query.append(note_query == 20)
            elif attribute in ["Pas ou peu dégradé", "Nulles à faibles"]:
                and_query.append(and_(note_query != 20, note_query >= 0, note_query <= 25))
            elif attribute in ["Partiellement dégradé", "Moyennes"]:
                and_query.append(and_(note_query > 25, note_query <= 50))
            elif attribute in ["Dégradé", "Fortes"]:
                and_query.append(and_(note_query > 50, note_query <= 75))
            elif attribute in ["Très dégradé", "Très fortes"]:
                and_query.append(and_(note_query > 75, note_query <= 100))
            else:
                raise AttributeError(attribute)
    elif rub.lower() in ["fonctions hydrologiques / biogéochimiques"]:
        for attribute in attribute_list:
            if attribute in ["Non évaluées"]:
                and_query.append(note_query == 45)
            elif attribute in ["Nulles à faibles"]:
                and_query.append(and_(note_query >= 0, note_query <= 33))
            elif attribute in ["Moyennes"]:
                and_query.append(and_(note_query != 45, note_query > 33, note_query <= 66))
            elif attribute in ["Fortes"]:
                and_query.append(and_(note_query > 66, note_query <= 100))
            else:
                raise AttributeError(attribute)
    else:
        raise AttributeError(rub)

    # Necessary to have having instead of filter as specified before
    return subquery.having(or_(*and_query))


def generate_attributes_subquery(attributes: list):
    subquery = select(CorZhNotes.id_zh)
    attribute_ids = []
    note_type_ids = []
    cor_rule_ids = []
    notes = []
    for attribute in attributes:
        attribute_ids.append(attribute["id_attribut"])
        note_type_ids.append(attribute["note_type_id"])
        cor_rule_ids.append(attribute["cor_rule_id"])
        notes.append(attribute["note"])

    # TODO: see if all of these are usefull... Are cor_rule_id with note sufficient?
    subquery = (
        subquery.where(CorZhNotes.attribute_id.in_(attribute_ids))
        .where(CorZhNotes.note_type_id.in_(note_type_ids))
        .where(CorZhNotes.cor_rule_id.in_(cor_rule_ids))
        .where(CorZhNotes.note.in_(notes))
    )

    return subquery.subquery()
