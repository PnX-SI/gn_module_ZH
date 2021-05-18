from .models import Nomenclatures


def get_nomenc_by_tab(id_tab,config):
    mnemo_nomenc_list = config[str(id_tab)]
    nomenc_info = {}
    if mnemo_nomenc_list:
        for mnemo in mnemo_nomenc_list:
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