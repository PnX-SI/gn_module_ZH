import uuid

import math
import sys
import traceback
from psycopg2 import OperationalError, errorcodes, errors

import datetime

from sqlalchemy import (
    func,
    text,
    # desc,
    and_
)

import sqlalchemy.exc as exc
from sqlalchemy.sql.expression import delete

from geonature.utils.env import DB

from geonature.core.ref_geo.models import BibAreasTypes, LAreas

from geonature.core.gn_commons.models import (
    BibTablesLocation,
    TMedias
)

from .model.zh_schema import *
from .model.code import Code

from pypnnomenclature.models import (
    TNomenclatures
)

from .api_error import ZHApiError

import psycopg2

import pdb


def update_tzh(data):
    try:
        zh = DB.session.query(TZH).filter_by(id_zh=data['id_zh']).first()
        for key, val in data.items():
            if hasattr(TZH, key) and key != 'id_zh':
                setattr(zh, key, val)
                DB.session.flush()
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="update_tzh_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="update_tzh_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


# tab 0


def create_zh(form_data, info_role, zh_date, polygon, zh_area, ref_geo_referentiels):

    try:
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
            geom=polygon,
            area=zh_area
        )
        DB.session.add(new_zh)
        DB.session.flush()

        # fill cor_zh_area for municipalities
        post_cor_zh_area(polygon, new_zh.id_zh, DB.session.query(
            BibAreasTypes).filter(BibAreasTypes.type_code == 'COM').one().id_type)
        # fill cor_zh_area for departements
        post_cor_zh_area(polygon, new_zh.id_zh, DB.session.query(
            BibAreasTypes).filter(BibAreasTypes.type_code == 'DEP').one().id_type)
        # fill cor_zh_area for other geo referentials
        for ref in ref_geo_referentiels:
            post_cor_zh_area(polygon, new_zh.id_zh, DB.session.query(
                BibAreasTypes).filter(BibAreasTypes.type_code == ref['type_code_ref_geo']).one().id_type)

        # fill cor_zh_rb
        post_cor_zh_rb(form_data['geom']['geometry'], new_zh.id_zh)
        # fill cor_zh_hydro
        post_cor_zh_hydro(form_data['geom']['geometry'], new_zh.id_zh)
        # fill cor_zh_fct_area
        post_cor_zh_fct_area(form_data['geom']['geometry'], new_zh.id_zh)

        # create zh code
        code = Code(new_zh.id_zh, new_zh.id_org, new_zh.geom)
        new_zh.code = code.__repr__()

        DB.session.flush()
        return new_zh.id_zh
    except ZHApiError:
        raise
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="create_zh_post_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="create_zh_post_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_cor_lim_list(uuid_lim, criteria):
    try:
        # fill pr_zh.cor_lim_list
        for lim in criteria:
            DB.session.add(CorLimList(
                id_lim_list=uuid_lim, id_lim=lim))
            DB.session.flush()
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_cor_lim_list_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_cor_lim_list_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_cor_zh_area(polygon, id_zh, id_type):
    try:
        elements = [getattr(element, 'id_area') for element in DB.session.query(LAreas).filter(LAreas.geom.ST_Intersects(
            func.ST_Transform(func.ST_SetSRID(func.ST_AsText(polygon), 4326), 2154))).filter(LAreas.id_type == id_type).all()]
        for element in elements:
            # if 'Communes', % of zh in the municipality must be calculated
            if id_type == CorZhArea.get_id_type('Communes'):
                municipality_geom = getattr(DB.session.query(LAreas).filter(
                    LAreas.id_area == element).first(), 'geom')
                polygon_2154 = DB.session.query(func.ST_Transform(
                    func.ST_SetSRID(func.ST_AsText(polygon), 4326), 2154)).scalar()
                intersect_area = DB.session.query(func.ST_Area(
                    func.ST_Intersection(municipality_geom, polygon_2154))).scalar()
                municipality_area = DB.session.query(
                    func.ST_Area(municipality_geom)).scalar()
                cover = math.ceil((intersect_area * 100)/municipality_area)
                if cover > 100:
                    cover = 100
            else:
                cover = None
            DB.session.add(
                CorZhArea(
                    id_area=element,
                    id_zh=id_zh,
                    cover=cover
                )
            )
            DB.session.flush()
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_cor_zh_area_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_cor_zh_area_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_cor_zh_rb(geom, id_zh):
    try:
        rbs = TZH.get_zh_area_intersected(
            'river_basin', func.ST_GeomFromGeoJSON(str(geom)))
        for rb in rbs:
            DB.session.add(CorZhRb(id_zh=id_zh, id_rb=rb.id_rb))
            DB.session.flush()
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_cor_zh_rb_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_cor_zh_rb_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_cor_zh_hydro(geom, id_zh):
    try:
        has = TZH.get_zh_area_intersected(
            'hydro_area', func.ST_GeomFromGeoJSON(str(geom)))
        for ha in has:
            DB.session.add(CorZhHydro(
                id_zh=id_zh, id_hydro=ha.id_hydro))
            DB.session.flush()
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_cor_zh_hydro_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_cor_zh_hydro_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_cor_zh_fct_area(geom, id_zh):
    try:
        fas = TZH.get_zh_area_intersected(
            'fct_area', func.ST_GeomFromGeoJSON(str(geom)))
        for fa in fas:
            DB.session.add(CorZhFctArea(
                id_zh=id_zh, id_fct_area=fa.id_fct_area))
            DB.session.flush()
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_cor_zh_fct_area_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary))
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_cor_zh_fct_area_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def update_zh_tab0(form_data, polygon, area, info_role, zh_date, geo_refs):
    try:
        is_geom_new = check_polygon(polygon, form_data['id_zh'])

        # update pr_zh.cor_lim_list
        id_lim_list = DB.session.query(TZH.id_lim_list).filter(
            TZH.id_zh == form_data['id_zh']).one()[0]
        DB.session.query(CorLimList).filter(
            CorLimList.id_lim_list == id_lim_list).delete()
        post_cor_lim_list(id_lim_list, form_data['critere_delim'])

        # update zh : fill pr_zh.t_zh
        DB.session.query(TZH).filter(TZH.id_zh == form_data['id_zh']).update({
            TZH.main_name: form_data['main_name'],
            TZH.id_org: form_data['id_org'],
            TZH.update_author: info_role.id_role,
            TZH.update_date: zh_date,
            TZH.id_sdage: form_data['sdage'],
            TZH.geom: polygon,
            TZH.area: area
        })
        DB.session.flush()

        if is_geom_new:
            update_cor_zh_area(polygon, form_data['id_zh'], geo_refs)
            update_cor_zh_rb(form_data['geom']['geometry'], form_data['id_zh'])
            update_cor_zh_hydro(
                form_data['geom']['geometry'], form_data['id_zh'])
            update_cor_zh_fct_area(
                form_data['geom']['geometry'], form_data['id_zh'])

        DB.session.flush()
        return form_data['id_zh']
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="update_tab0_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="update_tab0_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def check_polygon(polygon, id_zh):
    try:
        if polygon != str(DB.session.query(TZH.geom).filter(TZH.id_zh == id_zh).one()[0]).upper():
            return True
        return False
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="check_polygon_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def update_cor_zh_area(polygon, id_zh, geo_refs):
    try:
        DB.session.query(CorZhArea).filter(
            CorZhArea.id_zh == id_zh).delete()
        post_cor_zh_area(polygon, id_zh, DB.session.query(BibAreasTypes).filter(
            BibAreasTypes.type_code == 'COM').one().id_type)
        post_cor_zh_area(polygon, id_zh, DB.session.query(BibAreasTypes).filter(
            BibAreasTypes.type_code == 'DEP').one().id_type)
        # fill cor_zh_area for other geo referentials
        for ref in geo_refs:
            post_cor_zh_area(polygon, id_zh, DB.session.query(
                BibAreasTypes).filter(BibAreasTypes.type_code == ref['type_code_ref_geo']).one().id_type)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="update_cor_zh_area_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="update_cor_zh_area_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def update_cor_zh_rb(geom, id_zh):
    DB.session.query(CorZhRb).filter(
        CorZhRb.id_zh == id_zh).delete()
    post_cor_zh_rb(geom, id_zh)


