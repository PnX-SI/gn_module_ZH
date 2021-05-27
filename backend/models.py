from flask import current_app
from sqlalchemy import ForeignKey
# import utiles pour déclarer les classes SQLAlchemy
from sqlalchemy.sql import select, func, and_, cast
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from pypnnomenclature.models import (
    TNomenclatures
)

import geoalchemy2
from geoalchemy2.types import Geography, Geometry

from pypnusershub.db.models import User
from pypnusershub.db.tools import InsufficientRightsError

# méthode de sérialisation
from utils_flask_sqla.serializers import serializable
from utils_flask_sqla_geo.serializers import geoserializable

# instance de la BDD
from geonature.utils.env import DB

from pdb import set_trace as debug
from sqlalchemy.inspection import inspect


class ZhModel(DB.Model):
    """
        Classe abstraite permettant d'ajout des méthodes
        de controle d'accès à la donnée en fonction
        des droits associés à un utilisateur
    """

    __abstract__ = True

    def user_is_observer_or_digitiser(self, user):
        observers = [d.id_role for d in self.observers]
        return user.id_role == self.id_digitiser or user.id_role in observers

    def user_is_in_dataset_actor(self, user):
        only_user = user.value_filter == "1"
        return self.id_dataset in TDatasets.get_user_datasets(user, only_user=only_user)

    def user_is_allowed_to(self, user, level):
        """
            Fonction permettant de dire si un utilisateur
            peu ou non agir sur une donnée
        """
        # Si l'utilisateur n'a pas de droit d'accès aux données
        if level == "0" or level not in ("1", "2", "3"):
            return False

        # Si l'utilisateur à le droit d'accéder à toutes les données
        if level == "3":
            return True

        # Si l'utilisateur est propriétaire de la données
        if self.user_is_observer_or_digitiser(user):
            return True

        # Si l'utilisateur appartient à un organisme
        # qui a un droit sur la données et
        # que son niveau d'accès est 2 ou 3
        if self.user_is_in_dataset_actor(user) and level in ("2", "3"):
            return True
        return False

    def get_zh_if_allowed(self, user):
        """
            Return the zh if the user is allowed
            params:
                user: object from TRole
        """
        if self.user_is_allowed_to(user, user.value_filter):
            return self

        raise InsufficientRightsError(
            ('User "{}" cannot "{}" this current zh').format(
                user.id_role, user.code_action
            ),
            403,
        )

    def get_releve_cruved(self, user, user_cruved):
        """
        Return the user's cruved for a Releve instance.
        Use in the map-list interface to allow or not an action
        params:
            - user : a TRole object
            - user_cruved: object return by cruved_for_user_in_app(user)
        """
        return {
            action: self.user_is_allowed_to(user, level)
            for action, level in user_cruved.items()
        }


@serializable
class Nomenclatures(TNomenclatures):

    __abstract__ = True

    @staticmethod
    def get_nomenclature_info(bib_mnemo):
        q = TNomenclatures.query.filter_by(
            id_type=select(
                [func.ref_nomenclatures.get_id_nomenclature_type(bib_mnemo)])
        ).all()
        return q


@serializable
class BibSiteSpace(DB.Model):
    __tablename__ = "bib_site_space"
    __table_args__ = {"schema": "pr_zh"}
    id_site_space = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.Unicode)


@serializable
@geoserializable
class TZH(ZhModel):
    __tablename__ = "t_zh"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(
        DB.Integer,
        primary_key=True,
        autoincrement=True)
    zh_uuid = DB.Column(
        UUID(as_uuid=True),
        default=select([func.uuid_generate_v4()]))
    code = DB.Column(DB.Unicode, nullable=False)
    main_name = DB.Column(DB.Unicode, nullable=False)
    secondary_name = DB.Column(DB.Unicode)
    is_id_site_space = DB.Column(
        DB.Boolean,
        default=False)
    id_site_space = DB.Column(
        DB.Integer,
        ForeignKey(BibSiteSpace.id_site_space))
    create_author = DB.Column(
        DB.Integer,
        ForeignKey(User.id_role),
        nullable=False)
    update_author = DB.Column(
        DB.Integer,
        ForeignKey(User.id_role),
        nullable=False)
    create_date = DB.Column(DB.DateTime)
    update_date = DB.Column(DB.DateTime)
    geom = DB.Column(
        geoalchemy2.Geometry("GEOMETRY", 4326),
        nullable=False)
    id_lim_list = DB.Column(
        UUID(as_uuid=True),
        nullable=False)
    remark_lim = DB.Column(DB.Unicode)
    remark_lim_fs = DB.Column(DB.Unicode)
    id_sdage = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        nullable=False)
    id_sage = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature))
    remark_pres = DB.Column(DB.Unicode)
    v_habref = DB.Column(DB.Unicode)
    ef_area = DB.Column(DB.Integer)
    global_remark_activity = DB.Column(DB.Unicode)
    id_thread = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("EVAL_GLOB_MENACES"))
    id_frequency = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("SUBMERSION_FREQ"))
    id_spread = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("SUBMERSION_ETENDUE"))
    id_connexion = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature))
    id_diag_hydro = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("FONCTIONNALITE_HYDRO"))
    id_diag_bio = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("FONCTIONNALITE_BIO"))
    remark_diag = DB.Column(DB.Unicode)
    is_other_inventory = DB.Column(DB.Boolean, default=False)
    is_carto_hab = DB.Column(DB.Boolean, default=False)
    nb_hab = DB.Column(DB.Integer)
    total_hab_cover = DB.Column(
        DB.Integer,
        default=999,
        nullable=False)
    nb_flora_sp = DB.Column(DB.Integer)
    nb_vertebrate_sp = DB.Column(DB.Integer)
    nb_invertebrate_sp = DB.Column(DB.Integer)
    remark_eval_functions = DB.Column(DB.Unicode)
    remark_eval_heritage = DB.Column(DB.Unicode)
    remark_eval_thread = DB.Column(DB.Unicode)
    remark_eval_actions = DB.Column(DB.Unicode)

    authors = DB.relationship(
        User,
        lazy="joined",
        primaryjoin=(User.id_role == create_author)
    )

    def get_geofeature(self, recursif=True, relationships=()):
        return self.as_geofeature("geom", "id_zh", recursif, relationships=relationships)

    @staticmethod
    def get_zh_area_intersected(zh_area_type, id_zh_geom):
        if zh_area_type == 'river_basin':
            q = DB.session.query(TRiverBasin).filter(
                TRiverBasin.geom.ST_Intersects(cast(id_zh_geom, Geography))).all()
        if zh_area_type == 'hydro_area':
            q = DB.session.query(THydroArea).filter(
                THydroArea.geom.ST_Intersects(cast(id_zh_geom, Geography))).all()
        if zh_area_type == 'fct_area':
            q = DB.session.query(TFctArea).filter(
                TFctArea.geom.ST_Intersects(cast(id_zh_geom, Geography))).all()
        return q


