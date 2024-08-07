import sys

from geonature.utils.env import DB
from pypn_habref_api.models import CorespHab, Habref, TypoRef
from pypnnomenclature.models import BibNomenclaturesTypes, TNomenclatures
from sqlalchemy import and_
from sqlalchemy.sql import select

from .api_error import ZHApiError
from .model.zh_schema import (
    BibCb,
    CorChStatus,
    CorImpactTypes,
    CorMainFct,
    CorProtectionLevelType,
    CorSdageSage,
    CorUrbanTypeRange,
    Nomenclatures,
)


def get_sage_list():
    try:
        return [
            {
                int(sdage_id): [
                    {
                        "id_nomenclature": sage.CorSdageSage.id_sage,
                        "mnemonique": sage.TNomenclatures.mnemonique,
                    }
                    for sage in CorSdageSage.get_sage_by_id(sdage_id)
                ]
            }
            for sdage_id in CorSdageSage.get_id_sdage_list()
        ]
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_sage_list_error", details=str(exc_type) + ": " + str(e.with_traceback(tb))
        )


def get_corine_biotope():
    try:
        return [
            {
                "CB_code": cb.BibCb.lb_code,
                "CB_label": cb.Habref.lb_hab_fr,
                "front_name": cb.BibCb.lb_code + " - " + cb.Habref.lb_hab_fr,
                "CB_humidity": cb.BibCb.humidity,
                "CB_is_ch": cb.BibCb.is_ch,
            }
            for cb in BibCb.get_label()
        ]
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_corine_biotope_error",
            details=str(exc_type) + ": " + str(e.with_traceback(tb)),
        )


def get_ch(lb_code):
    try:
        CH_typo = DB.session.scalar(select(TypoRef.cd_typo).where(TypoRef.cd_table == "TYPO_CH"))
        CB_typo = DB.session.scalar(
            select(TypoRef.cd_typo).where(TypoRef.cd_table == "TYPO_CORINE_BIOTOPES")
        )
        # get cd_hab_sortie list from lb_code of selected Corine Biotope
        cd_hab_sortie = DB.session.scalar(
            select(Habref.cd_hab).where(and_(Habref.lb_code == lb_code, Habref.cd_typo == CB_typo))
        )
        # get all cd_hab_entre corresponding to cd_hab_sortie
        q_cd_hab_entre = DB.session.scalars(
            select(CorespHab).where(
                and_(CorespHab.cd_hab_sortie == cd_hab_sortie, CorespHab.cd_typo_entre == CH_typo)
            )
        ).all()
        # get list of cd_hab_entre/lb_code/lb_hab_fr for each cahier habitat
        ch = []
        for q in q_cd_hab_entre:
            hab = DB.session.scalar(select(Habref).where(Habref.cd_hab == q.cd_hab_entre))
            ch.append(
                {
                    "cd_hab": q.cd_hab_entre,
                    "front_name": hab.lb_code + " - " + hab.lb_hab_fr,
                    "lb_code": hab.lb_code,
                    "lb_hab_fr": hab.lb_hab_fr,
                    "priority": DB.session.scalar(
                        select(CorChStatus.priority)
                        .where(CorChStatus.lb_code == hab.lb_code)
                        .distinct()
                    ),
                }
            )
        return ch
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_cahier_habitat_error",
            details=str(exc_type) + ": " + str(e.with_traceback(tb)),
        )


def set_select_list(cd, mnemo):
    return cd + "- " + mnemo.capitalize()


def get_impact_list():
    try:
        return [
            {
                "id_cor_impact_types": impact.CorImpactTypes.id_cor_impact_types,
                "id_nomenclature": impact.CorImpactTypes.id_impact,
                "mnemonique": set_select_list(
                    impact.TNomenclatures.cd_nomenclature, impact.TNomenclatures.mnemonique
                ),
                "id_category": impact.CorImpactTypes.id_impact_type,
                "category": get_impact_category(impact),
            }
            for impact in CorImpactTypes.get_impacts()
        ]
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_impact_list_error",
            details=str(exc_type) + ": " + str(e.with_traceback(tb)),
        )


def get_impact_category(impact):
    # get mnemonique of id_impact_type
    if impact.CorImpactTypes.id_impact_type is not None:
        return DB.session.scalar(
            select(TNomenclatures.mnemonique).where(
                TNomenclatures.id_nomenclature == impact.CorImpactTypes.id_impact_type
            )
        )
    return "Aucun"


def get_function_list(mnemo):
    try:
        # get id_type of mnemo (ex : 'FONCTIONS_HYDRO') in BibNomenclatureTypes
        id_type_main_function = DB.session.scalar(
            select(BibNomenclaturesTypes.id_type).where(BibNomenclaturesTypes.mnemonique == mnemo)
        )

        # get list of TNomenclatures ids by id_type
        nomenclature_ids = [
            nomenc.id_nomenclature
            for nomenc in DB.session.scalars(
                select(TNomenclatures).where(TNomenclatures.id_type == id_type_main_function)
            ).all()
        ]

        return [
            {
                "id_nomenclature": function.CorMainFct.id_function,
                "mnemonique": function.TNomenclatures.mnemonique,
                "id_category": function.CorMainFct.id_main_function,
                "category": DB.session.scalar(
                    select(TNomenclatures.mnemonique).where(
                        TNomenclatures.id_nomenclature == function.CorMainFct.id_main_function
                    )
                ).upper(),
            }
            for function in CorMainFct.get_functions(nomenclature_ids)
        ]
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_function_list_error",
            details=str(exc_type) + ": " + str(e.with_traceback(tb)),
        )


