from flask import (
    Blueprint,
    current_app,
    session,
    request,
    json,
    jsonify
)

import uuid

from geojson import FeatureCollection

from sqlalchemy import func, text, desc
from sqlalchemy.orm.exc import NoResultFound

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
    CorZhFctArea,
    CorZhRef,
    TReferences,
    BibSiteSpace,
    CorZhLimFs,
    BibOrganismes,
    ZH,
    Code
)

from .nomenclatures import get_nomenc

from .repositories import (
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
        "items": FeatureCollection(featureCollection)
    }, 200


@blueprint.route("/<int:id_zh>", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_zh_by_id(id_zh, info_role):
    """Get zh form data by id
    """
    try:
        full_zh = ZH(id_zh).get_full_zh()
        return full_zh

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

        bib_organismes = DB.session.query(BibOrganismes).all()
        bib_organismes_list = [
            bib_org.as_dict() for bib_org in bib_organismes if bib_org.is_op_org == True
        ]
        metadata["BIB_ORGANISMES"] = bib_organismes_list

        bib_site_spaces = DB.session.query(BibSiteSpace).all()
        bib_site_spaces_list = [
            bib_site_space.as_dict() for bib_site_space in bib_site_spaces
        ]
        metadata["BIB_SITE_SPACE"] = bib_site_spaces_list

        return metadata
    except Exception as e:
        raise ZHApiError(message=str(e), details=str(e))


@blueprint.route("/references/autocomplete", methods=["GET"])
@permissions.check_cruved_scope("R", True, module_code="ZONES_HUMIDES")
@json_resp
def get_ref_autocomplete(info_role):
    params = request.args
    search_title = params.get("search_title")
    #search_title = 'MCD'
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


@blueprint.route("/references", methods=["POST"])
@permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
@json_resp
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


@blueprint.route("/references", methods=["PATCH"])
@permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
@json_resp
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


@blueprint.route("/form/<int:id_tab>", methods=["POST", "PATCH"])
@permissions.check_cruved_scope("C", True, module_code="ZONES_HUMIDES")
@json_resp
def get_tab_data(id_tab, info_role):
    """Post zh data
    """
    form_data = request.json
    try:
        # get form data
        if id_tab == 0:

            # set geometry from coordinates
            polygon = DB.session.query(func.ST_GeomFromGeoJSON(
                str(form_data['geom']['geometry']))).one()[0]
            # set date
            zh_date = datetime.now(timezone.utc)
            # set name
            if form_data['main_name'] == "":
                return 'Empty mandatory field', 400

            if 'id_zh' not in form_data.keys():

                # fill pr_zh.cor_lim_list
                uuid_id_lim_list = uuid.uuid4()
                for lim in form_data['critere_delim']:
                    DB.session.add(CorLimList(
                        id_lim_list=uuid_id_lim_list, id_lim=lim))
                    DB.session.flush()

                # temporary code
                code = str(uuid.uuid4())[0:12]

                # create zh : fill pr_zh.t_zh
                new_zh = TZH(
                    main_name=form_data['main_name'],
                    code=code,
                    id_org=form_data['id_org'],
                    create_author=info_role.id_role,
                    update_author=info_role.id_role,
                    create_date=zh_date,
                    update_date=zh_date,
                    id_lim_list=uuid_id_lim_list,
                    id_sdage=form_data['sdage'],
                    geom=polygon
                )
                DB.session.add(new_zh)
                DB.session.flush()

                # fill cor_zh_area for municipalities
                query = """
                    SELECT (ref_geo.fct_get_area_intersection(
                    ST_SetSRID('{geom}'::geometry,4326), {type})).id_area
                    """.format(geom=str(polygon), type=25)
                comm_list = DB.session.execute(text(query)).fetchall()
                for comm in comm_list:
                    DB.session.add(
                        CorZhArea(id_area=comm[0], id_zh=new_zh.id_zh))
                    DB.session.flush()

                # fill cor_zh_area for departements
                query = """
                    SELECT (ref_geo.fct_get_area_intersection(
                    ST_SetSRID('{geom}'::geometry,4326), {type})).id_area
                    """.format(geom=str(polygon), type=26)
                dep_list = DB.session.execute(text(query)).fetchall()
                for dep in dep_list:
                    DB.session.add(
                        CorZhArea(id_area=dep[0], id_zh=new_zh.id_zh))
                    DB.session.flush()

                # fill cor_zh_rb
                rbs = TZH.get_zh_area_intersected(
                    'river_basin', func.ST_GeomFromGeoJSON(str(form_data['geom']['geometry'])))
                for rb in rbs:
                    DB.session.add(CorZhRb(id_zh=new_zh.id_zh, id_rb=rb.id_rb))
                    DB.session.flush()

                # fill cor_zh_hydro
                has = TZH.get_zh_area_intersected(
                    'hydro_area', func.ST_GeomFromGeoJSON(str(form_data['geom']['geometry'])))
                for ha in has:
                    DB.session.add(CorZhHydro(
                        id_zh=new_zh.id_zh, id_hydro=ha.id_hydro))
                    DB.session.flush()

                # fill cor_zh_fct_area
                fas = TZH.get_zh_area_intersected(
                    'fct_area', func.ST_GeomFromGeoJSON(str(form_data['geom']['geometry'])))
                for fa in fas:
                    DB.session.add(CorZhFctArea(
                        id_zh=new_zh.id_zh, id_fct_area=fa.id_fct_area))
                    DB.session.flush()

                # create zh code
                # pdb.set_trace()
                #code = Code(new_zh.id_zh, new_zh.id_org, new_zh.geom)
                # pdb.set_trace()
                #new_zh.code = code

                DB.session.commit()
                return {
                    "id_zh": new_zh.id_zh
                }, 200

            if 'id_zh' in form_data.keys():

                if polygon != DB.session.query(TZH.geom).filter(
                        TZH.id_zh == form_data['id_zh']).one()[0]:
                    is_geom_new = True
                else:
                    is_geom_new = False

                # update pr_zh.cor_lim_list
                id_lim_list = DB.session.query(TZH.id_lim_list).filter(
                    TZH.id_zh == form_data['id_zh']).one()[0]
                DB.session.query(CorLimList).filter(
                    CorLimList.id_lim_list == id_lim_list).delete()
                for lim in form_data['critere_delim']:
                    DB.session.add(CorLimList(
                        id_lim_list=id_lim_list, id_lim=lim))
                    DB.session.flush()

                # update zh : fill pr_zh.t_zh
                DB.session.query(TZH).filter(TZH.id_zh == form_data['id_zh']).update({
                    TZH.main_name: form_data['main_name'],
                    TZH.id_org: form_data['id_org'],
                    TZH.update_author: info_role.id_role,
                    TZH.update_date: zh_date,
                    TZH.id_sdage: form_data['sdage'],
                    TZH.geom: polygon
                })
                DB.session.flush()

                if is_geom_new:
                    # update cor_zh_area
                    DB.session.query(CorZhArea).filter(
                        CorZhArea.id_zh == form_data['id_zh']).delete()
                    query = """
                        SELECT (ref_geo.fct_get_area_intersection(
                        ST_SetSRID('{geom}'::geometry,4326), {type})).id_area
                        """.format(geom=str(polygon), type=25)
                    comm_list = DB.session.execute(text(query)).fetchall()
                    for comm in comm_list:
                        DB.session.add(
                            CorZhArea(id_area=comm[0], id_zh=form_data['id_zh']))
                        DB.session.flush()

                    # update cor_zh_rb
                    DB.session.query(CorZhRb).filter(
                        CorZhRb.id_zh == form_data['id_zh']).delete()
                    rbs = TZH.get_zh_area_intersected(
                        'river_basin', func.ST_GeomFromGeoJSON(str(form_data['geom']['geometry'])))
                    for rb in rbs:
                        DB.session.add(
                            CorZhRb(id_zh=form_data['id_zh'], id_rb=rb.id_rb))
                        DB.session.flush()

                    # update cor_zh_hydro
                    DB.session.query(CorZhHydro).filter(
                        CorZhHydro.id_zh == form_data['id_zh']).delete()
                    has = TZH.get_zh_area_intersected(
                        'hydro_area', func.ST_GeomFromGeoJSON(str(form_data['geom']['geometry'])))
                    for ha in has:
                        DB.session.add(CorZhHydro(
                            id_zh=form_data['id_zh'], id_hydro=ha.id_hydro))
                        DB.session.flush()

                    # update cor_zh_fct_area
                    DB.session.query(CorZhFctArea).filter(
                        CorZhFctArea.id_zh == form_data['id_zh']).delete()
                    fas = TZH.get_zh_area_intersected(
                        'fct_area', func.ST_GeomFromGeoJSON(str(form_data['geom']['geometry'])))
                    for fa in fas:
                        DB.session.add(CorZhFctArea(
                            id_zh=form_data['id_zh'], id_fct_area=fa.id_fct_area))
                        DB.session.flush()

                DB.session.commit()
                return {
                    "id_zh": form_data['id_zh']
                }, 200

        if id_tab == 1:
            id_zh = form_data['id_zh']
            DB.session.query(TZH).filter(TZH.id_zh == id_zh).update({
                TZH.main_name: form_data['main_name'],
                TZH.secondary_name: form_data['secondary_name'],
                TZH.is_id_site_space: form_data['is_id_site_space'],
                TZH.id_site_space: form_data['id_site_space']
            })
            DB.session.query(CorZhRef).filter(CorZhRef.id_zh == id_zh).delete()
            for ref in form_data['id_references']:
                DB.session.add(CorZhRef(id_zh=id_zh, id_ref=ref))
                DB.session.flush()
            DB.session.commit()
            return {
                "id_zh": form_data['id_zh']
            }, 200

        if id_tab == 2:

            id_zh = form_data['id_zh']

            # edit criteres delim
            uuid_lim_list = DB.session.query(TZH.id_lim_list).filter(
                TZH.id_zh == id_zh).one().id_lim_list
            #query = DB.session.query(CorLimList).filter(CorLimList.id_lim_list == uuid_lim_list).all()
            #zh_crit_delim_list = sorted([q.id_lim for q in query])
            #new_crit_delim_list = sorted(form_data['critere_delim'])
            # if new_crit_delim_list != zh_crit_delim_list:
            DB.session.query(CorLimList).filter(
                CorLimList.id_lim_list == uuid_lim_list).delete()
            for lim in form_data['critere_delim']:
                DB.session.add(CorLimList(
                    id_lim_list=uuid_lim_list, id_lim=lim))
                DB.session.flush()

            # remarque criteres delim
            DB.session.query(TZH).filter(TZH.id_zh == id_zh).update(
                {TZH.remark_lim: form_data['remark_lim']})

            # edit criteres delim fonctionnelles
            DB.session.query(CorZhLimFs).filter(
                CorZhLimFs.id_zh == id_zh).delete()
            for lim in form_data['critere_delim_fs']:
                DB.session.add(CorZhLimFs(id_zh=id_zh, id_lim_fs=lim))
                DB.session.flush()

            # remarque criteres delim fonctionnelles
            DB.session.query(TZH).filter(TZH.id_zh == id_zh).update(
                {TZH.remark_lim_fs: form_data['remark_lim_fs']})

            DB.session.commit()

            return {
                "id_zh": id_zh
            }, 200

    except Exception as e:
        if e.__class__.__name__ == 'KeyError' or e.__class__.__name__ == 'TypeError':
            return 'Empty mandatory field', 400
        if e.__class__.__name__ == 'IntegrityError':
            return 'ZH main_name already exists', 400
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
    DB.session.query(CorZhRef).filter(CorZhRef.id_zh == id_zh).delete()
    zhRepository.delete(id_zh, info_role)

    return {"message": "delete with success"}, 200


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
