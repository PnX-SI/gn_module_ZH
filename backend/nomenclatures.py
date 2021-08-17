from .models import (
    Nomenclatures,
    CorSdageSage,
    BibCb,
    CorImpactTypes,
    CorMainFct,
    CorUrbanTypeRange
)

from pypnnomenclature.models import (
    TNomenclatures,
    BibNomenclaturesTypes
)

from geonature.utils.env import DB


import pdb


def get_sage_list():
    list_by_sdage = []
    id_sdage_list = CorSdageSage.get_id_sdage_list()
    for id in id_sdage_list:
        nomenc_list = []
        sages = CorSdageSage.get_sage_by_id(id)
        for sage in sages:
            nomenc_list.append(
                {
                    "id_nomenclature": sage.CorSdageSage.id_sage,
                    "mnemonique": sage.TNomenclatures.mnemonique
                }
            )
        list_by_sdage.append(
            {int(sage.CorSdageSage.id_sdage): nomenc_list}
        )
    return list_by_sdage


def get_corine_biotope():
    cbs = BibCb.get_label()
    nomenc_list = []
    for cb in cbs:
        nomenc_list.append(
            {
                "CB_code": cb.BibCb.lb_code,
                "CB_label": cb.Habref.lb_hab_fr,
                "CB_humidity": cb.BibCb.humidity
            }
        )
    return nomenc_list


def get_impact_list():
    impacts = CorImpactTypes.get_impacts()
    impacts_list = []
    for impact in impacts:
        # get mnemonique of id_impact_type
        if impact.CorImpactTypes.id_impact_type is not None:
            category = DB.session.query(TNomenclatures).filter(
                TNomenclatures.id_nomenclature == impact.CorImpactTypes.id_impact_type).one().mnemonique
        else:
            category = "Aucun"
        # list of impact ids and mnemoniques
        impacts_list.append({
            "id_cor_impact_types": impact.CorImpactTypes.id_cor_impact_types,
            "id_nomenclature": impact.CorImpactTypes.id_impact,
            "mnemonique": impact.TNomenclatures.mnemonique,
            "id_category": impact.CorImpactTypes.id_impact_type,
            "category": category
        })
    return impacts_list


def get_function_list(mnemo):

    # get id_type of mnemo (ex : 'FONCTIONS_HYDRO') in BibNomenclatureTypes
    id_type_main_function = DB.session.query(BibNomenclaturesTypes).filter(
        BibNomenclaturesTypes.mnemonique == mnemo).one().id_type

    # get list of TNomenclatures ids by id_type
    nomenclature_ids = [nomenc.id_nomenclature for nomenc in DB.session.query(TNomenclatures).filter(
        TNomenclatures.id_type == id_type_main_function).all()]

    # get mnemo main_functions
    main_functions_ids = CorMainFct.get_main_function_list(nomenclature_ids)

    # get list of functions by mnemo main function
    list_by_main_function = []
    for main_function_id in main_functions_ids:
        nomenc_list = []
        functions = CorMainFct.get_function_by_main_function(main_function_id)
        for function in functions:
            nomenc_list.append(
                {
                    "id_nomenclature": function.CorMainFct.id_function,
                    "mnemonique": function.TNomenclatures.mnemonique
                }
            )
        type_mnemo = CorMainFct.get_mnemo_type(main_function_id)
        if type_mnemo != '':
            list_by_main_function.append({type_mnemo.mnemonique: nomenc_list})
        else:
            list_by_main_function.append({type_mnemo: nomenc_list})
    return list_by_main_function


def get_urban_docs(mnemo):
    q_urban_docs = Nomenclatures.get_nomenclature_info("TYP_DOC_COMM")
    urban_docs = []
    for doc in q_urban_docs:
        urban_docs.append({
            "id_nomenclature": doc.id_nomenclature,
            "mnemonique": doc.mnemonique,
            "type_classement": CorUrbanTypeRange.get_range_by_doc(doc.id_nomenclature)
        })
    return urban_docs


def get_nomenc(config):
    nomenc_info = {}
    for mnemo in config:
        if mnemo in ['FONCTIONS_HYDRO', 'FONCTIONS_BIO', 'INTERET_PATRIM']:
            nomenc_list = get_function_list(mnemo)
            nomenc_info.update({mnemo: nomenc_list})
        elif mnemo == 'IMPACTS':
            nomenc_list = get_impact_list()
            nomenc_info.update({mnemo: nomenc_list})
        elif mnemo == 'CORINE_BIO':
            nomenc_list = get_corine_biotope()
            nomenc_info.update({mnemo: nomenc_list})
        elif mnemo == 'SDAGE-SAGE':
            list_by_sdage = get_sage_list()
            nomenc_info.update({mnemo: list_by_sdage})
        elif mnemo == 'TYP_DOC_COMM':
            nomenc_list = get_urban_docs(mnemo)
            nomenc_info.update({mnemo: nomenc_list})
        else:
            nomenc = Nomenclatures.get_nomenclature_info(mnemo)
            nomenc_list = []
            for i in nomenc:
                nomenc_list.append(
                    {
                        "id_nomenclature": i.id_nomenclature,
                        "mnemonique": i.mnemonique
                    }
                )
            nomenc_info.update({mnemo: nomenc_list})
    return nomenc_info
