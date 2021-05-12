from flask import (
    Blueprint, 
    current_app, 
    session,
    request,
    json
)

import uuid

#import psycopg2

from geojson import FeatureCollection

from sqlalchemy import func, text
import geoalchemy2
from datetime import datetime, timezone

from pypnnomenclature.models import (
    TNomenclatures,
    BibNomenclaturesTypes
)

from geonature.utils.utilssqlalchemy import json_resp
from geonature.utils.env import DB
#from geonature.utils.env import get_id_module

# import des fonctions utiles depuis le sous-module d'authentification
from geonature.core.gn_permissions import decorators as permissions
from geonature.core.gn_permissions.tools import get_or_fetch_user_cruved

from .models import (
    TZH, 
    Nomenclatures,
    CorLimList,
    CorZhArea,
    CorZhRb,
    CorZhHydro,
    CorZhFctArea
)

from .repositories import (
    ZhRepository
)

from .api_error import ZHApiError

from pdb import set_trace as debug

blueprint = Blueprint("pr_zh", __name__)


# Route pour afficher liste des zones humides
@blueprint.route("", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_zh(info_role):
    q = DB.session.query(TZH)

    parameters = request.args
    
    limit = int(parameters.get("limit", 100))
    page = int(parameters.get("offset", 0))

    # Pour obtenir le nombre de résultat de la requete sans le LIMIT
    nb_results_without_limit = q.count()

    user = info_role
    user_cruved = get_or_fetch_user_cruved(
        session=session, id_role=info_role.id_role, module_code="ZONES_HUMIDES"
    )

    data = q.limit(limit).offset(page * limit).all()
    
    featureCollection = []
    for n in data:
        releve_cruved = n.get_releve_cruved(user, user_cruved)
        feature = n.get_geofeature(
            relationships=()
        )
        feature["properties"]["rights"] = releve_cruved
        featureCollection.append(feature)
    return {
        "total": nb_results_without_limit,
        "total_filtered": len(data),
        "page": page,
        "limit": limit,
        "items": FeatureCollection(featureCollection),
    }


@blueprint.route("/form/<int:id_tab>", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_tab(id_tab, info_role):
    """Get form info for tabs
    """
    try:
        mnemo_nomenc_list = blueprint.config["nomenc_mnemo_by_tab"][str(id_tab)]
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
        else:
            nomenc_info.update({"message from server":"no nomenclature in this tab"})

        return nomenc_info,200
        
    except Exception as e:
        raise ZHApiError(message=str(e), details=str(e))


@blueprint.route("/form/<int:id_tab>/data", methods=["GET","POST"])
@permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
@json_resp
def get_tab_data(id_tab, info_role):
    """Get form info for tabs
    """

    print(json.loads(request.data))

    try:
        # get form data
        if id_tab == 0:
            form_data = json.loads(request.data)
            # set geometry from coordinates
            polygon = DB.session.query(func.ST_GeomFromGeoJSON(str(form_data['geom']['geometry']))).one()[0]
            # set date
            zh_date = datetime.now(timezone.utc)

            # fill pr_zh.cor_lim_list
            uuid_id_lim_list = uuid.uuid4()
            for lim in form_data['critere_delim']:
                DB.session.add(CorLimList(id_lim_list=uuid_id_lim_list, id_lim=lim))
                DB.session.flush()

            # temporary code
            code = str(uuid.uuid4())[0:12]
            
            # create zh : fill pr_zh.t_zh
            new_zh = TZH(
                main_name = form_data['name'],
                code = code,
                create_author = info_role.id_role,
                update_author = info_role.id_role,
                create_date = zh_date,
                update_date = zh_date,
                id_lim_list = uuid_id_lim_list,
                id_sdage = form_data['sdage'],
                geom = polygon
            )
            DB.session.add(new_zh)
            DB.session.flush()
                            
            # fill cor_zh_area
            #test = DB.session.query(TZH.geom).filter(TZH.id_zh == new_zh.id_zh).one()
            #select (ref_geo.fct_get_area_intersection(ST_SetSRID('010300000001000000040000008978EBFCDB05054098FA795391844640904FC8CEDB180540139B8F6B438346402EAA454431F90440CAFB389A238346408978EBFCDB05054098FA795391844640'::geometry,4326),25)).id_area;
            query = """
                SELECT (ref_geo.fct_get_area_intersection(
                ST_SetSRID('{geom}'::geometry,4326), {type})).id_area
                """.format(geom=str(polygon),type=25)
            comm_list = DB.session.execute(text(query)).fetchall()
            for comm in comm_list:
                DB.session.add(CorZhArea(id_area=comm[0], id_zh=new_zh.id_zh))
                DB.session.flush()

            # fill cor_zh_rb
            rbs = TZH.get_zh_area_intersected('river_basin',func.ST_GeomFromGeoJSON(str(form_data['geom']['geometry'])))
            for rb in rbs:
                DB.session.add(CorZhRb(id_zh=new_zh.id_zh,id_rb=rb.id_rb))
                DB.session.flush()

            # fill cor_zh_hydro
            has = TZH.get_zh_area_intersected('hydro_area',func.ST_GeomFromGeoJSON(str(form_data['geom']['geometry'])))
            for ha in has:
                DB.session.add(CorZhHydro(id_zh=new_zh.id_zh,id_hydro=ha.id_hydro))
                DB.session.flush()

            # fill cor_zh_fct_area
            fas = TZH.get_zh_area_intersected('fct_area',func.ST_GeomFromGeoJSON(str(form_data['geom']['geometry'])))
            for fa in fas:
                DB.session.add(CorZhFctArea(id_zh=new_zh.id_zh,id_fct_area=fa.id_fct_area))
                DB.session.flush()

            DB.session.commit()
        return "data tab {id_tab} commited".format(id_tab=id_tab)
    except Exception as e:
        DB.session.rollback()
        raise ZHApiError(message=str(e), details=str(e))
    finally:
        DB.session.close()



@blueprint.route("/<int:id_zh>", methods=["DELETE"])
@permissions.check_cruved_scope("D", True, module_code="ZONES_HUMIDES")
@json_resp
def deleteOneZh(id_zh, info_role):
    """Delete one zh

    :params int id_zh: ID of the zh to delete

    """
    zhRepository = ZhRepository(TZH)
    zhRepository.delete(id_zh, info_role)

    return {"message": "delete with success"},200


"""
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
"""


@blueprint.errorhandler(ZHApiError)
def handle_geonature_zh_api(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response