from sqlalchemy.sql.expression import true

import pdb

from .models import *


def get_bool(bool):
    if bool:
        return 'Oui'
    return 'Non'


def get_communes(communes):
    commune_insee = [k for k, v in [(k, v)
                                    for x in communes for (k, v) in x.items()]]
    commune_names = [v for k, v in [(k, v)
                                    for x in communes for (k, v) in x.items()]]
    return {
        "communes": commune_names,
        "code_insee": commune_insee
    }


def get_communes_info(id_zh):
    q = CorZhArea.get_municipalities_info(id_zh)
    communes = [{
        "Commune": commune.LiMunicipalities.nom_com,
        "Code INSEE": commune.LiMunicipalities.insee_com,
        "Couverture ZH par rapport à la surface de la commune": str(commune.CorZhArea.cover) if commune.CorZhArea.cover is not None else 'Non renseigné'
    } for commune in q]
    return communes


def get_author(id_zh, type='author'):
    if type == 'author':
        prenom = DB.session.query(TZH).filter(
            TZH.id_zh == id_zh).one().authors.prenom_role
        nom = DB.session.query(TZH).filter(
            TZH.id_zh == id_zh).one().authors.nom_role
    else:
        prenom = DB.session.query(TZH).filter(
            TZH.id_zh == id_zh).one().coauthors.prenom_role
        nom = DB.session.query(TZH).filter(
            TZH.id_zh == id_zh).one().coauthors.nom_role
    return prenom + ' ' + nom.upper()


def get_references(ref_list):
    if ref_list:
        return [
            {
                "Titre du document": ref['title'],
                "Auteurs": ref['authors'],
                "Année de parution": ref['pub_year'],
                "Bassins versants": 'en attente',
                "Editeur": ref['editor'],
                "Lieu": ref['editor_location']
            }
            for ref in ref_list
        ]
    return "Non renseigné"


def get_mnemo(ids):
    if ids:
        if type(ids) is int:
            return DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == ids).one().mnemonique
        return [DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == id).one().mnemonique for id in ids]
    return "Non renseigné"


def get_activities(activities):
    if activities:
        return [
            {
                "Activité humaine": get_mnemo(activity['id_human_activity']),
                "Localisation": get_mnemo(activity['id_localisation']),
                "Impacts": get_mnemo(activity['ids_impact']),
                "Remarques": activity['remark_activity']
            }
            for activity in activities
        ]
    return "Non renseigné"


def get_cb(cb_ids):
    if cb_ids:
        cbs = BibCb.get_label()
        cbs_info = {}
        for cb in cbs:
            if cb.BibCb.lb_code in cb_ids:
                cbs_info.update({
                    "Code Corine Biotope": cb.BibCb.lb_code,
                    "Libellé Corine Biotope": cb.Habref.lb_hab_fr,
                    "Humidité": cb.BibCb.humidity
                })
        return cbs_info
    return "Non renseigné"


def get_flows(flows, type):
    if type == "inflows":
        flow_type = "Entrée d'eau"
        id_key = "id_inflow"
        flows = flows[1]  # to do : correct json input
    else:
        flow_type = "Sortie d'eau"
        id_key = "id_outflow"
        flows = flows[0]  # to do : correct json input
    if flows[type]:
        return [
            {
                flow_type: get_mnemo(flow[id_key]),
                "Permanence": get_mnemo(flow["id_permanance"]),
                "Toponymie et compléments d'information": flow["topo"]
            }
            for flow in flows[type]
        ]
    return "Non renseigné"


def get_function_info(functions, type):
    if functions:
        return [
            {
                type: get_mnemo(function['id_function']),
                "Justification": function['justification'],
                "Qualification": get_mnemo(function['id_qualification']),
                "Connaissance": get_mnemo(function['id_knowledge'])
            }
            for function in functions
        ]
    return "Non renseigné"


def get_int(nb):
    return nb if nb is not None else 'Non évalué'


def get_hab_heritages(habs):
    if habs:
        return [
            {
                "Corine Biotope": DB.session.query(Habref).filter(Habref.cd_hab == hab['id_corine_bio']).one().lb_hab_fr,
                "Cahier Habitats": DB.session.query(Habref).filter(Habref.cd_hab == hab['id_cahier_hab']).one().lb_hab_fr,
                "Etat de préservation": get_mnemo(hab['id_preservation_state']),
                "Recouvrement de la ZH (%)": "Non évalué" if hab.hab_cover == "999" else hab.hab_cover
            }
            for hab in habs
        ]
    return "Non renseigné"