class CorLimList(DB.Model):
    __tablename__ = "cor_lim_list"
    __table_args__ = {"schema": "pr_zh"}
    id_lim_list = DB.Column(
        UUID(as_uuid=True),
        primary_key=True
    )
    id_lim = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )


class CorZhArea(DB.Model):
    __tablename__ = "cor_zh_area"
    __table_args__ = {"schema": "pr_zh"}
    id_area = DB.Column(
        DB.Integer,
        ForeignKey("ref_geo.l_areas.id_area"),
        primary_key=True
    )
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    cover = DB.Column(DB.Integer)


class TRiverBasin(DB.Model):
    __tablename__ = "t_river_basin"
    __table_args__ = {"schema": "pr_zh"}
    id_rb = DB.Column(
        DB.Integer,
        primary_key=True
    )
    name = DB.Column(
        DB.Unicode,
        nullable=False
    )
    geom = DB.Column(
        geoalchemy2.Geometry("GEOMETRY", 4326),
        nullable=False
    )
    id_climate_class = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature)
    )
    id_river_flow = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature)
    )


class CorZhRb(DB.Model):
    __tablename__ = "cor_zh_rb"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    id_rb = DB.Column(
        DB.Integer,
        ForeignKey(TRiverBasin.id_rb),
        primary_key=True
    )


class THydroArea(DB.Model):
    __tablename__ = "t_hydro_area"
    __table_args__ = {"schema": "pr_zh"}
    id_hydro = DB.Column(
        DB.Integer,
        primary_key=True
    )
    name = DB.Column(
        DB.Unicode,
        nullable=False
    )
    geom = DB.Column(
        geoalchemy2.Geometry("GEOMETRY", 4326),
        nullable=False
    )


class CorZhHydro(DB.Model):
    __tablename__ = "cor_zh_hydro"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    id_hydro = DB.Column(
        DB.Integer,
        ForeignKey(THydroArea.id_hydro),
        primary_key=True
    )


class TFctArea(DB.Model):
    __tablename__ = "t_fct_area"
    __table_args__ = {"schema": "pr_zh"}
    id_fct_area = DB.Column(
        DB.Integer,
        primary_key=True
    )
    geom = DB.Column(
        geoalchemy2.Geometry("GEOMETRY", 4326),
        nullable=False
    )


class CorZhFctArea(DB.Model):
    __tablename__ = "cor_zh_fct_area"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    id_fct_area = DB.Column(
        DB.Integer,
        ForeignKey(TFctArea.id_fct_area),
        primary_key=True
    )


@serializable
class TReferences(DB.Model):
    __tablename__ = "t_references"
    __table_args__ = {"schema": "pr_zh"}
    id_reference = DB.Column(
        DB.Integer,
        primary_key=True
    )
    authors = DB.Column(DB.Unicode)
    pub_year = DB.Column(DB.Integer)
    title = DB.Column(
        DB.Unicode,
        nullable=False
    )
    editor = DB.Column(DB.Unicode)
    editor_location = DB.Column(DB.Unicode)


class CorZhRef(DB.Model):
    __tablename__ = "cor_zh_ref"
    __table_args__ = {"schema": "pr_zh"}
    id_ref = DB.Column(
        DB.Integer,
        ForeignKey(TReferences.id_reference),
        primary_key=True
    )
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )


class CorZhLimFs(DB.Model):
    __tablename__ = "cor_zh_lim_fs"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    id_lim_fs = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )


@serializable
class BibOrganismes(DB.Model):
    __tablename__ = "bib_organismes"
    __table_args__ = {"schema": "pr_zh"}
    id_org = DB.Column(
        DB.Integer,
        primary_key=True
    )
    name = DB.Column(
        DB.Unicode(length=6),
        nullable=False
    )
    abbrevation = DB.Column(
        DB.Unicode,
        nullable=False
    )
    is_op_org = DB.Column(
        DB.Boolean,
        default=False,
        nullable=False
    )
