import os
import pdb
import sys

from sqlalchemy.orm import Query

from geonature.utils.env import ROOT_DIR, DB
from geonature.core.gn_commons.models import TMedias
from pypnnomenclature.models import (
    TNomenclatures
)

from .api_error import ZHApiError

from .model.zh_schema import BibAreasTypes, LAreas, TZH


def get_main_picture_id(id_zh):
    return DB.session.query(TZH).filter(TZH.id_zh == id_zh).one().main_pict_id


def get_last_pdf_export(id_zh, last_date) -> Query:
    """
    Get all the pdf more recent than last_date

    last_date(datetime.date): date
    """
    # TODO: Add with entities ?
    # Need to have do a separate query instead of reusing get_medias...
    query = DB.session.query(TZH, TMedias, TNomenclatures).with_entities(TMedias.id_media).filter(TZH.id_zh == id_zh).filter(TZH.zh_uuid == TMedias.unique_id_media).filter(TMedias.id_nomenclature_media_type == TNomenclatures.id_nomenclature).filter(TNomenclatures.mnemonique == 'PDF').filter(TMedias.meta_update_date > last_date).filter(TMedias.title_fr.like(f'{id_zh}_fiche%.pdf'))
    return query.first()


def get_file_path(id_media):
    try:
        media_path = get_media_path(id_media)
        return ROOT_DIR / media_path
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_file_path_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def get_media_path(id_media):
    try:
        return DB.session.query(TMedias).filter(TMedias.id_media == id_media).one().media_path
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_media_path_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def delete_file(id_media):
    try:
        try:
            os.remove(get_file_path(id_media))
        except:
            pass
        DB.session.query(TMedias).filter(TMedias.id_media == id_media).delete()
        DB.session.commit()
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="delete_file_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def check_ref_geo_schema():
    try:
        id_type_com = DB.session.query(BibAreasTypes).filter(
            BibAreasTypes.type_code == 'COM').one().id_type
        id_type_dep = DB.session.query(BibAreasTypes).filter(
            BibAreasTypes.type_code == 'DEP').one().id_type
        n_com = DB.session.query(LAreas).filter(
            LAreas.id_type == id_type_com).count()
        n_dep = DB.session.query(LAreas).filter(
            LAreas.id_type == id_type_dep).count()
        if n_com == 0 or n_dep == 0:
            return False
        return True
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="check_ref_geo_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def get_extension(file_name):
    split_filename = file_name.split('.')
    return '.' + split_filename[len(split_filename)-1]
