import datetime
import pytest
from geonature.utils.env import db

from shapely import Polygon
import geoalchemy2

import uuid


def printobj(obj):
    print("\n\n\nObj => ")
    for key, value in obj.__dict__.items():
        # if not key.startswith('_'):  # Ignore les attributs privés
        print(f"{key}: {value}")
    print("\n\n\n")


def create_river_basin(id_rb, name, geom, id_climate_class, id_river_flow):
    from gn_module_zh.model.zh_schema import TRiverBasin

    rb = TRiverBasin(
        id_rb=id_rb,
        name=name,
        geom=geom,
        id_climate_class=id_climate_class,
        id_river_flow=id_river_flow,
    )
    return rb


def create_t_rules(rule_id, abbreviation, pane_id, cat_id, subcat_id):
    from gn_module_zh.model.zh_schema import TRules

    rule = TRules(
        rule_id=rule_id,
        abbreviation=abbreviation,
        pane_id=pane_id,
        cat_id=cat_id,
        subcat_id=subcat_id,
    )
    return rule


def create_item(
    val_id,
    cor_rule_id,
    attribute_id,
    note,
    note_type_id,
):
    from gn_module_zh.model.zh_schema import TItems

    item = TItems(
        val_id=val_id,
        cor_rule_id=cor_rule_id,
        attribute_id=attribute_id,
        note=note,
        note_type_id=note_type_id,
    )
    return item


def create_cor_rb_rules(cor_rule_id, rb_id, rule_id):
    from gn_module_zh.model.zh_schema import CorRbRules

    cor_rb_rule = CorRbRules(cor_rule_id=cor_rule_id, rb_id=rb_id, rule_id=rule_id)
    return cor_rb_rule


@pytest.fixture(scope="function")
def rb_data(users):
    coords = (
        (-6.811523, 42.228517),
        (9.799805, 42.228517),
        (9.799805, 51.454007),
        (-6.811523, 51.454007),
        (-6.811523, 42.228517),
    )
    polygon = Polygon(coords)
    data = {}
    with db.session.begin_nested():
        for (
            id_rb,
            name,
            geom,
            id_climate_class,
            id_river_flow,
        ) in [
            (
                1,
                "rb1",
                geoalchemy2.shape.from_shape(polygon),
                None,
                None,
            ),
        ]:
            kwargs = {}
            s = create_river_basin(
                id_rb,
                name,
                geom,
                id_climate_class,
                id_river_flow,
            )
            db.session.add(s)
            data[name] = s
    return data


def create_zh(
    main_name,
    code,
    id_org,
    id_role,
    zh_date,
    uuid_id_lim_list,
    id_sdage,
    polygon,
    zh_area,
    main_id_rb,
    **kwargs,
):
    # Import here because TZH class need to be imported after "app instanced"
    from gn_module_zh.model.zh_schema import TZH

    zh = TZH(
        main_name=main_name,
        code=code,
        id_org=id_org,
        create_author=id_role,
        update_author=id_role,
        create_date=zh_date,
        update_date=zh_date,
        id_lim_list=uuid_id_lim_list,
        id_sdage=id_sdage,
        geom=polygon,
        area=zh_area,
        main_id_rb=main_id_rb,
    )
    return zh


