from .models import (
    Nomenclatures,
    CorSdageSage,
    BibCb
)

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
        list_by_sdage.append({int(sage.CorSdageSage.id_sdage): nomenc_list})
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


def get_nomenc(config):
    nomenc_info = {}
    for mnemo in config:
        if mnemo == 'CORINE_BIO':
            nomenc_list = get_corine_biotope()
            nomenc_info.update({mnemo: nomenc_list})
        elif mnemo == 'SDAGE-SAGE':
            list_by_sdage = get_sage_list()
            nomenc_info.update({mnemo: list_by_sdage})
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
