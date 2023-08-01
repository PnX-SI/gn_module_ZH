import sys

from geoalchemy2.shape import to_shape
from geonature.utils.env import DB
from sqlalchemy import func
from werkzeug.exceptions import BadRequest

from .api_error import ZHApiError
from .model.zh_schema import TZH, CorZhRb, TRiverBasin

import pdb

def set_geom(geometry, id_zh=None):
    if not id_zh:
        id_zh = 0
    # SetSRID for POSTGIS < 3.0 compat

    # select only already existing ZH geometries which intersect with the new ZH geometry
    q_zh = (
        DB.session.query(TZH)
        .filter(
            func.ST_Intersects(
                func.ST_GeogFromWKB(func.ST_AsEWKB(TZH.geom)),
                func.ST_GeogFromWKB(func.ST_AsEWKB(str(geometry))),
            )
        )
        .filter(
            func.ST_Touches(
                func.ST_GeomFromWKB(func.ST_AsEWKB(TZH.geom),4326),
                func.ST_GeomFromWKB(func.ST_AsEWKB(str(geometry)),4326),
            ) == False
        )
        .all()
    )

    is_intersected = False
    for zh in q_zh:
        if zh.id_zh != id_zh:
            zh_geom = DB.session.query(func.ST_GeogFromWKB(func.ST_AsEWKB(zh.geom))).scalar()
            polygon_geom = DB.session.query(func.ST_GeogFromWKB(func.ST_AsEWKB(str(geometry)))).scalar()
            if DB.session.query(func.ST_Intersects(polygon_geom, zh_geom)).scalar():
                if DB.session.query(func.ST_GeometryType(func.ST_Intersection(zh_geom, polygon_geom, 0.1))).scalar() not in ['ST_LineString','ST_MultiLineString']:
                    is_intersected = True
            if DB.session.query(
                func.ST_Contains(
                    zh_geom,
                    polygon_geom,
                )
            ).scalar():
                raise BadRequest("La ZH est entièrement dans une ZH existante")
                # TODO: not detected if contained entirely in 2 or more ZH polygons
            polygon = DB.session.query(func.ST_Difference(polygon_geom, zh_geom)).scalar()
    return {"polygon": polygon, "is_intersected": is_intersected}


def set_area(geom):
    # unit : ha
    return round(
        (
            DB.session.query(
                func.ST_Area(func.ST_GeomFromText(func.ST_AsText(geom["polygon"])), False)
            ).scalar()
        )
        / 10000,
        2,
    )


def get_main_rb(query: list) -> int:
    rb_id = None
    area = 0
    for q_ in query:
        zh_polygon = (
            DB.session.query(TZH.geom).filter(TZH.id_zh == getattr(q_, "id_zh")).first().geom
        )
        rb_polygon = (
            DB.session.query(CorZhRb, TRiverBasin)
            .join(TRiverBasin, TRiverBasin.id_rb == CorZhRb.id_rb)
            .filter(TRiverBasin.id_rb == getattr(q_, "id_rb"))
            .first()
            .TRiverBasin.geom
        )
        intersection = DB.session.query(
            func.ST_Intersection(
                func.ST_GeomFromText(func.ST_AsText(zh_polygon)),
                func.ST_GeomFromText(func.ST_AsText(rb_polygon)),
            )
        ).scalar()
        if DB.session.query(func.ST_Area(intersection, False)).scalar() > area:
            area = DB.session.query(func.ST_Area(intersection, False)).scalar()
            rb_id = getattr(q_, "id_rb")
    return rb_id