def update_cor_zh_hydro(geom, id_zh):
    DB.session.query(CorZhHydro).filter(
        CorZhHydro.id_zh == id_zh).delete()
    post_cor_zh_hydro(geom, id_zh)


def update_cor_zh_fct_area(geom, id_zh):
    DB.session.query(CorZhFctArea).filter(
        CorZhFctArea.id_zh == id_zh).delete()
    post_cor_zh_fct_area(geom, id_zh)


# tab 1


def update_refs(form_data):
    try:
        DB.session.query(CorZhRef).filter(
            CorZhRef.id_zh == form_data['id_zh']).delete()
        for ref in form_data['id_references']:
            DB.session.add(CorZhRef(id_zh=form_data['id_zh'], id_ref=ref))
            DB.session.flush()
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="update_refs_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="update_refs_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


# tab 3


def post_activities(id_zh, activities):
    for activity in activities:
        uuid_activity = uuid.uuid4()
        DB.session.add(TActivity(
            id_activity=activity['human_activity']['id_nomenclature'],
            id_zh=id_zh,
            id_position=activity['localisation']['id_nomenclature'],
            id_impact_list=uuid_activity,
            remark_activity=activity['remark_activity']
        ))
        DB.session.flush()
        for impact in activity['impacts']['impacts']:
            DB.session.add(CorImpactList(
                id_impact_list=uuid_activity,
                id_cor_impact_types=impact['id_cor_impact_types']
            ))
            DB.session.flush()


