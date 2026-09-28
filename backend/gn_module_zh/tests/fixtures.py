import csv
import datetime

import geoalchemy2
import pytest
import uuid
from geonature.utils.env import db
from ref_geo.models import LAreas
from shapely.geometry import MultiPolygon
from shapely import Polygon, wkt
import geoalchemy2.shape


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
    )
    return zh


@pytest.fixture(scope="function")
def zh_data(users):
    date = datetime.datetime(2024, 10, 2, 11, 22, 33)
    id_sdage = 967
    user = users["self_user"]
    data = {}
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
        ) in [
            (
                "zh1",
                "05CEN0189",
                2,  # id_org = 2 (not dynamic) because not same table bib_organismes used with the users
                user.id_role,
                date,
                uuid.uuid4(),
                id_sdage,
                geoalchemy2.shape.from_shape(
                    Polygon(
                        (
                            (0.949631, 43.587447),
                            (0.963364, 43.685843),
                            (1.159744, 43.686836),
                            (1.140518, 43.601372),
                            (0.949631, 43.587447),
                        )
                    )
                ),
                Polygon(
                    (
                        (0.949631, 43.587447),
                        (0.963364, 43.685843),
                        (1.159744, 43.686836),
                        (1.140518, 43.601372),
                        (0.949631, 43.587447),
                    )
                ).area,
            ),
            (
                "zh2",
                "05CEN0190",
                3,  # id_org = 2 (not dynamic) because not same table bib_organismes used with the users
                user.id_role,
                date,
                uuid.uuid4(),
                id_sdage,
                geoalchemy2.shape.from_shape(
                    Polygon(
                        (
                            (6.536951065063476, 43.92445000463151),
                            (6.536951065063477, 43.930075358202956),
                            (6.546220779418944, 43.930075358202956),
                            (6.546220779418944, 43.9244500046315),
                            (6.536951065063476, 43.92445000463151),
                        )
                    )
                ),
                Polygon(
                    (
                        (6.536951065063476, 43.92445000463151),
                        (6.536951065063477, 43.930075358202956),
                        (6.546220779418944, 43.930075358202956),
                        (6.546220779418944, 43.9244500046315),
                        (6.536951065063476, 43.92445000463151),
                    )
                ).area,
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
                **kwargs,
            )
            db.session.add(s)
            data[main_name] = s
    return data


@pytest.fixture(scope="function")
def ref_geo_data():
    areas = db.session.query(LAreas).all()
    csv.field_size_limit(int(1e7))  # 10 millions de caractères

    with open("backend/gn_module_zh/tests/l_areas.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            with db.session.begin_nested():
                # Parse geometries
                geom_shape = wkt.loads(row["geom"])
                geom_4326_shape = wkt.loads(row["geom_4326"])
                
                if geom_shape.geom_type == 'Polygon':
                    geom_shape = MultiPolygon([geom_shape])
                if geom_4326_shape.geom_type == 'Polygon':
                    geom_4326_shape = MultiPolygon([geom_4326_shape])
                
                # Convert to GeoAlchemy2 format
                geom = geoalchemy2.shape.from_shape(geom_shape, srid=2154)
                geom_4326 = geoalchemy2.shape.from_shape(geom_4326_shape, srid=4326)
                
                area = LAreas(
                    id_area=row["id_area"],
                    area_name=row["area_name"],
                    area_code=row["area_code"],
                    id_type=row["id_type"],
                    geom=geom,
                    geom_4326=geom_4326,
                )
                db.session.merge(area)
                db.session.commit()
        areas = db.session.query(LAreas).all()
        return areas
