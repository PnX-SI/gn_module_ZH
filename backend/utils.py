import os
import pdb
import sys

from geonature.utils.env import ROOT_DIR, DB
from geonature.core.gn_commons.models import TMedias

from .api_error import ZHApiError

from .model.zh_schema import BibAreasTypes, LAreas


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