def update_activities(id_zh, activities):
    try:
        # delete cascade t_activity and cor_impact_list with id_zh
        DB.session.query(TActivity).filter(
            TActivity.id_zh == id_zh).delete()
        # post new activities
        post_activities(id_zh, activities)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_activities_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_activities_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def update_corine_biotopes(id_zh, corine_biotopes):
    try:
        DB.session.query(CorZhCb).filter(
            CorZhCb.id_zh == id_zh).delete()
        post_corine_biotopes(id_zh, corine_biotopes)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_corine_biotopes_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_corine_biotopes_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_corine_biotopes(id_zh, corine_biotopes):
    for corine_biotope in corine_biotopes:
        DB.session.add(CorZhCb(
            id_zh=id_zh, lb_code=corine_biotope['CB_code']))
        DB.session.flush()


def update_corine_landcover(id_zh, ids_cover):
    try:
        DB.session.query(CorZhCorineCover).filter(
            CorZhCorineCover.id_zh == id_zh).delete()
        post_corine_landcover(id_zh, ids_cover)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_corine_landcover_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_corine_landcover_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_corine_landcover(id_zh, ids_cover):
    for id in ids_cover:
        DB.session.add(CorZhCorineCover(
            id_zh=id_zh, id_cover=id))
        DB.session.flush()


# tab 2


def update_delim(id_zh, criteria):
    try:
        uuid_lim_list = DB.session.query(TZH.id_lim_list).filter(
            TZH.id_zh == id_zh).one().id_lim_list
        DB.session.query(CorLimList).filter(
            CorLimList.id_lim_list == uuid_lim_list).delete()
        post_delim(uuid_lim_list, criteria)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_delim_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_delim_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_delim(uuid_lim, criteria):
    for lim in criteria:
        DB.session.add(CorLimList(
            id_lim_list=uuid_lim, id_lim=lim))
        DB.session.flush()


def update_fct_delim(id_zh, criteria):
    try:
        DB.session.query(CorZhLimFs).filter(
            CorZhLimFs.id_zh == id_zh).delete()
        post_fct_delim(id_zh, criteria)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_fct_delim_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_fct_delim_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_fct_delim(id_zh, criteria):
    for lim in criteria:
        DB.session.add(CorZhLimFs(id_zh=id_zh, id_lim_fs=lim))
        DB.session.flush()


# tab 4


def update_outflow(id_zh, outflows):
    try:
        DB.session.query(TOutflow).filter(
            TOutflow.id_zh == id_zh).delete()
        post_outflow(id_zh, outflows)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_outflow_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_outflow_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_outflow(id_zh, outflows):
    for outflow in outflows:
        DB.session.add(
            TOutflow(
                id_outflow=outflow['id_outflow'],
                id_zh=id_zh,
                id_permanance=outflow['id_permanance'],
                topo=outflow['topo']
            )
        )
        DB.session.flush()


def update_inflow(id_zh, inflows):
    try:
        DB.session.query(TInflow).filter(
            TInflow.id_zh == id_zh).delete()
        post_inflow(id_zh, inflows)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_inflow_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_inflow_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_inflow(id_zh, inflows):
    for inflow in inflows:
        DB.session.add(
            TInflow(
                id_inflow=inflow['id_inflow'],
                id_zh=id_zh,
                id_permanance=inflow['id_permanance'],
                topo=inflow['topo']
            )
        )
        DB.session.flush()


# tab 5


def post_functions(id_zh, functions):

    for function in functions:
        DB.session.add(TFunctions(
            id_function=function['id_function'],
            id_zh=id_zh,
            justification=function['justification'],
            id_qualification=function['id_qualification'],
            id_knowledge=function['id_knowledge']
        ))
        DB.session.flush()


