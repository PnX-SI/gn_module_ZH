from .models import Nomenclatures

def get_nomenc(config):
    #pdb.set_trace()
    nomenc_info = {}
    for mnemo in config:
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