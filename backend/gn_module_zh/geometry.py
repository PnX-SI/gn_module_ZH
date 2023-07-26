import sys

from geoalchemy2.shape import to_shape
from geonature.utils.env import DB
from sqlalchemy import func
from werkzeug.exceptions import BadRequest

from .api_error import ZHApiError
from .model.zh_schema import TZH, CorZhRb, TRiverBasin


def set_geom(geometry, id_zh=None):
    if not id_zh:
        id_zh = 0
    # SetSRID for POSTGIS < 3.0 compat

    # set new ZH geometry (in WGS84 projection)
    polygon = DB.session.query(
        func.ST_SetSRID(func.ST_GeomFromGeoJSON(str(geometry)), 4326)
    ).one()[0]

    # select only already existing ZH polygons which intersect with the new ZH polygon
    q_zh = (
        DB.session.query(TZH)
        .filter(
            # !!! some ZH polygons won't be filtered here (ST_Intersects=True) when they have a shared borders,
            # !!! while some other ZH with shared borders will be filtered.
            # => probably because of small approximation errors when ZH are cropped with PostGis (ST_Difference)
            # => so, ST_Intersects, ST_Touches or other PostGis methods won't be able here to detect if it is a shared
            # border or a real intersection
            func.ST_Intersects(
                func.ST_GeogFromWKB(func.ST_AsEWKB(TZH.geom)),
                func.ST_GeomFromGeoJSON(str(geometry)),
            )
        )
        .all()
    )

    is_intersected = False
    for zh in q_zh:
        if zh.id_zh != id_zh:
            zh_geom = DB.session.query(func.ST_GeogFromWKB(func.ST_AsEWKB(zh.geom))).scalar()
            polygon_geom = DB.session.query(func.ST_GeogFromWKB(func.ST_AsEWKB(polygon))).scalar()
            if DB.session.query(func.ST_Intersects(polygon_geom, zh_geom)).scalar():
                # !!! because some ZH polygons which share borders with the new polygon are not previously
                # !!! filtered (see comment above), we needed to find a way to detect ZH with shared
                # !!! border but which not really intersect each other : 
                # Here we consider that intersecting area < 0.001% of each global ZH area is a shared border
                interection_area = (DB.session.query(func.ST_Area(func.ST_Intersection(polygon_geom, zh_geom), False)).scalar())/10000
                polygon_geom_area = (DB.session.query(func.ST_Area(polygon_geom, False)).scalar())/10000
                zh_geom_area = (DB.session.query(func.ST_Area(zh_geom, False)).scalar())/10000
                per_intersection_polygon_geom = (interection_area/polygon_geom_area)*100
                per_intersection_zh_geom = (interection_area/zh_geom_area)*100
                if (per_intersection_polygon_geom > 0.001 and per_intersection_zh_geom > 0.001):
                    is_intersected = True
                
            if DB.session.query(
                func.ST_Contains(
                    func.ST_GeomFromText(func.ST_AsText(zh_geom)),
                    func.ST_GeomFromText(func.ST_AsText(polygon_geom)),
                )
            ).scalar():
                raise BadRequest("La ZH est entièrement dans une ZH existante")
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
