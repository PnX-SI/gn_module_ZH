from flask import (
    Blueprint, 
    current_app, 
    session,
    request
)

from geojson import FeatureCollection

from geonature.utils.utilssqlalchemy import json_resp
from geonature.utils.env import DB
# from geonature.utils.env import get_id_module

# import des fonctions utiles depuis le sous-module d'authentification
from geonature.core.gn_permissions import decorators as permissions
from geonature.core.gn_permissions.tools import get_or_fetch_user_cruved

from .models import TZH

from pdb import set_trace as debug

blueprint = Blueprint("zones_humides", __name__)


# Route pour afficher liste des zones humides
@blueprint.route("", methods=["GET"])
#@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_zh():
    #debug()

    q = DB.session.query(TZH)

    parameters = request.args
    
    limit = int(parameters.get("limit", 100))
    page = int(parameters.get("offset", 0))

    # Pour obtenir le nombre de résultat de la requete sans le LIMIT
    nb_results_without_limit = q.count()

    '''
    user = info_role
    user_cruved = get_or_fetch_user_cruved(
        session=session, id_role=info_role.id_role, module_code="ZONES_HUMIDES"
    )
    '''

    data = q.limit(limit).offset(page * limit).all()
    #debug()
    featureCollection = []
    for n in data:
        #releve_cruved = n.get_releve_cruved(user, user_cruved)
        feature = n.get_geofeature(
            relationships=()
        )
        #feature["properties"]["rights"] = releve_cruved
        featureCollection.append(feature)
    return {
        "total": nb_results_without_limit,
        "total_filtered": len(data),
        "page": page,
        "limit": limit,
        "items": FeatureCollection(featureCollection),
    }


@blueprint.route("/<int:id_zh>", methods=["DELETE"])
@permissions.check_cruved_scope("D", True, module_code="ZONES_HUMIDES")
@json_resp
def deleteOneZh(id_zh, info_role):
    """Delete one zh

    :params int id_zh: ID of the zh to delete

    """
    debug()
    #releveRepository = ReleveRepository(TRelevesOccurrence)
    #releveRepository.delete(id_releve, info_role)
    zh = DB.session.query(TZH).get(id_zh)
    if zh:
        zh = zh.get_releve_if_allowed(info_user)
        DB.session.delete(zh)
        DB.session.commit()
        return {"message": "delete with success"}, 200
    raise NotFound('The zh "{}" does not exist'.format(id_zh))


# Exemple d'une route protégée le CRUVED du sous module d'authentification
@blueprint.route("/test_cruved", methods=["GET"])
@permissions.check_cruved_scope("R", module_code="ZONES_HUMIDES")
@json_resp
def get_sensitive_view(info_role):
    # Récupérer l'id de l'utilisateur qui demande la route
    id_role = info_role.id_role
    # Récupérer la portée autorisée à l'utilisateur pour l'acton 'R' (read)
    read_scope = info_role.value_filter

    # récupérer le CRUVED complet de l'utilisateur courant
    user_cruved = get_or_fetch_user_cruved(
        session=session, id_role=info_role.id_role, module_code="ZONES_HUMIDES",
    )
    q = DB.session.query(MySQLAModel)
    data = q.all()
    return [d.as_dict() for d in data]