@pytest.fixture(scope="function")
def zh_data(users):
    coords = (
        (-6.811523, 42.228517),
        (9.799805, 42.228517),
        (9.799805, 51.454007),
        (-6.811523, 51.454007),
        (-6.811523, 42.228517),
    )
    polygon = Polygon(coords)
    rb = create_river_basin(1, "rb1", geoalchemy2.shape.from_shape(polygon), None, None)
    db.session.add(rb)

    cor_sdage_rule = create_cor_rb_rules(1, 1, 1)
    db.session.add(cor_sdage_rule)
    item = create_item(1, cor_sdage_rule.rule_id, cor_sdage_rule.rule_id, 75, 1)
    db.session.add(item)

    # cor_hab_rule = create_cor_rb_rules(2, 1, 2)
    # db.session.add(cor_hab_rule)
    # item = create_item(2, cor_hab_rule.rule_id, cor_hab_rule.rule_id, 75, 1)
    # db.session.add(item)
    #
    # cor_flore_rule = create_cor_rb_rules(3, 1, 3)
    # db.session.add(cor_flore_rule)
    # item = create_item(3, cor_flore_rule.rule_id, cor_flore_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_vertebrates_rule = create_cor_rb_rules(4, 1, 4)
    # db.session.add(cor_vertebrates_rule)
    # item = create_item(4, cor_vertebrates_rule.rule_id, cor_vertebrates_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_invertebrates_rule = create_cor_rb_rules(5, 1, 5)
    # db.session.add(cor_invertebrates_rule)
    # item = create_item(5, cor_invertebrates_rule.rule_id, cor_invertebrates_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_eco_rule = create_cor_rb_rules(6, 1, 6)
    # db.session.add(cor_eco_rule)
    # item = create_item(6, cor_eco_rule.rule_id, cor_eco_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_protection_rule = create_cor_rb_rules(7, 1, 7)
    # db.session.add(cor_protection_rule)
    # item = create_item(7, cor_protection_rule.rule_id, cor_protection_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_epuration_rule = create_cor_rb_rules(8, 1, 8)
    # db.session.add(cor_epuration_rule)
    # item = create_item(8, cor_epuration_rule.rule_id, cor_epuration_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_support_rule = create_cor_rb_rules(9, 1, 9)
    # db.session.add(cor_support_rule)
    # item = create_item(9, cor_support_rule.rule_id, cor_support_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_pedagogy_rule = create_cor_rb_rules(10, 1, 10)
    # db.session.add(cor_pedagogy_rule)
    # item = create_item(10, cor_pedagogy_rule.rule_id, cor_pedagogy_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_production_rule = create_cor_rb_rules(11, 1, 11)
    # db.session.add(cor_production_rule)
    # item = create_item(11, cor_production_rule.rule_id, cor_production_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_status_rule = create_cor_rb_rules(12, 1, 12)
    # db.session.add(cor_status_rule)
    # item = create_item(12, cor_status_rule.rule_id, cor_status_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_management_rule = create_cor_rb_rules(13, 1, 13)
    # db.session.add(cor_management_rule)
    # item = create_item(13, cor_management_rule.rule_id, cor_management_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_hydro_rule = create_cor_rb_rules(14, 1, 14)
    # db.session.add(cor_hydro_rule)
    # item = create_item(14, cor_hydro_rule.rule_id, cor_hydro_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_bio_rule = create_cor_rb_rules(15, 1, 15)
    # db.session.add(cor_bio_rule)
    # item = create_item(15, cor_bio_rule.rule_id, cor_bio_rule.rule_id, 75, 1)
    # db.session.add(item)

    # cor_thread_rule = create_cor_rb_rules(16, 1, 16)
    # db.session.add(cor_thread_rule)
    # item = create_item(16, cor_thread_rule.rule_id, cor_thread_rule.rule_id, 75, 1)
    # db.session.add(item)

    coords = (
        (1.307287, 43.56357),
        (1.312222, 43.56357),
        (1.312222, 43.566182),
        (1.307287, 43.566182),
        (1.307287, 43.56357),
    )
    polygon = Polygon(coords)
    date = datetime.datetime(2024, 10, 2, 11, 22, 33)
    id_sdage = cor_sdage_rule.rule_id
    # hab =
    # flore =
    # vertebrates =
    # invertebrates =
    # eco =
    # protection =
    # epuration =
    # support =
    # pedagogy =
    # production =
    # status =
    # management =
    # hydro =
    # bio =
    # thread =

    user = users["self_user"]
    data = {}
    data["rb1"] = rb
    data["cor_rule"] = cor_sdage_rule
    with db.session.begin_nested():
        for (
            main_name,
            code,
            id_org,
            id_role,
            zh_date,
            uuid_id_lim_list,
            id_sdage,
            geom,
            zh_area,
            main_id_rb,
        ) in [
            (
                "zh1",
                "05CEN0189",
                2,  # id_org = 2 (not dynamic) because not same table bib_organismes used with the users
                user.id_role,
                date,
                uuid.uuid4(),
                id_sdage,
                geoalchemy2.shape.from_shape(polygon),
                polygon.area,
                1,
            ),
        ]:
            kwargs = {}
            s = create_zh(
                main_name,
                code,
                id_org,
                id_role,
                zh_date,
                uuid_id_lim_list,
                id_sdage,
                geom,
                zh_area,
                main_id_rb,
                **kwargs,
            )
            db.session.add(s)
            data[main_name] = s
    return data
