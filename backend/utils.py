import os

from geonature.utils.env import ROOT_DIR, DB
from geonature.core.gn_commons.models import TMedias


def get_file_path(id_media):
    media_path = get_media_path(id_media)
    return ROOT_DIR / media_path


def get_media_path(id_media):
    return DB.session.query(TMedias).filter(TMedias.id_media == id_media).one().media_path


def delete_file(id_media):
    try:
        os.remove(get_file_path(id_media))
    except:
        pass
    DB.session.query(TMedias).filter(TMedias.id_media == id_media).delete()
    DB.session.commit()
