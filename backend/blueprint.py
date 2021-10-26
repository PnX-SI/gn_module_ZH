from flask import (
    Blueprint,
    current_app,
    session,
    request,
    json,
    jsonify
)

import uuid

from sqlalchemy.sql.expression import delete

from geojson import FeatureCollection

from sqlalchemy import func, text, desc, and_
from sqlalchemy.orm.exc import NoResultFound

import geoalchemy2
from datetime import datetime, timezone

from pypn_habref_api.models import (
    Habref,
    CorespHab
)
from geonature.core.ref_geo.models import LAreas, BibAreasTypes

from geonature.utils.utilssqlalchemy import json_resp
from geonature.utils.env import DB
# from geonature.utils.env import get_id_module

# import des fonctions utiles depuis le sous-module d'authentification
from geonature.core.gn_permissions import decorators as permissions
from geonature.core.gn_permissions.tools import get_or_fetch_user_cruved

from .model.zh_schema import (
    TZH,
    CorLimList,
    CorZhArea,
    CorZhRef,
    TReferences,
    BibSiteSpace,
    BibOrganismes,
    BibActions
)

from .model.zh import ZH

from .model.cards import Card

from .nomenclatures import (
    get_nomenc,
    get_ch
)

from .forms import *

from .geometry import set_geom

from .model.repositories import (
    ZhRepository
)

from .api_error import ZHApiError

import pdb

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

    # check if municipalities and dep in ref_geo
    id_type_com = DB.session.query(BibAreasTypes).filter(
        BibAreasTypes.type_code == 'COM').one().id_type
    id_type_dep = DB.session.query(BibAreasTypes).filter(
        BibAreasTypes.type_code == 'DEP').one().id_type
    n_com = DB.session.query(LAreas).filter(
        LAreas.id_type == id_type_com).count()
    n_dep = DB.session.query(LAreas).filter(
        LAreas.id_type == id_type_dep).count()
    if n_com == 0 or n_dep == 0:
        is_ref_geo = False
    else:
        is_ref_geo = True

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
        "check_ref_geo": is_ref_geo
    }, 200