def get_all_function_list(mnemo):
    try:
        # get id_type of mnemo (ex : 'FONCTIONS_HYDRO') in BibNomenclatureTypes
        id_type_main_function = DB.session.execute(
            select(BibNomenclaturesTypes.id_type).where(BibNomenclaturesTypes.mnemonique == mnemo)
        ).scalar_one()

        # get list of TNomenclatures ids by id_type
        nomenclature_ids = [
            nomenc.id_nomenclature
            for nomenc in DB.session.scalars(
                select(TNomenclatures).where(TNomenclatures.id_type == id_type_main_function)
            ).all()
        ]

        return [
            {
                "id_nomenclature": function.CorMainFct.id_function,
                "mnemonique": function.TNomenclatures.mnemonique,
                "id_category": function.CorMainFct.id_main_function,
                "category": DB.session.execute(
                    select(TNomenclatures.mnemonique).where(
                        TNomenclatures.id_nomenclature == function.CorMainFct.id_main_function
                    )
                )
                .scalar_one()
                .upper(),
            }
            for function in CorMainFct.get_all_functions(nomenclature_ids)
        ]
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_all_function_list_error",
            details=str(exc_type) + ": " + str(e.with_traceback(tb)),
        )


def get_urban_docs():
    try:
        return [
            {
                "id_nomenclature": doc.id_nomenclature,
                "mnemonique": doc.mnemonique,
                "type_classement": CorUrbanTypeRange.get_range_by_doc(doc.id_nomenclature),
            }
            for doc in Nomenclatures.get_nomenclature_info("TYP_DOC_COMM")
        ]
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_urban_docs_error",
            details=str(exc_type) + ": " + str(e.with_traceback(tb)),
        )


def get_protections():
    try:
        return [
            {
                "id_protection_status": protection.id_protection_status,
                "mnemonique_status": DB.session.scalar(
                    select(TNomenclatures.mnemonique).where(
                        TNomenclatures.id_nomenclature == protection.id_protection_status
                    )
                ),
                "id_protection_level": protection.id_protection_level,
                "mnemonique_level": DB.session.scalar(
                    select(TNomenclatures.mnemonique).where(
                        TNomenclatures.id_nomenclature == protection.id_protection_level
                    )
                ),
                "category": get_protection_category(protection),
                "category_id": protection.id_protection_type,
            }
            for protection in DB.session.scalars(
                select(CorProtectionLevelType).order_by(CorProtectionLevelType.id_protection)
            ).all()
        ]
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_protections_error",
            details=str(exc_type) + ": " + str(e.with_traceback(tb)),
        )


def get_protection_category(protection):
    if protection.id_protection_type is not None:
        return DB.session.scalar(
            select(TNomenclatures.mnemonique).where(
                TNomenclatures.id_nomenclature == protection.id_protection_type
            )
        )
    return "Autre"


def get_nomenc(config):
    nomenc_info = {}
    for mnemo in config:
        if mnemo in ["FONCTIONS_HYDRO", "FONCTIONS_BIO", "INTERET_PATRIM"]:
            mnemo_all = mnemo + "_all"
            nomenc_info = {**nomenc_info, mnemo: get_function_list(mnemo)}
            nomenc_info = {**nomenc_info, mnemo_all: get_all_function_list(mnemo)}
        elif mnemo == "IMPACTS":
            nomenc_info = {**nomenc_info, mnemo: get_impact_list()}
        elif mnemo == "CORINE_BIO":
            nomenc_info = {**nomenc_info, mnemo: get_corine_biotope()}
        elif mnemo == "SDAGE-SAGE":
            nomenc_info = {**nomenc_info, mnemo: get_sage_list()}
        elif mnemo == "TYP_DOC_COMM":
            nomenc_info = {**nomenc_info, mnemo: get_urban_docs()}
        elif mnemo == "PROTECTIONS":
            nomenc_info = {**nomenc_info, mnemo: get_protections()}
        elif mnemo == "SDAGE":
            nomenc_list = [
                {"id_nomenclature": nomenc.id_nomenclature, "mnemonique": nomenc.label_default}
                for nomenc in Nomenclatures.get_nomenclature_info(mnemo)
            ]
            nomenc_info = {**nomenc_info, mnemo: nomenc_list}
        elif mnemo == "OCCUPATION_SOLS":
            nomenc_list = [
                {
                    "id_nomenclature": nomenc.id_nomenclature,
                    "mnemonique": set_select_list(nomenc.cd_nomenclature, nomenc.mnemonique),
                }
                for nomenc in Nomenclatures.get_nomenclature_info(mnemo)
            ]
            nomenc_info = {**nomenc_info, mnemo: nomenc_list}
        else:
            nomenc_list = [
                {"id_nomenclature": nomenc.id_nomenclature, "mnemonique": nomenc.mnemonique}
                for nomenc in Nomenclatures.get_nomenclature_info(mnemo)
            ]
            nomenc_info = {**nomenc_info, mnemo: nomenc_list}
    return nomenc_info
