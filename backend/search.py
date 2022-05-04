from sqlalchemy import func
from sqlalchemy.sql.expression import select

from geonature.utils.env import DB
from geonature.core.ref_geo.models import LAreas, BibAreasTypes
from pypnnomenclature.models import TNomenclatures

from .model.zh_schema import (
    TZH,
    THydroArea,
    TRiverBasin,
    TOwnership,
    TManagementStructures,
    TManagementPlans,
    TFunctions,
)
from .api_error import ZHApiError


def main_search(query, json):
    sdage = json.get("sdage")
    if sdage is not None:
        query = filter_sdage(query, sdage)

    nameorcode = json.get("nameorcode")
    if nameorcode is not None:
        query = filter_nameorcode(query, nameorcode)

    ensemble = json.get("ensemble")
    if ensemble is not None:
        query = filter_ensemble(query, ensemble)

    area = json.get("area")
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

    evaluations = json.get("evaluations")
    if evaluations is not None:
        query = filter_evaluations(query, evaluations)

    return query


def filter_sdage(query, json: dict):
    ids = [obj.get("id_nomenclature") for obj in json]
    return query.filter(TZH.id_sdage.in_(ids))


def filter_nameorcode(query, json: dict):
    # Checks if the code OR the name is already taken
    if json:
        return query.filter((TZH.code.contains(json)) | (TZH.main_name.contains(json)))
    return query


def filter_ensemble(query, json: dict):
    ids = [obj.get("id_nomenclature") for obj in json]
    return query.filter(TZH.id_site_space.in_(ids))


def filter_area_size(query, json: dict):
    ha = json.get("ha", None)
    symbol = json.get("symbol", None)
    if symbol is None or ha is None:
        return query

    # TZH.area is already in ha
    if symbol == "=":
        query = query.filter(TZH.area == ha)
    elif symbol == "≥":
        query = query.filter(TZH.area >= ha)
    elif symbol == "≤":
        query = query.filter(TZH.area <= ha)

    return query


def filter_area(query, json: dict, type_code: str):
    codes = [area.get("code", None) for area in json]
    if any(code is None for code in codes):
        return query

    # Filter on departments
    subquery = (
        DB.session.query(LAreas)
        .with_entities(
            LAreas.area_name, LAreas.geom, LAreas.id_type, BibAreasTypes.type_code
        )
        .join(BibAreasTypes, LAreas.id_type == BibAreasTypes.id_type)
        .filter(BibAreasTypes.type_code == type_code)
        .filter(LAreas.area_code.in_(codes))
        .subquery()
    )

    # Filter on geom.
    # Need to use (c) on subquery to get the column
    query = query.filter(
        func.ST_Transform(func.ST_SetSRID(TZH.geom, 4326), 2154).ST_Intersects(
            subquery.c.geom
        )
    )

    return query


def filter_hydro(query, json):
    codes = [area.get("code", None) for area in json]

    if codes and all(code is not None for code in codes):
        subquery = (
            DB.session.query(THydroArea)
            .with_entities(THydroArea.id_hydro, THydroArea.geom)
            .filter(THydroArea.id_hydro.in_(codes))
            .subquery()
        )

        # SET_SRID does not return a valid geom...
        query = query.filter(
            func.ST_Transform(func.ST_SetSRID(TZH.geom, 4326), 4326).ST_Intersects(
                subquery.c.geom
            )
        )

    return query


def filter_basin(query, json):
    codes = [area.get("code", None) for area in json]

    if codes is not None:
        subquery = (
            DB.session.query(TRiverBasin)
            .with_entities(
                TRiverBasin.id_rb,
                TRiverBasin.geom,
            )
            .filter(TRiverBasin.id_rb.in_(codes))
            .subquery()
        )
        # SET_SRID does not return a valid geom...
        query = query.filter(
            func.ST_Transform(func.ST_SetSRID(TZH.geom, 4326), 4326).ST_Intersects(
                subquery.c.geom
            )
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
        DB.session.query(TFunctions.id_zh)
        .with_entities(
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
        .filter_by(
            id_type=select([func.ref_nomenclatures.get_id_nomenclature_type(type_)])
        )
    )

    if ids_fct and all(id_ is not None for id_ in ids_fct):
        subquery = subquery.filter(TFunctions.id_function.in_(ids_fct))

    if ids_qual and all(id_ is not None for id_ in ids_qual):
        subquery = subquery.filter(TFunctions.id_qualification.in_(ids_qual))

    if ids_conn and all(id_ is not None for id_ in ids_conn):
        subquery = subquery.filter(TFunctions.id_knowledge.in_(ids_conn))

    query = query.filter(TZH.id_zh == subquery.subquery().c.id_zh).distinct()

    return query


def filter_statuts(query, json: dict):
    ids_statuts = [f.get("id_nomenclature") for f in json.get("statuts", [])]

    if ids_statuts and ids_statuts:
        subquery = (
            DB.session.query(TOwnership.id_zh)
            .with_entities(TOwnership.id_zh, TOwnership.id_status)
            .filter(TOwnership.id_status.in_(ids_statuts))
        )
        query = query.filter(TZH.id_zh == subquery.subquery().c.id_zh).distinct()

    return query


def filter_plans(query, json: dict):

    ids_plans = [f.get("id_nomenclature") for f in json.get("plans", [])]

    if ids_plans and all(id_ is not None for id_ in ids_plans):
        subquery = (
            DB.session.query(TManagementStructures.id_zh)
            .with_entities(
                TManagementPlans.id_nature,
                TManagementPlans.id_structure,
                TManagementStructures.id_structure,
                TManagementStructures.id_zh,
            )
            .join(
                TManagementStructures,
                TManagementPlans.id_structure == TManagementStructures.id_structure,
            )
            .filter(TManagementPlans.id_nature.in_(ids_plans))
        )

        query = query.filter(TZH.id_zh == subquery.subquery().c.id_zh).distinct()

    return query


def filter_evaluations(query, json: dict):
    ids_hydros = [f.get("id_nomenclature") for f in json.get("hydros", [])]
    ids_bios = [f.get("id_nomenclature") for f in json.get("bios", [])]
    ids_menaces = [f.get("id_nomenclature") for f in json.get("menaces", [])]

    if ids_hydros and all(id_ is not None for id_ in ids_hydros):
        query = query.filter(TZH.id_diag_hydro.in_(ids_hydros))

    if ids_bios and all(id_ is not None for id_ in ids_bios):
        query = query.filter(TZH.id_diag_bio.in_(ids_bios))

    if ids_menaces and all(id_ is not None for id_ in ids_menaces):
        query = query.filter(TZH.id_thread.in_(ids_menaces))

    return query
