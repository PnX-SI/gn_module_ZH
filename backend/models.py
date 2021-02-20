from flask import current_app
from sqlalchemy import ForeignKey
# import utiles pour déclarer les classes SQLAlchemy
from sqlalchemy.sql import select, func, and_
from sqlalchemy.dialects.postgresql import UUID

from geoalchemy2 import Geometry

from pypnusershub.db.models import User

# méthode de sérialisation
from utils_flask_sqla.serializers import serializable
from utils_flask_sqla_geo.serializers import geoserializable

# instance de la BDD
from geonature.utils.env import DB

from pdb import set_trace as debug
from sqlalchemy.inspection import inspect


# ajoute la méthode as_dict() à la classe
@serializable
# ajoute la méthode as_geofeature() générant un geojson à la classe
@geoserializable
class TZH(DB.Model):
    __tablename__ = "t_zh"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(DB.Integer, primary_key=True)
    zh_uuid = DB.Column(
        UUID(as_uuid=True), default=select([func.uuid_generate_v4()])
    )
    code = DB.Column(DB.Unicode, nullable=False)
    main_name = DB.Column(DB.Unicode, nullable=False)
    secondary_name = DB.Column(DB.Unicode)
    id_site_space = DB.Column(DB.Integer)
    create_author = DB.Column(DB.Integer, nullable=False)
    update_author = DB.Column(DB.Integer, nullable=False)
    create_date = DB.Column(DB.DateTime)
    update_date = DB.Column(DB.DateTime)
    geom = DB.Column(
        Geometry("GEOMETRY", 4326))
    remark_lim = DB.Column(DB.Unicode)
    remark_lim_fs = DB.Column(DB.Unicode)
    id_sdage = DB.Column(DB.Integer)
    id_local_typo = DB.Column(DB.Integer)
    remark_pres = DB.Column(DB.Unicode)
    v_habref = DB.Column(DB.Unicode)
    ef_area = DB.Column(DB.Integer)
    global_remark_activity = DB.Column(DB.Unicode)
    id_thread = DB.Column(DB.Integer)
    id_frequency = DB.Column(DB.Integer)
    id_spread = DB.Column(DB.Integer)
    id_connexion = DB.Column(DB.Integer)
    id_diag_hydro = DB.Column(DB.Integer)
    id_diag_bio = DB.Column(DB.Integer)
    remark_diag = DB.Column(DB.Unicode)
    other_inventory = DB.Column(DB.Boolean)
    carto_hab = DB.Column(DB.Boolean)
    nb_hab = DB.Column(DB.Integer)
    total_hab_cover = DB.Column(DB.Integer)
    nb_flora_sp = DB.Column(DB.Integer)
    nb_vertebrate_sp = DB.Column(DB.Integer)
    nb_invertebrate_sp = DB.Column(DB.Integer)
    remark_eval_functions = DB.Column(DB.Unicode)
    remark_eval_heritage = DB.Column(DB.Unicode)
    remark_eval_thread = DB.Column(DB.Unicode)
    reamrk_eval_actions = DB.Column(DB.Unicode)

    authors = DB.relationship(
        User,
        lazy="joined",
        #secondary=corRoleRelevesOccurrence.__table__,
        primaryjoin=(User.id_role == create_author),
        #secondaryjoin=(corRoleRelevesOccurrence.id_role == User.id_role),
        #cascade="all, delete-orphan",
        foreign_keys=[User.id_role]
    )

    def get_geofeature(self, recursif=True, relationships=()):
        return self.as_geofeature("geom", "id_zh", recursif, relationships=relationships)

