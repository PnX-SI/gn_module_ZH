import uuid

from sqlalchemy import (
    func,
    text
    # desc,
    # and_
)

from geonature.utils.env import DB

from .models import (
    TZH,
    # Nomenclatures,
    CorLimList,
    CorZhArea,
    CorZhRb,
    CorZhHydro,
    CorZhFctArea,
    # CorZhRef,
    # TReferences,
    # BibSiteSpace,
    # CorZhLimFs,
    # BibOrganismes,
    # ZH,
    Code
)

from .api_error import ZHApiError

import pdb


def create_zh(form_data, info_role, zh_date, polygon):

    uuid_id_lim_list = uuid.uuid4()
    post_cor_lim_list(uuid_id_lim_list, form_data['critere_delim'])

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
    post_cor_zh_area(polygon, new_zh.id_zh, 25)
    # fill cor_zh_area for departements
    post_cor_zh_area(polygon, new_zh.id_zh, 26)
    # fill cor_zh_rb
    post_cor_zh_rb(form_data['geom']['geometry'], new_zh.id_zh)
    # fill cor_zh_hydro
    post_cor_zh_hydro(form_data['geom']['geometry'], new_zh.id_zh)
    # fill cor_zh_fct_area
    post_cor_zh_fct_area(form_data['geom']['geometry'], new_zh.id_zh)

    # create zh code
    code = Code(new_zh.id_zh, new_zh.id_org, new_zh.geom)
    if code.is_valid_number:
        new_zh.code = str(code)
    else:
        return {
            "code error": "zh_number_greater_than_9999"
        }, 500

    DB.session.commit()
    return new_zh.id_zh


def post_cor_lim_list(uuid_lim, crit):
    # fill pr_zh.cor_lim_list
    for lim in crit:
        DB.session.add(CorLimList(
            id_lim_list=uuid_lim, id_lim=lim))
        DB.session.flush()


def post_cor_zh_area(polygon, id_zh, id_type):
    query = """
        SELECT (ref_geo.fct_get_area_intersection(
        ST_SetSRID('{geom}'::geometry,4326), {type})).id_area
        """.format(geom=str(polygon), type=id_type)
    q_list = DB.session.execute(text(query)).fetchall()
    for q in q_list:
        DB.session.add(
            CorZhArea(id_area=q[0], id_zh=id_zh))
        DB.session.flush()


def post_cor_zh_rb(geom, id_zh):
    rbs = TZH.get_zh_area_intersected(
        'river_basin', func.ST_GeomFromGeoJSON(str(geom)))
    for rb in rbs:
        DB.session.add(CorZhRb(id_zh=id_zh, id_rb=rb.id_rb))
        DB.session.flush()


def post_cor_zh_hydro(geom, id_zh):
    has = TZH.get_zh_area_intersected(
        'hydro_area', func.ST_GeomFromGeoJSON(str(geom)))
    for ha in has:
        DB.session.add(CorZhHydro(
            id_zh=id_zh, id_hydro=ha.id_hydro))
        DB.session.flush()


def post_cor_zh_fct_area(geom, id_zh):
    fas = TZH.get_zh_area_intersected(
        'fct_area', func.ST_GeomFromGeoJSON(str(geom)))
    for fa in fas:
        DB.session.add(CorZhFctArea(
            id_zh=id_zh, id_fct_area=fa.id_fct_area))
        DB.session.flush()
