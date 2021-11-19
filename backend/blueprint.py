from flask import (
    Blueprint,
    current_app,
    session,
    request,
    json,
    jsonify,
    send_file
)

import csv

from pathlib import Path

import uuid

from pathlib import Path

import os
from flask.helpers import send_file, send_from_directory
from werkzeug import utils

from werkzeug.utils import secure_filename

from sqlalchemy.sql.expression import delete

from geojson import FeatureCollection

from sqlalchemy import func, text, desc, and_, inspect
from sqlalchemy.orm.exc import NoResultFound

import geoalchemy2
from datetime import datetime as dt, timezone

from pypn_habref_api.models import (
    Habref,
    CorespHab
)
from geonature.core.ref_geo.models import LAreas, BibAreasTypes

from geonature.utils.utilssqlalchemy import json_resp
from utils_flask_sqla.response import json_resp_accept_empty_list
from geonature.utils.env import DB, ROOT_DIR
from geonature.core.gn_commons.models import TMedias

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

from .upload import upload

from .hierarchy import *

from .utils import (
    get_file_path,
    delete_file,
    check_ref_geo_schema
)

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
    try:
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
        is_ref_geo = check_ref_geo_schema()

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
    except Exception as e:
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_zh_list_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


# Route pour afficher liste des zones humides
@blueprint.route("/check_ref_geo", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def check_ref_geo(info_role):
    try:
        # check if municipalities and dep in ref_geo
        return {
            "check_ref_geo": check_ref_geo_schema()
        }, 200
    except Exception as e:
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="check_ref_geo_route_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


@blueprint.route("/<int:id_zh>", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_zh_by_id(id_zh, info_role):
    """Get zh form data by id
    """
    try:
        return ZH(id_zh).__repr__()
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        if e.__class__.__name__ == 'NoResultFound':
            raise ZHApiError(message='is_zh_id_exists', details=str(
                exc_type) + ': ' + str(e.with_traceback(tb)))
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="get_zh_by_id_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        raise ZHApiError(
            message="get_zh_by_id_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


@blueprint.route("/<int:id_zh>/complete_card", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_complete_info(id_zh, info_role):
    """Get zh complete info
    """
    try:
        # get other referentials needed for the module from the config file
        ref_geo_config = [
            ref for ref in blueprint.config['ref_geo_referentiels'] if ref['active']]
        return Card(id_zh, "full", ref_geo_config).__repr__()
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        if e.__class__.__name__ == 'NoResultFound':
            raise ZHApiError(message='is_zh_id_exists', details=str(
                exc_type) + ': ' + str(e.with_traceback(tb)))
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="get_complete_info_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        raise ZHApiError(
            message="get_complete_info_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


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
        exc_type, value, tb = sys.exc_info()
        if e.__class__.__name__ == 'NoResultFound':
            raise ZHApiError(message='is_zh_id_exists', details=str(
                exc_type) + ': ' + str(e.with_traceback(tb)))
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        raise ZHApiError(
            message="get_zh_eval_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


@blueprint.route("/municipalities/<int:id_zh>", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_municipalities(id_zh, info_role):
    """Get municipalities list
    """
    try:
        if not CorZhArea.get_municipalities_info(id_zh):
            raise ZHApiError(message='no_municipality_error',
                             details='Empty list of municipality returned from get_municipalities_info db request')
        return [
            {
                "municipality_name": municipality.LiMunicipalities.nom_com,
                "id_area": municipality.CorZhArea.id_area
            } for municipality in CorZhArea.get_municipalities_info(id_zh)
        ]
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        if e.__class__.__name__ == 'NoResultFound':
            raise ZHApiError(message='is_zh_id_exists', details=str(
                exc_type) + ': ' + str(e.with_traceback(tb)))
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        raise ZHApiError(
            message="get_municipalities_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


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
        exc_type, value, tb = sys.exc_info()
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        raise ZHApiError(
            message="get_tab_data_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


@blueprint.route("/forms/cahierhab/<string:lb_code>", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_cahier_hab(info_role, lb_code):
    """Get cahier hab list from corine biotope lb_code
    """
    try:
        return get_ch(lb_code)
    except Exception as e:
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_cahier_hab_route_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


@blueprint.route("/geometries", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_geometries(info_role):
    """Get list of all zh geometries (contours)
    """
    try:
        if not DB.session.query(TZH).all():
            raise ZHApiError(message='no_geometry',
                             details='Empty list of zh returned from get_zh_list db request')
        return [
            {
                "geometry": zh.get_geofeature()["geometry"],
                "id_zh": zh.get_geofeature()["properties"]["id_zh"]
            } for zh in DB.session.query(TZH).all()
        ]
    except Exception as e:
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_geometries_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


@ blueprint.route("/references/autocomplete", methods=["GET"])
@ permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@ json_resp
def get_ref_autocomplete(info_role):
    try:
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
    except Exception as e:
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_ref_autocomplete_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


@ blueprint.route("/references", methods=["POST"])
@ permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
@ json_resp
def post_reference(info_role):
    """create reference
    """
    try:
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
    except Exception as e:
        DB.session.rollback()
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_reference_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_reference_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


@ blueprint.route("/references", methods=["PATCH"])
@ permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
@ json_resp
def patch_reference(info_role):
    """edit reference
    """
    try:
        form_data = request.json
        DB.session.query(TReferences).filter(TReferences.id_reference == form_data['id_reference']).update({
            TReferences.authors: form_data["authors"],
            TReferences.pub_year: form_data["pub_year"],
            TReferences.title: form_data["title"],
            TReferences.editor: form_data["editor"],
            TReferences.editor_location: form_data["editor_location"]
        })
        DB.session.commit()
        return form_data
    except Exception as e:
        DB.session.rollback()
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="edit_reference_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="edit_reference_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


@ blueprint.route("/<int:id_zh>/files", methods=["GET"])
@ permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
@ json_resp_accept_empty_list
def get_file_list(id_zh, info_role):
    """get a list of the zh files contained in static repo
    """
    try:
        zh_uuid = DB.session.query(TZH).filter(
            TZH.id_zh == id_zh).one().zh_uuid
        q_medias = DB.session.query(TMedias).filter(
            TMedias.unique_id_media == zh_uuid).all()
        return {
            "media_data": [media.as_dict() for media in q_medias],
            "main_pict_id": DB.session.query(TZH).filter(TZH.id_zh == id_zh).one().main_pict_id
        }
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_file_list_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


@ blueprint.route("files/<int:id_media>", methods=["DELETE"])
@ permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
def delete_one_file(id_media, info_role):
    """delete file by id_media in TMedias and static directory
    """
    try:
        delete_file(id_media)
        return ('', 204)
    except Exception as e:
        DB.session.rollback()
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        raise ZHApiError(
            message="delete_one_file_error", details=str(e))
    finally:
        DB.session.close()


@ blueprint.route("files/<int:id_media>", methods=["GET"])
@ permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
def download_file(id_media, info_role):
    """download file by id_media in static directory
    """
    try:
        return send_file(get_file_path(id_media), as_attachment=True)
    except Exception as e:
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        raise ZHApiError(
            message="download_file_error", details=str(e))
    finally:
        DB.session.close()


@ blueprint.route("<int:id_zh>/main_pict/<int:id_media>", methods=["PATCH"])
@ permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
def post_main_pict(id_zh, id_media, info_role):
    """post main picture id in tzh
    """
    try:
        DB.session.query(TZH).filter(TZH.id_zh == id_zh).update({
            TZH.main_pict_id: id_media})
        DB.session.commit()
        return ('', 204)
    except Exception as e:
        DB.session.rollback()
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_main_pict_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_main_pict_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


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
            zh_date = dt.now(timezone.utc)
            # set name
            if form_data['main_name'] == "":
                raise ZHApiError(
                    message='empty_field_error', details='empty main name field', status_code=400)

            # select active geo refs in config
            active_geo_refs = [
                ref for ref in blueprint.config['ref_geo_referentiels'] if ref['active']]
            intersection = None
            if 'id_zh' not in form_data.keys():
                # set geometry from coordinates
                geom = set_geom(form_data['geom']['geometry'])
                # create_zh
                zh = create_zh(form_data, info_role, zh_date,
                               geom['polygon'], active_geo_refs)
                intersection = geom['is_intersected']
            else:
                # edit geometry
                geom = set_geom(
                    form_data['geom']['geometry'], form_data['id_zh'])
                # edit zh
                zh = update_zh_tab0(form_data, geom['polygon'],
                                    info_role, zh_date, active_geo_refs)
                intersection = geom['is_intersected']

            DB.session.commit()

            return {
                "id_zh": zh,
                "is_intersected": intersection
            }, 200

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

        if id_tab == 8:
            # to do :
            #   add main_picture attribute in pr_zh.t_zh when implemented in frontend (radio ?)
            try:
                file_name = secure_filename(request.files["file"].filename)
                temp = file_name.split(".")
                extension = temp[len(temp) - 1]
            except Exception as e:
                file_name = "Filename_error"
                extension = "Extension_error"
                raise

            ALLOWED_EXTENSIONS = blueprint.config['allowed_extensions']
            MAX_PDF_SIZE = blueprint.config['max_pdf_size']
            MAX_JPG_SIZE = blueprint.config['max_jpg_size']
            FILE_PATH = blueprint.config['file_path']
            MODULE_NAME = blueprint.config['MODULE_CODE'].lower()
            uploaded_resp = upload(
                request,
                ALLOWED_EXTENSIONS,
                MAX_PDF_SIZE,
                MAX_JPG_SIZE,
                FILE_PATH,
                MODULE_NAME
            )

            # checks if error in user file or user http request:
            if "error" in uploaded_resp:
                return {"id_zh": request.form.to_dict['id_zh'], "errors": uploaded_resp["error"]}, 400

            # save in db
            id_media = post_file_info(
                request.form.to_dict()['id_zh'],
                request.form.to_dict()['title'],
                request.form.to_dict()['author'],
                request.form.to_dict()['summary'],
                uploaded_resp['media_path'],
                uploaded_resp['extension'])
            DB.session.commit()

            return {
                "media_path": uploaded_resp["media_path"],
                "secured_file_name": uploaded_resp['file_name'],
                "original_file_name": request.files["file"].filename,
                "id_media": id_media
            }, 200

    except Exception as e:
        DB.session.rollback()
        if e.__class__.__name__ == 'KeyError' or e.__class__.__name__ == 'TypeError':
            raise ZHApiError(
                message='likely_empty_mandatory_field_error', details=str(e), status_code=400)
        if e.__class__.__name__ == 'IntegrityError':
            raise ZHApiError(
                message='ZH_main_name_already_exists', details=str(e), status_code=400)
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_tab_form_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_tab_form_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
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

        # delete files in TMedias and repos
        zh_uuid = DB.session.query(TZH).filter(
            TZH.id_zh == id_zh).one().zh_uuid
        q_medias = DB.session.query(TMedias).filter(
            TMedias.unique_id_media == zh_uuid).all()
        for media in q_medias:
            delete_file(media.id_media)

        zhRepository.delete(id_zh, info_role)
        DB.session.commit()

        return {"message": "delete with success"}, 200
    except Exception as e:
        DB.session.rollback()
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=400)
        raise ZHApiError(
            message="error_during_zh_delete", details=str(e))
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


@blueprint.route("/<int:id_zh>/taxa")
@ permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
def write_csv(id_zh, info_role):
    try:
        names = []
        FILE_PATH = blueprint.config['file_path']
        MODULE_NAME = blueprint.config['MODULE_CODE'].lower()
        # author name
        prenom = DB.session.query(User).filter(
            User.id_role == info_role.id_role).one().prenom_role
        nom = DB.session.query(User).filter(
            User.id_role == info_role.id_role).one().nom_role
        author = prenom + ' ' + nom
        for i in ['vertebrates_view_name', 'invertebrates_view_name', 'flora_view_name']:
            model = get_view_model(
                blueprint.config[i]['table_name'],
                blueprint.config[i]['schema_name']
            )
            query = DB.session.query(model).filter(model.id_zh == id_zh).all()
            current_date = dt.now(timezone.utc)
            if query:
                rows = [
                    {
                        "Groupe d'étude": row.group,
                        "Nom Scientifique": row.scientific_name,
                        "Nom vernaculaire": row.vernac_name,
                        "Réglementation": row.reglementation,
                        "Article": row.article,
                        "Nombre d'observations": row.obs_nb,
                        "Date de la dernière observation": row.last_date,
                        "Dernier observateur": row.observer,
                        "Organisme": row.organisme
                    } for row in query
                ]
                name_file = blueprint.config[i]['category'] + "_" + \
                    current_date.strftime("%Y-%m-%d_%H:%M:%S") + ".csv"
                media_path = Path('external_modules',
                                  MODULE_NAME, FILE_PATH, name_file)
                full_name = ROOT_DIR / media_path
                names.append(str(full_name))
                with open(full_name, 'w', encoding='UTF8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)

                post_file_info(
                    id_zh,
                    blueprint.config[i]['category'] + "_" +
                    current_date.strftime("%Y-%m-%d_%H:%M:%S"),
                    author,
                    'liste des taxons générée sur demande de l''utilisateur dans l''onglet 5',
                    str(media_path),
                    '.csv')
                DB.session.commit()
        return {"file_names": names}, 200
    except Exception as e:
        DB.session.rollback()
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="csv_taxa_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        if e.__class__.__name__ == 'ZHApiError':
            raise ZHApiError(
                message=str(e.message), details=str(e.details))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="csv_taxa_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.close()


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


@blueprint.route("/<int:id_zh>/hierarchy", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_hierarchy(id_zh, info_role):
    """Get zh note
    """
    try:
        hierarchy = Hierarchy(id_zh).__str__()
        # pdb.set_trace()
        return hierarchy
    except ZHApiError as e:
        raise ZHApiError(
            message=str(e.message), details=str(e.details), status_code=e.status_code)
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_hierarchy_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
    finally:
        DB.session.rollback()
        DB.session.close()
