import os
import pdb
import sys

from geonature.core.gn_commons.models import TMedias
from geonature.core.gn_permissions.tools import get_or_fetch_user_cruved
from geonature.utils.env import DB, ROOT_DIR
from pypnnomenclature.models import TNomenclatures
from sqlalchemy.orm import Query

from .api_error import ZHApiError
from .model.zh_schema import TZH, BibAreasTypes, LAreas


def get_main_picture_id(id_zh, media_list: None):
    """
    Args:
        media_list(list): media_list of the zh to set the main_pict_id if not
        present
    """
    main_pict_id = DB.session.query(TZH).filter(TZH.id_zh == id_zh).one().main_pict_id
    if main_pict_id is None and media_list is not None and len(media_list) > 0:
        id_media = media_list[0].id_media
        DB.session.query(TZH).update({TZH.main_pict_id: id_media})
        DB.session.commit()
        main_pict_id = id_media
    return main_pict_id


def get_last_pdf_export(id_zh, last_date) -> Query:
    """
    Get all the pdf more recent than last_date

    last_date(datetime.date): date
    """
    # TODO: Add with entities ?
    # Need to have do a separate query instead of reusing get_medias...
    query = (
        DB.session.query(TZH, TMedias, TNomenclatures)
        .with_entities(TMedias.id_media)
        .filter(TZH.id_zh == id_zh)
        .filter(TZH.zh_uuid == TMedias.unique_id_media)
        .filter(TMedias.id_nomenclature_media_type == TNomenclatures.id_nomenclature)
        .filter(TNomenclatures.mnemonique == "PDF")
        .filter(TMedias.meta_update_date > last_date)
        .filter(TMedias.title_fr.like(f"{id_zh}_fiche%.pdf"))
    )
    return query.first()


def get_file_path(id_media):
    try:
        media_path = get_media_path(id_media)
        return ROOT_DIR / media_path
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_file_path_error", details=str(exc_type) + ": " + str(e.with_traceback(tb))
        )


def get_media_path(id_media):
    try:
        return DB.session.query(TMedias).filter(TMedias.id_media == id_media).one().media_path
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="get_media_path_error",
            details=str(exc_type) + ": " + str(e.with_traceback(tb)),
        )


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
            message="delete_file_error", details=str(exc_type) + ": " + str(e.with_traceback(tb))
        )


def check_ref_geo_schema():
    try:
        id_type_com = (
            DB.session.query(BibAreasTypes).filter(BibAreasTypes.type_code == "COM").one().id_type
        )
        id_type_dep = (
            DB.session.query(BibAreasTypes).filter(BibAreasTypes.type_code == "DEP").one().id_type
        )
        n_com = DB.session.query(LAreas).filter(LAreas.id_type == id_type_com).count()
        n_dep = DB.session.query(LAreas).filter(LAreas.id_type == id_type_dep).count()
        if n_com == 0 or n_dep == 0:
            return False
        return True
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="check_ref_geo_error", details=str(exc_type) + ": " + str(e.with_traceback(tb))
        )


def get_user_cruved(info_role, session):
    user = info_role
    user_cruved = get_or_fetch_user_cruved(
        session=session, id_role=info_role.id_role, module_code="ZONES_HUMIDES"
    )
    return (user, user_cruved)


def get_extension(file_name):
    split_filename = file_name.split(".")
    return "." + split_filename[len(split_filename) - 1]
