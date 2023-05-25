from geonature.utils.env import DB
from werkzeug.exceptions import NotFound


class ZhRepository:
    """
    Repository: classe permettant l'acces au données
    d'un modèle de type 'zh'
    """

    def __init__(self, model):
        self.model = model

    def delete(self, id_zh, user, user_cruved):
        """Delete a zh
        params:
         - id_zh: integer
         - info_user: TRole object model"""
        level = user_cruved["D"]
        zh = DB.session.query(self.model).get(id_zh)
        if zh:
            zh = zh.get_zh_if_allowed(user, "D", level)
            DB.session.delete(zh)
            DB.session.commit()
            return zh
        raise NotFound('The zh "{}" does not exist'.format(id_zh))
