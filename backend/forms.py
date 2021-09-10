import uuid

from sqlalchemy import (
    func,
    text,
    # desc,
    and_
)

from sqlalchemy.sql.expression import delete

from geonature.utils.env import DB

from .models import *

from pypnnomenclature.models import (
    TNomenclatures
)

from .api_error import ZHApiError

import pdb


def update_tzh(data):

    zh = DB.session.query(TZH).filter_by(id_zh=data['id_zh']).first()
    for key, val in data.items():
        if hasattr(TZH, key) and key != 'id_zh':
            setattr(zh, key, val)
            DB.session.flush()


# tab 0


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

    DB.session.flush()
    return new_zh.id_zh


def post_cor_lim_list(uuid_lim, criteria):
    # fill pr_zh.cor_lim_list
    for lim in criteria:
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


def update_zh_tab0(form_data, polygon, info_role, zh_date):
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
        TZH.geom: polygon
    })
    DB.session.flush()

    if is_geom_new:
        update_cor_zh_area(polygon, form_data['id_zh'])
        update_cor_zh_rb(form_data['geom']['geometry'], form_data['id_zh'])
        update_cor_zh_hydro(form_data['geom']['geometry'], form_data['id_zh'])
        update_cor_zh_fct_area(
            form_data['geom']['geometry'], form_data['id_zh'])

    DB.session.flush()
    return form_data['id_zh']


def check_polygon(polygon, id_zh):
    if polygon != str(DB.session.query(TZH.geom).filter(TZH.id_zh == id_zh).one()[0]).upper():
        return True
    return False


def update_cor_zh_area(polygon, id_zh):
    DB.session.query(CorZhArea).filter(
        CorZhArea.id_zh == id_zh).delete()
    post_cor_zh_area(polygon, id_zh, 25)
    post_cor_zh_area(polygon, id_zh, 26)


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
    DB.session.query(CorZhRef).filter(
        CorZhRef.id_zh == form_data['id_zh']).delete()
    for ref in form_data['id_references']:
        DB.session.add(CorZhRef(id_zh=form_data['id_zh'], id_ref=ref))
        DB.session.flush()


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
    # delete cascade t_activity and cor_impact_list with id_zh
    DB.session.query(TActivity).filter(
        TActivity.id_zh == id_zh).delete()
    # post new activities
    post_activities(id_zh, activities)


def update_corine_biotopes(id_zh, corine_biotopes):
    DB.session.query(CorZhCb).filter(
        CorZhCb.id_zh == id_zh).delete()
    post_corine_biotopes(id_zh, corine_biotopes)


def post_corine_biotopes(id_zh, corine_biotopes):
    for corine_biotope in corine_biotopes:
        DB.session.add(CorZhCb(
            id_zh=id_zh, lb_code=corine_biotope['CB_code']))
        DB.session.flush()


def update_corine_landcover(id_zh, ids_cover):
    DB.session.query(CorZhCorineCover).filter(
        CorZhCorineCover.id_zh == id_zh).delete()
    post_corine_landcover(id_zh, ids_cover)


def post_corine_landcover(id_zh, ids_cover):
    for id in ids_cover:
        DB.session.add(CorZhCorineCover(
            id_zh=id_zh, id_cover=id))
        DB.session.flush()


# tab 2


def update_delim(id_zh, criteria):
    uuid_lim_list = DB.session.query(TZH.id_lim_list).filter(
        TZH.id_zh == id_zh).one().id_lim_list
    DB.session.query(CorLimList).filter(
        CorLimList.id_lim_list == uuid_lim_list).delete()
    post_delim(uuid_lim_list, criteria)


def post_delim(uuid_lim, criteria):
    for lim in criteria:
        DB.session.add(CorLimList(
            id_lim_list=uuid_lim, id_lim=lim))
        DB.session.flush()


def update_fct_delim(id_zh, criteria):
    DB.session.query(CorZhLimFs).filter(
        CorZhLimFs.id_zh == id_zh).delete()
    post_fct_delim(id_zh, criteria)


def post_fct_delim(id_zh, criteria):
    for lim in criteria:
        DB.session.add(CorZhLimFs(id_zh=id_zh, id_lim_fs=lim))
        DB.session.flush()


# tab 4


