import sys

from geoalchemy2.shape import to_shape
from geonature.utils.env import DB
from sqlalchemy import func
from sqlalchemy.sql import select, func
from sqlalchemy.orm import aliased

from werkzeug.exceptions import BadRequest

from .api_error import ZHApiError
from .model.zh_schema import TZH, CorZhRb, TRiverBasin

import pdb


def set_geom(geometry_geojson, id_zh=None):
    if not id_zh:
        id_zh = 0

    geometry = func.ST_SetSRID(func.ST_GeomFromGeoJSON(str(geometry_geojson)), 4326)
    # SetSRID for POSTGIS < 3.0 compat
    # select only already existing ZH geometries which intersect with the new ZH geometry
    q_zh = DB.session.scalars(
        select(TZH)
        .where(
            func.ST_Intersects(
                TZH.geom,
                geometry,
            )
        )
        .where(
            func.ST_Touches(
                TZH.geom,
                geometry,
            )
            == False
        )
    ).all()

    is_intersected = False
    polygon_geom = geometry
    for zh in q_zh:
        if zh.id_zh != id_zh:
            if DB.session.scalar(select(func.ST_Intersects(polygon_geom, zh.geom))):
                if DB.session.scalar(
                    select(func.ST_GeometryType(func.ST_Intersection(zh.geom, polygon_geom)))
                ) not in ["ST_LineString", "ST_MultiLineString"]:
                    is_intersected = True
            if DB.session.scalar(
                select(
                    func.ST_Contains(
                        zh.geom,
                        polygon_geom,
                    )
                )
            ):
                raise BadRequest("La ZH est entièrement dans une ZH existante")
                # TODO: not detected if contained entirely in 2 or more ZH polygons
            if DB.session.scalar(
                select(
                    func.ST_Contains(
                        polygon_geom,
                        zh.geom,
                    )
                )
            ):
                raise BadRequest("La ZH englobe complètement une ZH existante")
                # TODO: not detected if contained entirely in 2 or more ZH polygons

            polygon_geom = DB.session.scalar(select(func.ST_Difference(polygon_geom, zh.geom)))

    return {"polygon": polygon_geom, "is_intersected": is_intersected}


def set_area(geom):
    # unit : ha
    return round(
        (
            DB.session.scalar(
                select(func.ST_Area(func.ST_GeomFromText(func.ST_AsText(geom["polygon"])), False))
            )
        )
        / 10000,
        2,
    )


def get_main_rb(rbs, geom):
    rb_id = None
    area = 0
    for q_ in rbs:
        intersection = DB.session.scalar(
            select(
                func.ST_Intersection(
                    func.ST_GeomFromText(func.ST_AsText(func.ST_GeomFromGeoJSON(str(geom)))),
                    func.ST_GeomFromText(func.ST_AsText(getattr(q_, "geom"))),
                )
            )
        )
        if DB.session.scalar(select(func.ST_Area(intersection, False))) > area:
            area = DB.session.scalar(select(func.ST_Area(intersection, False)))
            rb_id = getattr(q_, "id_rb")
    return rb_id
