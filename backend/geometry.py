from geonature.utils.env import DB

from sqlalchemy import func

from geoalchemy2.shape import to_shape

from .models import TZH


def set_geom(geometry):
    polygon = DB.session.query(func.ST_GeomFromGeoJSON(str(geometry))).one()[0]
    q_zh = DB.session.query(TZH).all()
    for q in q_zh:
        intersect = DB.session.query(func.ST_Difference(polygon, q.geom))
        polygon = DB.session.query(func.ST_GeomFromText(
            to_shape(intersect.scalar()).to_wkt())).one()[0]
    return polygon