# Route pour afficher liste des zones humides
@blueprint.route("/check_ref_geo", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def check_ref_geo(info_role):
    try:
        # check if municipalities and dep in ref_geo
        id_type_com = DB.session.query(BibAreasTypes).filter(
            BibAreasTypes.type_code == 'COM').one().id_type
        id_type_dep = DB.session.query(BibAreasTypes).filter(
            BibAreasTypes.type_code == 'DEP').one().id_type
        n_com = DB.session.query(LAreas).filter(
            LAreas.id_type == id_type_com).count()
        n_dep = DB.session.query(LAreas).filter(
            LAreas.id_type == id_type_dep).count()
        if n_com == 0 or n_dep == 0:
            is_ref_geo = False
        else:
            is_ref_geo = True
        return {
            "check_ref_geo": is_ref_geo
        }, 200
    except Exception as e:
        raise ZHApiError(message=str(e), details=str(e))


@blueprint.route("/<int:id_zh>", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_zh_by_id(id_zh, info_role):
    """Get zh form data by id
    """
    try:
        return ZH(id_zh).__repr__()
    except Exception as e:
        if e.__class__.__name__ == 'NoResultFound':
            raise ZHApiError(message='zh id exist?', details=str(e))
        raise ZHApiError(message=str(e), details=str(e))


@blueprint.route("/<int:id_zh>/complete_card", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_complete_info(id_zh, info_role):
    """Get zh complete info
    """
    try:
        ref_geo_config = blueprint.config['ref_geo_referentiels']
        return Card(id_zh, "full", ref_geo_config).__repr__()
    except Exception as e:
        print(e)
        if e.__class__.__name__ == 'NoResultFound':
            raise ZHApiError(message='zh id exist?', details=str(e))
        raise ZHApiError(message=str(e), details=str(e))


@blueprint.route("/eval/<int:id_zh>", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_zh_eval(id_zh, info_role):
    """Get zh form data by id
    """
    try:
        zh_eval = ZH(id_zh).get_eval()
        return zh_eval
    except Exception as e:
        if e.__class__.__name__ == 'NoResultFound':
            raise ZHApiError(message='zh id exist?', details=str(e))
        raise ZHApiError(message=str(e), details=str(e))


@blueprint.route("/municipalities/<int:id_zh>", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_municipalities(id_zh, info_role):
    """Get municipalities list
    """
    try:
        return [{
            "municipality_name": municipality.LiMunicipalities.nom_com,
            "id_area": municipality.CorZhArea.id_area
        } for municipality in CorZhArea.get_municipalities_info(id_zh)]
    except Exception as e:
        if e.__class__.__name__ == 'NoResultFound':
            raise ZHApiError(message='zh id exist?', details=str(e))
        raise ZHApiError(message=str(e), details=str(e))


@blueprint.route("/forms", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_tab(info_role):
    """Get form metadata for all tabs
    """
    try:
        metadata = get_nomenc(blueprint.config["nomenclatures"])
        metadata["BIB_ORGANISMES"] = BibOrganismes.get_bib_organisms(
            "operator")
        metadata["BIB_SITE_SPACE"] = BibSiteSpace.get_bib_site_spaces()
        metadata["BIB_MANAGEMENT_STRUCTURES"] = BibOrganismes.get_bib_organisms(
            "management_structure")
        metadata["BIB_ACTIONS"] = BibActions.get_bib_actions()
        return metadata
    except Exception as e:
        raise ZHApiError(message=str(e), details=str(e))


@blueprint.route("/forms/cahierhab/<string:lb_code>", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_cahier_hab(info_role, lb_code):
    """Get cahier hab list from corine biotope lb_code
    """
    try:
        return get_ch(lb_code)
    except Exception as e:
        raise ZHApiError(message=str(e), details=str(e))


@blueprint.route("/geometries", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_geometries(info_role):
    """Get list of all zh geometries (contours)
    """
    try:
        return [
            {
                "geometry": zh.get_geofeature()["geometry"],
                "id_zh": zh.get_geofeature()["properties"]["id_zh"]
            } for zh in DB.session.query(TZH).all()
        ]
    except Exception as e:
        raise ZHApiError(message=str(e), details=str(e))


@ blueprint.route("/references/autocomplete", methods=["GET"])
@ permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@ json_resp
def get_ref_autocomplete(info_role):
    params = request.args
    search_title = params.get("search_title")
    # search_title = 'MCD'
    q = DB.session.query(
        TReferences,
        func.similarity(TReferences.title, search_title).label("idx_trgm"),
    )

    # if "id_list" in params:
    #    q = q.join(
    #        CorListHabitat, CorListHabitat.cd_hab == AutoCompleteHabitat.cd_hab
    #    ).filter(CorListHabitat.id_list == params.get("id_list"))

    search_title = search_title.replace(" ", "%")
    q = q.filter(
        TReferences.title.ilike("%" + search_title + "%")
    ).order_by(desc("idx_trgm"))

    # filter by typology
    # if "cd_typo" in params:
    #    q = q.filter(AutoCompleteHabitat.cd_typo == params.get("cd_typo"))

    limit = request.args.get("limit", 20)
    print(q)

    data = q.limit(limit).all()
    if data:
        return [d[0].as_dict() for d in data]
    else:
        return "No Result", 404


@ blueprint.route("/references", methods=["POST"])
@ permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
@ json_resp
def post_reference(info_role):
    """create reference
    """
    form_data = request.json
    new_ref = TReferences(
        authors=form_data["authors"],
        pub_year=form_data["pub_year"],
        title=form_data["title"],
        editor=form_data["editor"],
        editor_location=form_data["editor_location"]
    )
    DB.session.add(new_ref)
    DB.session.commit()
    return new_ref.as_dict()


@ blueprint.route("/references", methods=["PATCH"])
@ permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
@ json_resp
def patch_reference(info_role):
    """edit reference
    """
    form_data = request.json
    DB.session.query(TReferences).filter(TReferences.id_reference == form_data['id_reference']).update({
        TReferences.authors: form_data["authors"],
        TReferences.pub_year: form_data["pub_year"],
        TReferences.title: form_data["title"],
        TReferences.editor: form_data["editor"],
        TReferences.editor_location: form_data["editor_location"],
    })
    DB.session.commit()
    return form_data


@ blueprint.route("/form/<int:id_tab>", methods=["POST", "PATCH"])
@ permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
@ json_resp
def get_tab_data(id_tab, info_role):
    """Post zh data
    """
    form_data = request.json
    try:
        if id_tab == 0:
            # set date
            zh_date = datetime.now(timezone.utc)
            # set name
            if form_data['main_name'] == "":
                return 'Empty mandatory field', 400

            if 'id_zh' not in form_data.keys():
                # set geometry from coordinates
                polygon = set_geom(form_data['geom']['geometry'])
                # create_zh
                zh = create_zh(form_data, info_role, zh_date, polygon)
            else:
                # edit geometry
                polygon = set_geom(
                    form_data['geom']['geometry'], form_data['id_zh'])
                # edit zh
                zh = update_zh_tab0(form_data, polygon, info_role, zh_date)

            DB.session.commit()

            return {"id_zh": zh}, 200

        if id_tab == 1:
            update_tzh(form_data)
            update_refs(form_data)
            DB.session.commit()
            return {"id_zh": form_data['id_zh']}, 200

        if id_tab == 2:
            update_tzh(form_data)
            update_delim(form_data['id_zh'], form_data['critere_delim'])
            update_fct_delim(form_data['id_zh'], form_data['critere_delim_fs'])
            DB.session.commit()
            return {"id_zh": form_data['id_zh']}, 200

        if id_tab == 3:
            update_tzh(form_data)
            update_corine_biotopes(
                form_data['id_zh'], form_data['corine_biotopes'])
            update_corine_landcover(
                form_data['id_zh'], form_data['id_corine_landcovers'])
            update_activities(
                form_data['id_zh'], form_data['activities'])  # , form_data['id_cor_impact_types'])
            DB.session.commit()
            return {"id_zh": form_data['id_zh']}, 200

        if id_tab == 4:
            update_outflow(form_data['id_zh'], form_data['outflows'])
            update_inflow(form_data['id_zh'], form_data['inflows'])
            update_tzh(form_data)
            DB.session.commit()
            return {"id_zh": form_data['id_zh']}, 200

        if id_tab == 5:
            update_functions(
                form_data['id_zh'], form_data['fonctions_hydro'], 'FONCTIONS_HYDRO')
            update_functions(
                form_data['id_zh'], form_data['fonctions_bio'], 'FONCTIONS_BIO')

            update_functions(
                form_data['id_zh'], form_data['interet_patrim'], 'INTERET_PATRIM')

            update_functions(form_data['id_zh'],
                             form_data['val_soc_eco'], 'VAL_SOC_ECO')
            if form_data['total_hab_cover'] is None:
                form_data['total_hab_cover'] = DB.session.query(TZH).filter(
                    TZH.id_zh == form_data['id_zh']).one().total_hab_cover
            update_tzh(form_data)
            update_hab_heritages(
                form_data['id_zh'], form_data['hab_heritages'])
            DB.session.commit()
            return {"id_zh": form_data['id_zh']}, 200

        if id_tab == 6:
            update_ownerships(form_data['id_zh'], form_data['ownerships'])
            update_managements(form_data['id_zh'], form_data['managements'])
            update_instruments(form_data['id_zh'], form_data['instruments'])
            update_protections(form_data['id_zh'], form_data['protections'])
            update_zh_tab6(form_data)
            update_urban_docs(form_data['id_zh'], form_data['urban_docs'])
            DB.session.commit()
            return {"id_zh": form_data['id_zh']}, 200

        if id_tab == 7:
            update_tzh(form_data)
            update_actions(
                form_data['id_zh'], form_data['actions'])
            DB.session.commit()
            return {"id_zh": form_data['id_zh']}, 200

    except Exception as e:
        DB.session.rollback()
        if e.__class__.__name__ == 'KeyError' or e.__class__.__name__ == 'TypeError':
            return 'Empty mandatory field ?', 400
        if e.__class__.__name__ == 'IntegrityError':
            return 'ZH_main_name_already_exists', 400
        raise ZHApiError(message=str(e), details=str(e))
    finally:
        DB.session.close()


@ blueprint.route("/<int:id_zh>", methods=["DELETE"])
@ permissions.check_cruved_scope("D", True, module_code="ZONES_HUMIDES")
@ json_resp
def deleteOneZh(id_zh, info_role):
    """Delete one zh

    :params int id_zh: ID of th*e zh to delete

    """
    try:
        zhRepository = ZhRepository(TZH)
        # delete references
        DB.session.query(CorZhRef).filter(CorZhRef.id_zh == id_zh).delete()
        # delete criteres delim
        id_lim_list = DB.session.query(TZH).filter(
            TZH.id_zh == id_zh).one().id_lim_list
        DB.session.query(CorLimList).filter(
            CorLimList.id_lim_list == id_lim_list).delete()
        # delete cor_zh_area
        DB.session.query(CorZhArea).filter(CorZhArea.id_zh == id_zh).delete()

        zhRepository.delete(id_zh, info_role)
        DB.session.commit()

        return {"message": "delete with success"}, 200
    except Exception as e:
        if e.__class__.__name__ == 'KeyError' or e.__class__.__name__ == 'TypeError':
            return 'Empty mandatory field', 400
        if e.__class__.__name__ == 'IntegrityError':
            return 'ZH main_name already exists', 400
        DB.session.rollback()
        raise ZHApiError(message=str(e), details=str(e))
    finally:
        DB.session.close()


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


@ blueprint.errorhandler(ZHApiError)
def handle_geonature_zh_api(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@blueprint.route('/user/cruved', methods=['GET'])
@permissions.check_cruved_scope('R', True)
@json_resp
def returnUserCruved(info_role):
    # récupérer le CRUVED complet de l'utilisateur courant
    print(info_role)
    user_cruved = get_or_fetch_user_cruved(
        session=session,
        id_role=info_role.id_role,
        module_code=blueprint.config['MODULE_CODE']
    )
    return user_cruved
