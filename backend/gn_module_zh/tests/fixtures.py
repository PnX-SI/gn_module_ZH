import datetime
import pytest
from geonature.utils.env import db

from shapely import Polygon
import geoalchemy2

import uuid

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
    coords = ((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.))
    polygon = Polygon(coords)
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
                2, # id_org = 2 (not dynamic) because not same table bib_organismes used with the users
                user.id_role,
                date,
                uuid.uuid4(),
                id_sdage,
                geoalchemy2.shape.from_shape(polygon),
                polygon.area,
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
