from geonature.utils.env import DB

from sqlalchemy import func

from geoalchemy2.shape import to_shape

from .model.zh_schema import TZH


def set_geom(geometry, id_zh=None):
    if not id_zh:
        id_zh = 0
    polygon = DB.session.query(
        func.ST_GeomFromGeoJSON(str(geometry))).one()[0]
    q_zh = DB.session.query(TZH).all()
    for zh in q_zh:
        if zh.id_zh != id_zh:
            intersect = DB.session.query(
                func.ST_Difference(polygon, zh.geom))
            polygon = DB.session.query(func.ST_GeomFromText(
                to_shape(intersect.scalar()).to_wkt())).one()[0]
    return polygon