def update_functions(id_zh, functions, function_type):
    try:
        id_function_list = [
            nomenclature.id_nomenclature for nomenclature in Nomenclatures.get_nomenclature_info(function_type)
        ]
        DB.session.query(TFunctions).filter(TFunctions.id_zh == id_zh).filter(
            TFunctions.id_function.in_(id_function_list)).delete(synchronize_session='fetch')
        post_functions(id_zh, functions)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_functions_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_functions_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def update_hab_heritages(id_zh, hab_heritages):
    try:
        # delete cascade t_hab_heritages
        DB.session.query(THabHeritage).filter(
            THabHeritage.id_zh == id_zh).delete()
        # post new hab_heritages
        post_hab_heritages(id_zh, hab_heritages)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_hab_heritages_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_hab_heritages_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_hab_heritages(id_zh, hab_heritages):
    for hab_heritage in hab_heritages:
        DB.session.add(THabHeritage(
            id_zh=id_zh,
            id_corine_bio=hab_heritage['id_corine_bio'],
            id_cahier_hab=hab_heritage['id_cahier_hab'],
            id_preservation_state=hab_heritage['id_preservation_state'],
            hab_cover=hab_heritage['hab_cover']
        ))


# tab 6


def update_ownerships(id_zh, ownerships):
    try:
        DB.session.query(TOwnership).filter(
            TOwnership.id_zh == id_zh).delete()
        post_ownerships(id_zh, ownerships)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_ownerships_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_ownerships_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_ownerships(id_zh, ownerships):
    for ownership in ownerships:
        DB.session.add(
            TOwnership(
                id_status=ownership['id_status'],
                id_zh=id_zh,
                remark=ownership['remark']
            )
        )
        DB.session.flush()


def update_managements(id_zh, managements):
    try:
        DB.session.query(TManagementStructures).filter(
            TManagementStructures.id_zh == id_zh).delete()
        # verifier si suppression en cascade ok dans TManagementPlans
        post_managements(id_zh, managements)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_managements_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_managements_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_managements(id_zh, managements):
    for management in managements:
        DB.session.add(
            TManagementStructures(
                id_zh=id_zh,
                id_org=management["structure"]
            )
        )
        DB.session.flush()
        if management["plans"]:
            for plan in management["plans"]:
                DB.session.add(
                    TManagementPlans(
                        id_nature=plan["id_nature"],
                        id_structure=DB.session.query(TManagementStructures).filter(and_(
                            TManagementStructures.id_zh == id_zh, TManagementStructures.id_org == management["structure"])).one().id_structure,
                        plan_date=plan["plan_date"],
                        duration=plan["duration"],
                        remark=plan["remark"]
                    )
                )
                DB.session.flush()


def update_instruments(id_zh, instruments):
    try:
        DB.session.query(TInstruments).filter(
            TInstruments.id_zh == id_zh).delete()
        post_instruments(id_zh, instruments)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_instruments_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_instruments_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_instruments(id_zh, instruments):
    for instrument in instruments:
        DB.session.add(
            TInstruments(
                id_instrument=instrument["id_instrument"],
                id_zh=id_zh,
                instrument_date=instrument["instrument_date"]
            )
        )
        DB.session.flush()


def update_protections(id_zh, protections):
    try:
        DB.session.query(CorZhProtection).filter(
            CorZhProtection.id_zh == id_zh).delete()
        post_protections(id_zh, protections)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_update_protections_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="post_update_protections_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_protections(id_zh, protections):
    for protection in protections:
        DB.session.add(
            CorZhProtection(
                id_protection=DB.session.query(CorProtectionLevelType).filter(
                    CorProtectionLevelType.id_protection_status == protection).one().id_protection,
                id_zh=id_zh,
            )
        )
        DB.session.flush()


def update_zh_tab6(data):
    try:
        is_other_inventory = data['is_other_inventory']
        DB.session.query(TZH).filter(TZH.id_zh == data['id_zh']).update({
            TZH.update_author: data['update_author'],
            TZH.update_date: data['update_date'],
            TZH.is_other_inventory: is_other_inventory,
            TZH.remark_is_other_inventory: data['remark_is_other_inventory'] if is_other_inventory else None
        })
        DB.session.flush()
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="update_zh_tab6_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="update_zh_tab6_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def update_urban_docs(id_zh, urban_docs):
    try:
        DB.session.query(TUrbanPlanningDocs).filter(
            TUrbanPlanningDocs.id_zh == id_zh).delete()
        post_urban_docs(id_zh, urban_docs)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="update_urban_docs_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="update_urban_docs_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_urban_docs(id_zh, urban_docs):
    for urban_doc in urban_docs:
        id_doc_type = DB.session.query(CorUrbanTypeRange).filter(
            CorUrbanTypeRange.id_cor == urban_doc["id_urban_type"][0]["id_cor"]).one().id_doc_type
        uuid_doc = uuid.uuid4()
        DB.session.add(
            TUrbanPlanningDocs(
                id_area=urban_doc["id_area"],
                id_zh=id_zh,
                id_doc_type=id_doc_type,
                id_doc=uuid_doc,
                remark=urban_doc["remark"]
            )
        )
        DB.session.flush()
        for type in urban_doc["id_urban_type"]:
            DB.session.add(
                CorZhDocRange(
                    id_doc=uuid_doc,
                    id_cor=type["id_cor"]
                )
            )
            DB.session.flush()


