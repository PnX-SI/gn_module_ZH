from sqlalchemy.sql.expression import true

import pdb

from .models import *


def get_is_site_space(is_site_space):
    if is_site_space:
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


def get_mnemo(ids):
    if type(ids) is int:
        if ids:
            mnemo = DB.session.query(TNomenclatures).filter(
                TNomenclatures.id_nomenclature == ids).one().mnemonique
        else:
            mnemo = "Non renseigné"
    else:
        if ids:
            mnemo = [DB.session.query(TNomenclatures).filter(
                TNomenclatures.id_nomenclature == id).one().mnemonique
                for id in ids]
        else:
            mnemo = "Non renseigné"
    return mnemo
