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


def set_geom(geometry, id_zh=None):
    if not id_zh:
        id_zh = 0
    # SetSRID for POSTGIS < 3.0 compat
    # select only already existing ZH geometries which intersect with the new ZH geometry
    q_zh = DB.session.scalars(
        select(TZH)
        .where(
            func.ST_Intersects(
                func.ST_GeogFromWKB(func.ST_AsEWKB(TZH.geom)),
                func.ST_GeogFromWKB(func.ST_AsEWKB(func.ST_GeomFromGeoJSON(str(geometry)))),
            )
        )
        .where(
            func.ST_Touches(
                func.ST_GeomFromWKB(func.ST_AsEWKB(TZH.geom), 4326),
                func.ST_GeomFromWKB(func.ST_AsEWKB(func.ST_GeomFromGeoJSON(str(geometry))), 4326),
            )
            == False
        )
    ).all()

    is_intersected = False
    polygon = DB.session.scalar(
        select(func.ST_SetSRID(func.ST_GeomFromGeoJSON(str(geometry)), 4326))
    )
    for zh in q_zh:
        if zh.id_zh != id_zh:
            zh_geom = DB.session.scalar(select(func.ST_GeogFromWKB(func.ST_AsEWKB(zh.geom))))
            polygon_geom = DB.session.scalar(
                select(func.ST_GeogFromWKB(func.ST_AsEWKB(str(geometry))))
            )
            if DB.session.scalar(select(func.ST_Intersects(polygon_geom, zh_geom))):
                if DB.session.scalar(
                    select(func.ST_GeometryType(func.ST_Intersection(zh_geom, polygon_geom, 0.1)))
                ) not in ["ST_LineString", "ST_MultiLineString"]:
                    is_intersected = True
            if DB.session.scalar(
                select(
                    func.ST_Contains(
                        zh_geom,
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
                        zh_geom,
                    )
                )
            ):
                raise BadRequest("La ZH englobe complètement une ZH existante")
                # TODO: not detected if contained entirely in 2 or more ZH polygons

            polygon = DB.session.scalar(select(func.ST_Difference(polygon_geom, zh_geom)))

    return {"polygon": polygon, "is_intersected": is_intersected}


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


def get_main_rb(query: list) -> int:
    rb_id = None
    area = 0
    for q_ in query:
        zh_polygon = DB.session.execute(
            select(TZH.geom).where(TZH.id_zh == getattr(q_, "id_zh"))
        ).scalar_one()

        rb_polygon = DB.session.execute(
            select(TRiverBasin.geom)
            .select_from(CorZhRb)
            .join(TRiverBasin, TRiverBasin.id_rb == CorZhRb.id_rb)
            .where(TRiverBasin.id_rb == getattr(q_, "id_rb"))
            .limit(1)
        ).scalar_one()

        intersection = DB.session.scalar(
            select(
                func.ST_Intersection(
                    func.ST_GeomFromText(func.ST_AsText(zh_polygon)),
                    func.ST_GeomFromText(func.ST_AsText(rb_polygon)),
                )
            )
        )
        if DB.session.scalar(select(func.ST_Area(intersection, False))) > area:
            area = DB.session.scalar(select(func.ST_Area(intersection, False)))
            rb_id = getattr(q_, "id_rb")
    return rb_id
