from .models import (
    Nomenclatures,
    CorSdageSage,
    BibCb,
    CorImpactTypes,
    CorMainFct,
    CorUrbanTypeRange,
    CorProtectionLevelType
)

from pypnnomenclature.models import (
    TNomenclatures,
    BibNomenclaturesTypes
)

from geonature.utils.env import DB


import pdb


def get_sage_list():
    return [
        {
            int(sdage_id): [
                {
                    "id_nomenclature": sage.CorSdageSage.id_sage,
                    "mnemonique": sage.TNomenclatures.mnemonique
                } for sage in CorSdageSage.get_sage_by_id(sdage_id)
            ]
        } for sdage_id in CorSdageSage.get_id_sdage_list()
    ]


def get_corine_biotope():
    return [
        {
            "CB_code": cb.BibCb.lb_code,
            "CB_label": cb.Habref.lb_hab_fr,
            "CB_humidity": cb.BibCb.humidity,
            "CB_is_ch": cb.BibCb.is_ch
        } for cb in BibCb.get_label()
    ]


def get_impact_list():
    return [
        {
            "id_cor_impact_types": impact.CorImpactTypes.id_cor_impact_types,
            "id_nomenclature": impact.CorImpactTypes.id_impact,
            "mnemonique": impact.TNomenclatures.mnemonique,
            "id_category": impact.CorImpactTypes.id_impact_type,
            "category": get_impact_category(impact)
        } for impact in CorImpactTypes.get_impacts()
    ]


def get_impact_category(impact):
    # get mnemonique of id_impact_type
    if impact.CorImpactTypes.id_impact_type is not None:
        return DB.session.query(TNomenclatures).filter(
            TNomenclatures.id_nomenclature == impact.CorImpactTypes.id_impact_type).one().mnemonique
    return "Aucun"


def get_function_list(mnemo):
    # get id_type of mnemo (ex : 'FONCTIONS_HYDRO') in BibNomenclatureTypes
    id_type_main_function = DB.session.query(BibNomenclaturesTypes).filter(
        BibNomenclaturesTypes.mnemonique == mnemo).one().id_type

    # get list of TNomenclatures ids by id_type
    nomenclature_ids = [nomenc.id_nomenclature for nomenc in DB.session.query(TNomenclatures).filter(
        TNomenclatures.id_type == id_type_main_function).all()]

    return [
        {
            "id_nomenclature": function.CorMainFct.id_function,
            "mnemonique": function.TNomenclatures.mnemonique,
            "id_category": function.CorMainFct.id_main_function,
            "category": DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == function.CorMainFct.id_main_function).one().mnemonique
        } for function in CorMainFct.get_functions(nomenclature_ids)
    ]


def get_urban_docs():
    return [
        {
            "id_nomenclature": doc.id_nomenclature,
            "mnemonique": doc.mnemonique,
            "type_classement": CorUrbanTypeRange.get_range_by_doc(doc.id_nomenclature)
        } for doc in Nomenclatures.get_nomenclature_info("TYP_DOC_COMM")
    ]


def get_protections():
    return [
        {
            "id_protection_type": q_protection_type.id_nomenclature,
            "mnemonique_type": q_protection_type.mnemonique,
            "protection_status": CorProtectionLevelType.get_status_by_type(q_protection_type.id_nomenclature)
        } for q_protection_type in Nomenclatures.get_nomenclature_info("PROTECTION_TYP")
    ]


def get_nomenc(config):
    nomenc_info = {}
    for mnemo in config:
        if mnemo in ['FONCTIONS_HYDRO', 'FONCTIONS_BIO', 'INTERET_PATRIM']:
            nomenc_info = {**nomenc_info, mnemo: get_function_list(mnemo)}
        elif mnemo == 'IMPACTS':
            nomenc_info = {**nomenc_info, mnemo: get_impact_list()}
        elif mnemo == 'CORINE_BIO':
            nomenc_info = {**nomenc_info, mnemo: get_corine_biotope()}
        elif mnemo == 'SDAGE-SAGE':
            nomenc_info = {**nomenc_info, mnemo: get_sage_list()}
        elif mnemo == 'TYP_DOC_COMM':
            nomenc_info = {**nomenc_info, mnemo: get_urban_docs()}
        elif mnemo == 'PROTECTIONS':
            nomenc_info = {**nomenc_info, mnemo: get_protections()}
        else:
            nomenc_list = [
                {
                    "id_nomenclature": nomenc.id_nomenclature,
                    "mnemonique": nomenc.mnemonique
                } for nomenc in Nomenclatures.get_nomenclature_info(mnemo)
            ]
            nomenc_info = {**nomenc_info, mnemo: nomenc_list}
    return nomenc_info
