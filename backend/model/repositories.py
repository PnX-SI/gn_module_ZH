from sqlalchemy import or_
from werkzeug.exceptions import NotFound
from sqlalchemy.sql import func, and_
from sqlalchemy.orm.exc import NoResultFound

from pypnnomenclature.models import TNomenclatures
from utils_flask_sqla.generic import testDataType

from geonature.utils.env import DB
from geonature.core.gn_commons.models import VLatestValidations
from geonature.utils.errors import GeonatureApiError

from .zh_schema import (
    TZH
)
from geonature.core.gn_meta.models import TDatasets, CorDatasetActor
from pypnusershub.db.models import User

import pdb


class ZhRepository:
    """
    Repository: classe permettant l'acces au données
    d'un modèle de type 'zh'
    """

    def __init__(self, model):
        self.model = model

    def delete(self, id_zh, info_user):
        """Delete a zh
        params:
         - id_zh: integer
         - info_user: TRole object model"""

        zh = DB.session.query(self.model).get(id_zh)
        if zh:
            zh = zh.get_zh_if_allowed(info_user)
            DB.session.delete(zh)
            DB.session.commit()
            return zh
        raise NotFound('The zh "{}" does not exist'.format(id_zh))
