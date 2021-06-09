from .models import Nomenclatures, CorSdageSage

import pdb


def get_nomenc(config):
    nomenc_info = {}
    for mnemo in config:
        if mnemo == 'SDAGE-SAGE':
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
                    {
                        int(sage.CorSdageSage.id_sdage): nomenc_list
                    }
                )
            nomenc_dict = {mnemo: list_by_sdage}
            nomenc_info.update(nomenc_dict)

        else:
            nomenc = Nomenclatures.get_nomenclature_info(mnemo)
            nomenc_list = []
            for i in nomenc:
                nomenc_list.append(
                    {
                        "id_nomenclature": i.id_nomenclature,
                        "mnemonique": i.mnemonique
                    })
            nomenc_dict = {
                mnemo: nomenc_list
            }
            nomenc_info.update(nomenc_dict)
    return nomenc_info
