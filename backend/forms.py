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
    try:
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
        code = Code(new_zh.id_zh, new_zh.id_org, new_zh.geom)
        # pdb.set_trace()
        if code.is_valid_number:
            new_zh.code = str(code)
        else:
            return {
                "code error": "zh_number_greater_than_9999"
            }, 500

        DB.session.commit()

        return new_zh.id_zh, 200
    except Exception as e:
        pdb.set_trace()
        if e.__class__.__name__ == 'KeyError' or e.__class__.__name__ == 'TypeError':
            return 'Empty mandatory field', 400
        if e.__class__.__name__ == 'IntegrityError':
            return 'ZH main_name already exists', 400
        DB.session.rollback()
        raise ZHApiError(message=str(e), details=str(e))
