import os
import sys

from geonature.core.gn_commons.models import TMedias
from geonature.core.gn_permissions.tools import get_scopes_by_action

from geonature.utils.env import DB, ROOT_DIR
from pypnnomenclature.models import TNomenclatures
from sqlalchemy.orm import Query
from sqlalchemy.sql import select, update, delete, func

from .api_error import ZHApiError
from .model.zh_schema import TZH, BibAreasTypes, LAreas


def get_main_picture_id(id_zh, media_list=None):
    """
    Args:
        media_list(list): media_list of the zh to set the main_pict_id if not
        present
    """
    main_pict_id = (
        DB.session.execute(select(TZH).where(TZH.id_zh == id_zh)).scalar_one().main_pict_id
    )
    if main_pict_id is None and media_list is not None and len(media_list) > 0:
        id_media = media_list[0].id_media
        stmt = update(TZH).where(TZH.id_zh == id_zh).values(main_pict_id=id_media)
        DB.session.execute(stmt)
        DB.session.commit()
    return main_pict_id


def get_last_pdf_export(id_zh, last_date) -> Query:
    """
    Get all the pdf more recent than last_date

    last_date(datetime.date): date
    """
    # TODO: Add with entities ?
    # Need to have do a separate query instead of reusing get_medias...
    query = (
        select(TZH, TMedias, TNomenclatures)
        .with_only_columns(TMedias.id_media)
        .where(TZH.id_zh == id_zh)
        .where(TZH.zh_uuid == TMedias.unique_id_media)
        .where(TMedias.id_nomenclature_media_type == TNomenclatures.id_nomenclature)
        .where(TNomenclatures.mnemonique == "PDF")
        .where(TMedias.meta_update_date > last_date)
        .where(TMedias.title_fr.like(f"{id_zh}_fiche%.pdf"))
    )
    return DB.session.execute(query).first()


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
        return DB.session.get(TMedias, id_media).media_path
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
        stmt = delete(TMedias).where(TMedias.id_media == id_media)
        DB.session.execute(stmt)
        DB.session.commit()
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="delete_file_error", details=str(exc_type) + ": " + str(e.with_traceback(tb))
        )


def check_ref_geo_schema():
    try:
        id_type_com = (
            DB.session.execute(select(BibAreasTypes).where(BibAreasTypes.type_code == "COM"))
            .scalar_one()
            .id_type
        )
        id_type_dep = (
            DB.session.execute(select(BibAreasTypes).where(BibAreasTypes.type_code == "DEP"))
            .scalar_one()
            .id_type
        )
        n_com = DB.session.scalar(select(func.count()).where(LAreas.id_type == id_type_com))
        n_dep = DB.session.scalar(select(func.count()).where(LAreas.id_type == id_type_dep))
        if n_com == 0 or n_dep == 0:
            return False
        return True
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="check_ref_geo_error", details=str(exc_type) + ": " + str(e.with_traceback(tb))
        )


def get_user_cruved():
    user_cruved = get_scopes_by_action(module_code="ZONES_HUMIDES")
    return user_cruved


def get_extension(file_name):
    split_filename = file_name.split(".")
    return "." + split_filename[len(split_filename) - 1]