def update_outflow(id_zh, outflows):
    DB.session.query(TOutflow).filter(
        TOutflow.id_zh == id_zh).delete()
    post_outflow(id_zh, outflows)


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
    DB.session.query(TInflow).filter(
        TInflow.id_zh == id_zh).delete()
    post_inflow(id_zh, inflows)


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
    id_function_list = [
        nomenclature.id_nomenclature for nomenclature in Nomenclatures.get_nomenclature_info(function_type)
    ]
    DB.session.query(TFunctions).filter(TFunctions.id_zh == id_zh).filter(
        TFunctions.id_function.in_(id_function_list)).delete(synchronize_session='fetch')
    post_functions(id_zh, functions)


def update_hab_heritages(id_zh, hab_heritages):
    # delete cascade t_hab_heritages
    DB.session.query(THabHeritage).filter(
        THabHeritage.id_zh == id_zh).delete()
    # post new hab_heritages
    post_hab_heritages(id_zh, hab_heritages)


def post_hab_heritages(id_zh, hab_heritages):
    for hab_heritage in hab_heritages:
        if hab_heritage['hab_cover'] is None:
            hab_heritage['hab_cover'] = '999'
        DB.session.add(THabHeritage(
            id_zh=id_zh,
            id_corine_bio=hab_heritage['id_corine_bio'],
            id_cahier_hab=hab_heritage['id_cahier_hab'],
            id_preservation_state=hab_heritage['id_preservation_state'],
            hab_cover=hab_heritage['hab_cover']
        ))


# tab 6


def update_ownerships(id_zh, ownerships):
    DB.session.query(TOwnership).filter(
        TOwnership.id_zh == id_zh).delete()
    post_ownerships(id_zh, ownerships)


def post_ownerships(id_zh, ownerships):
    for ownership in ownerships:
        DB.session.add(
            TOwnership(
                id_status=ownership.id_status,
                id_zh=id_zh,
                remark=ownership.remark
            )
        )
        DB.session.flush()


def update_managements(id_zh, managements):
    DB.session.query(TManagementStructures).filter(
        TManagementStructures.id_zh == id_zh).delete()
    # verifier si suppression en cascade ok dans TManagementPlans
    post_managements(id_zh, managements)


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
                        duration=plan["duration"]
                    )
                )
                DB.session.flush()


def update_instruments(id_zh, instruments):
    DB.session.query(TInstruments).filter(
        TInstruments.id_zh == id_zh).delete()
    post_instruments(id_zh, instruments)


def post_instruments(id_zh, instruments):
    for instrument in instruments:
        DB.session.add(
            TInstruments(
                id_instrument=instrument.id_instrument,
                id_zh=id_zh,
                instrument_date=instrument.instrument_date
            )
        )
        DB.session.flush()


def update_protections(id_zh, protections):
    DB.session.query(CorZhProtection).filter(
        CorZhProtection.id_zh == id_zh).delete()
    post_instruments(id_zh, protections)


def post_protections(id_zh, protections):
    for protection in protections:
        DB.session.add(
            CorZhProtection(
                id_protection=protection.id_protection,
                id_zh=id_zh,
            )
        )
        DB.session.flush()


def update_zh_tab6(data):
    DB.session.query(TZH).filter(TZH.id_zh == data['id_zh']).update({
        TZH.is_other_inventory: data['is_other_inventory']
    })
    DB.session.flush()


def update_urban_docs(id_zh, urban_docs):
    DB.session.query(TUrbanPlanningDocs).filter(
        TUrbanPlanningDocs.id_zh == id_zh).delete()
    post_instruments(id_zh, TUrbanPlanningDocs)


def post_urban_docs(id_zh, urban_docs):
    for urban_doc in urban_docs:
        DB.session.add(
            TUrbanPlanningDocs(
                id_area=urban_doc.id_area,
                id_zh=id_zh,
                id_urban_type=urban_doc.id_cor,
                remark=urban_doc.remark
            )
        )
        DB.session.flush()


# tab 7


def update_actions(id_zh, actions):
    # delete cascade actions
    DB.session.query(TActions).filter(
        TActions.id_zh == id_zh).delete()
    # post new actions
    post_actions(id_zh, actions)


def post_actions(id_zh, actions):
    for action in actions:
        DB.session.add(TActions(
            id_zh=id_zh,
            id_action=action['id_action'],
            id_priority_level=action['id_priority_level'],
            remark=action['remark']
        ))
        DB.session.flush()