# tab 7


def update_actions(id_zh, actions):
    try:
        # delete cascade actions
        DB.session.query(TActions).filter(
            TActions.id_zh == id_zh).delete()
        # post new actions
        post_actions(id_zh, actions)
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="update_actions_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="update_actions_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def post_actions(id_zh, actions):
    for action in actions:
        DB.session.add(TActions(
            id_zh=id_zh,
            id_action=action['id_action'],
            id_priority_level=action['id_priority_level'],
            remark=action['remark']
        ))
        DB.session.flush()


# tab 8


def post_file_info(id_zh, title, author, description, extension, media_path=None):
    try:
        unique_id_media = DB.session.query(TZH).filter(
            TZH.id_zh == int(id_zh)).one().zh_uuid
        uuid_attached_row = uuid.uuid4()
        if extension == '.pdf':
            mnemo = 'PDF'
        elif extension == '.csv':
            mnemo = 'Tableur'
        else:
            mnemo = 'Photo'
        id_nomenclature_media_type = DB.session.query(TNomenclatures).filter(
            TNomenclatures.mnemonique == mnemo).one().id_nomenclature
        id_table_location = DB.session.query(BibTablesLocation).filter(and_(
            BibTablesLocation.schema_name == 'pr_zh', BibTablesLocation.table_name == 't_zh')).one().id_table_location
        post_date = datetime.datetime.now()
        DB.session.add(TMedias(
            unique_id_media=unique_id_media,
            id_nomenclature_media_type=id_nomenclature_media_type,
            id_table_location=id_table_location,
            uuid_attached_row=uuid_attached_row,
            title_fr=title,
            author=author,
            description_fr=description,
            is_public=True,
            media_path=media_path,
            meta_create_date=str(post_date),
            meta_update_date=str(post_date)
        ))
        DB.session.commit()
        id_media = DB.session.query(TMedias).filter(
            TMedias.uuid_attached_row == uuid_attached_row).one().id_media
        return id_media
    except Exception as e:
        if e.__class__.__name__ == 'DataError':
            raise ZHApiError(
                message="post_file_info_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
        raise ZHApiError(message="post_file_info_error", details=str(e))


def patch_file_info(id_zh, id_media, title, author, description):
    try:
        unique_id_media = DB.session.query(TZH).filter(
            TZH.id_zh == int(id_zh)).one().zh_uuid
        uuid_attached_row = uuid.uuid4()
        id_table_location = DB.session.query(BibTablesLocation).filter(and_(
            BibTablesLocation.schema_name == 'pr_zh', BibTablesLocation.table_name == 't_zh')).one().id_table_location
        post_date = datetime.datetime.now()
        DB.session.query(TMedias).filter(TMedias.id_media == id_media).update({
            'unique_id_media': unique_id_media,
            'id_table_location': id_table_location,
            'uuid_attached_row': uuid_attached_row,
            'title_fr': title,
            'author': author,
            'description_fr': description,
            'is_public': True,
            'meta_update_date': str(post_date)
        })
        DB.session.flush()
    except exc.DataError as e:
        raise ZHApiError(
            message="patch_file_info_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
    except Exception as e:
        raise ZHApiError(message="patch_file_info_error", details=str(e))


def update_file_extension(id_media, extension):
    try:
        if extension == '.pdf':
            mnemo = 'PDF'
        elif extension == '.csv':
            mnemo = 'Tableur'
        else:
            mnemo = 'Photo'
        id_nomenclature_media_type = DB.session.query(TNomenclatures).filter(
            TNomenclatures.mnemonique == mnemo).one().id_nomenclature
        DB.session.query(TMedias).filter(TMedias.id_media == id_media).update({
            'id_nomenclature_media_type': id_nomenclature_media_type
        })
        DB.session.flush()
    except exc.DataError as e:
        raise ZHApiError(
            message="update_file_extension_db_error", details=str(e.orig.diag.sqlstate + ': ' + e.orig.diag.message_primary), status_code=400)
    except Exception as e:
        raise ZHApiError(message="update_file_extension_error", details=str(e))
