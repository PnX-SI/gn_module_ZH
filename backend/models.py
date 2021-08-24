from flask import current_app
from sqlalchemy import ForeignKey
# import utiles pour déclarer les classes SQLAlchemy
from sqlalchemy.sql import select, func, and_, cast
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from pypnnomenclature.models import (
    TNomenclatures
)

from pypn_habref_api.models import (
    Habref,
    CorespHab
)

import geoalchemy2
from geoalchemy2.types import Geography, Geometry
from geoalchemy2.shape import to_shape

from pypnusershub.db.models import User
from pypnusershub.db.tools import InsufficientRightsError

# méthode de sérialisation
from utils_flask_sqla.serializers import serializable
from utils_flask_sqla_geo.serializers import geoserializable

# instance de la BDD
from geonature.utils.env import DB

from geonature.core.ref_geo.models import (
    LAreas,
    BibAreasTypes,
    LiMunicipalities
)

import pdb
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

    def user_is_observer_or_digitiser(self, user):
        observers = [d.id_role for d in self.observers]
        return user.id_role == self.id_digitiser or user.id_role in observers


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

    def get_bib_site_spaces():
        bib_site_spaces = DB.session.query(BibSiteSpace).all()
        bib_site_spaces_list = [
            bib_site_space.as_dict() for bib_site_space in bib_site_spaces
        ]
        return bib_site_spaces_list


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

    def get_abbrevation(id_org):
        org = DB.session.query(BibOrganismes).filter(
            BibOrganismes.id_org == id_org).one()
        return org.abbrevation

    def get_bib_organisms(org_type):
        bib_organismes = DB.session.query(BibOrganismes).all()
        if org_type == "operator":
            is_op_org = True
        elif org_type == "management_structure":
            is_op_org = False
        else:
            return "error in org type", 500
        bib_organismes_list = [
            bib_org.as_dict() for bib_org in bib_organismes if bib_org.is_op_org == is_op_org
        ]
        return bib_organismes_list


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
    id_org = DB.Column(
        DB.Integer,
        ForeignKey(BibOrganismes.id_org))
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


@serializable
class CorZhArea(DB.Model):
    __tablename__ = "cor_zh_area"
    __table_args__ = {"schema": "pr_zh"}
    id_area = DB.Column(
        DB.Integer,
        ForeignKey(LAreas.id_area),
        primary_key=True
    )
    id_zh = DB.Column(
        DB.Integer,
        primary_key=True
    )
    cover = DB.Column(DB.Integer)

    def get_id_type(mnemo):
        return DB.session.query(BibAreasTypes).filter(BibAreasTypes.type_name == mnemo).one().id_type

    def get_departments(id_zh):
        return DB.session.query(CorZhArea, LAreas, TZH).join(LAreas).filter(
            CorZhArea.id_zh == id_zh, LAreas.id_type == CorZhArea.get_id_type("Départements"), TZH.id_zh == id_zh).all()

    def get_municipalities_info(id_zh):
        return DB.session.query(CorZhArea, LAreas, TZH).join(LAreas).filter(
            CorZhArea.id_zh == id_zh, LAreas.id_type == CorZhArea.get_id_type("Communes"), TZH.id_zh == id_zh).all()


@serializable
@geoserializable
class ZH(TZH):
    __abstract__ = True

    def __init__(self, id_zh):
        self.zh = DB.session.query(TZH).filter(
            TZH.id_zh == id_zh).one()
        self.id_lims = self.get_id_lims()
        self.id_lims_fs = self.get_id_lims_fs()
        self.id_references = self.get_id_references()
        self.cb_codes_corine_biotope = self.get_cb_codes()
        self.id_corine_landcovers = self.get_corine_landcovers()
        self.activities = self.get_activities()
        self.flows = self.get_flows()
        self.fonctions_hydro = self.get_functions('FONCTIONS_HYDRO')
        self.fonctions_bio = self.get_functions('FONCTIONS_BIO')
        self.interet_patrim = self.get_functions('INTERET_PATRIM')
        self.val_soc_eco = self.get_functions('VAL_SOC_ECO')
        self.hab_heritages = self.get_hab_heritages()
        self.actions = self.get_actions()
        self.eval_fonctions_hydro = self.get_functions(
            'FONCTIONS_HYDRO', is_eval=True)
        self.eval_fonctions_bio = self.get_functions(
            'FONCTIONS_BIO', is_eval=True)
        self.eval_interet_patrim = self.get_functions(
            'INTERET_PATRIM', is_eval=True)
        self.eval_val_soc_eco = self.get_functions('VAL_SOC_ECO', is_eval=True)

    def get_id_lims(self):
        lim_list = CorLimList.get_lims_by_id(self.zh.id_lim_list)
        return {
            "id_lims": [id.id_lim for id in lim_list]
        }

    def get_id_lims_fs(self):
        lim_fs_list = CorZhLimFs.get_lim_fs_by_id(self.zh.id_zh)
        return {
            "id_lims_fs": [id.id_lim_fs for id in lim_fs_list]
        }

    def get_id_references(self):
        ref_list = CorZhRef.get_references_by_id(self.zh.id_zh)
        return {
            "id_references": [ref.as_dict() for ref in ref_list]
        }

    def get_cb_codes(self):
        corine_biotopes = CorZhCb.get_cb_by_id(self.zh.id_zh)
        return {
            "cb_codes_corine_biotope": [cb_code.lb_code for cb_code in corine_biotopes]
        }

    def get_corine_landcovers(self):
        landcovers = CorZhCorineCover.get_landcovers_by_id(self.zh.id_zh)
        return {
            "id_corine_landcovers": [landcover.id_cover for landcover in landcovers]
        }

    def get_activities(self):
        q_activities = TActivity.get_activites_by_id(self.zh.id_zh)
        activities = []
        for activity in q_activities:
            activities.append({
                'id_human_activity': activity.id_activity,
                'id_localisation': activity.id_position,
                'ids_impact': [impact.id_cor_impact_types for impact in CorImpactList.get_impacts_by_uuid(activity.id_impact_list)],
                'remark_activity': activity.remark_activity
            })
        return {
            "activities": activities
        }

    def get_flows(self):
        q_outflows = TOutflow.get_outflows_by_id(self.zh.id_zh)
        q_inflows = TInflow.get_inflows_by_id(self.zh.id_zh)
        flows = []
        outflows = []
        inflows = []
        for flow in q_outflows:
            outflows.append({
                "id_outflow": flow.id_outflow,
                "id_permanance": flow.id_permanance,
                "topo": flow.topo
            })
        flows.append({
            "outflows": outflows
        })
        for flow in q_inflows:
            inflows.append({
                "id_inflow": flow.id_inflow,
                "id_permanance": flow.id_permanance,
                "topo": flow.topo
            })
        flows.append({
            "inflows": inflows
        })
        return {
            "flows": flows
        }

    def get_functions(self, category, is_eval=False):
        q_functions = TFunctions.get_functions_by_id_and_category(
            self.zh.id_zh, category, is_eval)
        functions = []
        for function in q_functions:
            functions.append({
                'id_function': function.id_function,
                'justification': function.justification,
                'id_qualification': function.id_qualification,
                'id_knowledge': function.id_knowledge
            })
        return {
            category.lower(): functions
        }

    def get_hab_heritages(self):
        q_hab_heritages = THabHeritage.get_hab_heritage_by_id(self.zh.id_zh)
        hab_heritages = []
        for hab_heritage in q_hab_heritages:
            hab_heritages.append({
                'id_corine_bio': hab_heritage.id_corine_bio,
                'id_cahier_hab': hab_heritage.id_cahier_hab,
                'id_preservation_state': hab_heritage.id_preservation_state,
                'hab_cover': hab_heritage.hab_cover
            })
        return {
            "hab_heritages": hab_heritages
        }

    def get_actions(self):
        q_actions = TActions.get_actions_by_id(self.zh.id_zh)
        actions = []
        for action in q_actions:
            actions.append({
                'id_action': action.id_action,
                'id_priority_level': action.id_priority_level,
                'remark': action.remark
            })
        return {
            "actions": actions
        }

    def get_fauna_nb(self):
        try:
            vertebrates = int(self.zh.as_dict()['nb_vertebrate_sp'])
        except TypeError:
            vertebrates = 0
        try:
            invertebrates = int(self.zh.as_dict()['nb_invertebrate_sp'])
        except TypeError:
            invertebrates = 0
        return vertebrates+invertebrates

    def get_full_zh(self):
        full_zh = self.zh.get_geofeature()
        full_zh.properties.update(self.id_lims)
        full_zh.properties.update(self.id_lims_fs)
        full_zh.properties.update(self.id_references)
        full_zh.properties.update(self.cb_codes_corine_biotope)
        full_zh.properties.update(self.id_corine_landcovers)
        full_zh.properties.update(self.activities)
        full_zh.properties.update(self.flows)
        full_zh.properties.update(self.fonctions_hydro)
        full_zh.properties.update(self.fonctions_bio)
        full_zh.properties.update(self.interet_patrim)
        full_zh.properties.update(self.val_soc_eco)
        full_zh.properties.update(self.hab_heritages)
        full_zh.properties.update(self.actions)
        return full_zh

    def get_eval(self):
        eval = {}
        eval.update(self.eval_fonctions_hydro)
        eval.update(self.eval_fonctions_bio)
        eval.update(self.eval_interet_patrim)
        eval.update(self.eval_val_soc_eco)
        eval.update({
            "nb_flora_sp": self.zh.as_dict()['nb_flora_sp'],
            "nb_hab": self.zh.as_dict()['nb_flora_sp'],
            "nb_fauna_sp": self.get_fauna_nb(),
            "total_hab_cover": self.zh.as_dict()['nb_flora_sp'],
            "id_thread": self.zh.as_dict()['id_thread'],
            "id_diag_hydro": self.zh.as_dict()['id_diag_hydro'],
            "id_diag_bio": self.zh.as_dict()['id_diag_bio']
        })
        return eval


class Code(ZH):
    def __init__(self, id_zh, id_org, zh_geom):
        self.id_zh = id_zh
        self.id_org = id_org
        self.zh_geom = zh_geom
        self.dep = self.get_departments()
        self.organism = self.get_organism()
        self.number = self.get_number()
        self.is_valid_number = self.set_valid_number()

    def get_departments(self):
        departments = CorZhArea.get_departments(self.id_zh)
        area = 0
        my_geom = DB.session.query(func.ST_Transform(func.ST_SetSRID(
            TZH.geom, 4326), 2154)).filter(TZH.id_zh == self.id_zh).one()[0]
        for dep in departments:
            if DB.session.scalar(dep.LAreas.geom.ST_Intersection(my_geom).ST_Area()) > area:
                area = DB.session.scalar(
                    dep.LAreas.geom.ST_Intersection(my_geom).ST_Area())
                main_dep = dep.LAreas.area_code
        return main_dep

    def get_organism(self):
        return BibOrganismes.get_abbrevation(self.id_org)

    def get_number(self):
        number = DB.session.query(CorZhArea).join(LAreas, LAreas.id_area == CorZhArea.id_area).join(
            TZH, TZH.id_zh == CorZhArea.id_zh).filter(TZH.id_org == self.id_org, LAreas.area_code == self.get_departments()).count()
        return number+1

    def set_valid_number(self):
        if self.number > 9999:
            return False
        return True

    def __repr__(self):
        return f'{self.dep}-{self.organism}-{self.number}'


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

    def get_lims_by_id(id):
        return DB.session.query(CorLimList).filter(
            CorLimList.id_lim_list == id).all()


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
        primary_key=True,
        autoincrement=True
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

    def get_references_by_id(id_zh):
        return DB.session.query(TReferences).join(
            CorZhRef).filter(CorZhRef.id_zh == id_zh).all()


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

    def get_lim_fs_by_id(id_zh):
        return DB.session.query(CorZhLimFs).filter(
            CorZhLimFs.id_zh == id_zh).all()


class CorSdageSage(DB.Model):
    __tablename__ = "cor_sdage_sage"
    __table_args__ = {"schema": "pr_zh"}
    id_sdage = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )
    id_sage = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )

    def get_id_sdage_list():
        q_id_sdages = DB.session.query(
            func.distinct(CorSdageSage.id_sdage)).all()
        return [id[0] for id in q_id_sdages]

    def get_sage_by_id(id):
        return DB.session.query(CorSdageSage, TNomenclatures).join(TNomenclatures, TNomenclatures.id_nomenclature == CorSdageSage.id_sage).filter(CorSdageSage.id_sdage == id).all()


class BibCb(DB.Model):
    __tablename__ = "bib_cb"
    __table_args__ = {"schema": "pr_zh"}
    lb_code = DB.Column(
        DB.Unicode,
        primary_key=True
    )
    humidity = DB.Column(
        DB.Unicode,
        nullable=False
    )
    is_ch = DB.Column(
        DB.Boolean,
        nullable=False
    )

    def get_label():
        return DB.session.query(BibCb, Habref).join(
            Habref, BibCb.lb_code == Habref.lb_code).filter(Habref.cd_typo == 22).all()

    def get_ch(lb_code):
        # get cd_hab_sortie from lb_code of selected Corine Biotope
        cd_hab_sortie = DB.session.query(Habref).filter(
            and_(Habref.lb_code == lb_code, Habref.cd_typo == 22)).one().cd_hab
        # get all cd_hab_entre corresponding to cd_hab_sortie
        q_cd_hab_entre = DB.session.query(CorespHab).filter(
            CorespHab.cd_hab_sortie == cd_hab_sortie).all()
        # get list of cd_hab_entre/lb_code/lb_hab_fr for each cahier habitat
        ch = []
        for q in q_cd_hab_entre:
            ch.append({
                "cd_hab": q.cd_hab_entre,
                "lb_code": DB.session.query(Habref).filter(Habref.cd_hab == q.cd_hab_entre).one().lb_code,
                "lb_hab_fr": DB.session.query(Habref).filter(Habref.cd_hab == q.cd_hab_entre).one().lb_hab_fr
            })
        return ch


class CorImpactTypes(DB.Model):
    __tablename__ = "cor_impact_types"
    __table_args__ = {"schema": "pr_zh"}
    id_cor_impact_types = DB.Column(
        DB.Integer,
        primary_key=True
    )
    id_impact = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        nullable=False
    )
    id_impact_type = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature)
    )
    active = DB.Column(
        DB.Integer,
        nullable=False
    )

    def get_impacts():
        return DB.session.query(CorImpactTypes, TNomenclatures).join(
            TNomenclatures, TNomenclatures.id_nomenclature == CorImpactTypes.id_impact).filter(
                CorImpactTypes.active).all()

    #            and_(CorImpactTypes.id_impact_type == id_type, CorImpactTypes.active)).all()
    # def get_impact_type_list():
    #    q_id_types = DB.session.query(
    #        func.distinct(CorImpactTypes.id_impact_type)).all()
    #    return [id[0] for id in q_id_types]

    # def get_impact_by_type(id_type):
    #    return DB.session.query(CorImpactTypes, TNomenclatures).join(
    #        TNomenclatures, TNomenclatures.id_nomenclature == CorImpactTypes.id_impact).filter(
    #            and_(CorImpactTypes.id_impact_type == id_type, CorImpactTypes.active)).all()

    # def get_mnemo_type(id_type):
    #    if id_type:
    #        return DB.session.query(TNomenclatures).filter(
    #            TNomenclatures.id_nomenclature == id_type).one()
    #    else:
    #        return ''


class CorMainFct(DB.Model):
    __tablename__ = "cor_main_fct"
    __table_args__ = {"schema": "pr_zh"}
    id_function = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )
    id_main_function = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        nullable=False
    )
    active = DB.Column(
        DB.Integer,
        nullable=False
    )

    def get_main_function_list(ids):
        q_id_types = DB.session.query(
            func.distinct(CorMainFct.id_main_function)).all()
        return [id[0] for id in q_id_types if id[0] in ids]

    def get_function_by_main_function(id_main):
        return DB.session.query(CorMainFct, TNomenclatures).join(
            TNomenclatures, TNomenclatures.id_nomenclature == CorMainFct.id_function).filter(
                and_(CorMainFct.id_main_function == id_main, CorMainFct.active)).all()

    def get_mnemo_type(id_type):
        if id_type:
            return DB.session.query(TNomenclatures).filter(
                TNomenclatures.id_nomenclature == id_type).one()
        else:
            return ''


class CorZhCb(DB.Model):
    __tablename__ = "cor_zh_cb"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    lb_code = DB.Column(
        DB.Integer,
        ForeignKey(BibCb.lb_code),
        primary_key=True
    )

    def get_cb_by_id(id_zh):
        return DB.session.query(CorZhCb).filter(
            CorZhCb.id_zh == id_zh).all()


class CorZhCorineCover(DB.Model):
    __tablename__ = "cor_zh_corine_cover"
    __table_args__ = {"schema": "pr_zh"}
    id_cover = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )

    def get_landcovers_by_id(id_zh):
        return DB.session.query(CorZhCorineCover).filter(
            CorZhCorineCover.id_zh == id_zh).all()


class CorImpactList(DB.Model):
    __tablename__ = "cor_impact_list"
    __table_args__ = {"schema": "pr_zh"}
    id_impact_list = DB.Column(
        UUID(as_uuid=True),
        ForeignKey("pr_zh.t_activity.id_impact_list", ondelete='CASCADE'),
        primary_key=True
    )
    id_cor_impact_types = DB.Column(
        DB.Integer,
        ForeignKey(CorImpactTypes.id_cor_impact_types),
        primary_key=True
    )

    def get_impacts_by_uuid(uuid_activity):
        return DB.session.query(CorImpactList).filter(
            CorImpactList.id_impact_list == uuid_activity).all()


class TActivity(DB.Model):
    __tablename__ = "t_activity"
    __table_args__ = {"schema": "pr_zh"}
    id_activity = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    id_position = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        nullable=False
    )
    id_impact_list = DB.Column(
        UUID(as_uuid=True),
        nullable=False
    )
    remark_activity = DB.Column(
        DB.Unicode
    )
    child = relationship(CorImpactList, backref="parent", passive_deletes=True)

    def get_activites_by_id(id_zh):
        return DB.session.query(TActivity).filter(
            TActivity.id_zh == id_zh).all()


class TOutflow(DB.Model):
    __tablename__ = "t_outflow"
    __table_args__ = {"schema": "pr_zh"}
    id_outflow = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    id_permanance = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("PERMANENCE_SORTIE"),
    )
    topo = DB.Column(
        DB.Unicode
    )

    def get_outflows_by_id(id_zh):
        return DB.session.query(TOutflow).filter(
            TOutflow.id_zh == id_zh).all()


class TInflow(DB.Model):
    __tablename__ = "t_inflow"
    __table_args__ = {"schema": "pr_zh"}
    id_inflow = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    id_permanance = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("PERMANENCE_ENTREE"),
    )
    topo = DB.Column(
        DB.Unicode
    )

    def get_inflows_by_id(id_zh):
        return DB.session.query(TInflow).filter(
            TInflow.id_zh == id_zh).all()


class TFunctions(DB.Model):
    __tablename__ = "t_functions"
    __table_args__ = {"schema": "pr_zh"}
    id_function = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        primary_key=True
    )
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    justification = DB.Column(
        DB.Unicode(length=2000)
    )
    id_qualification = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("FONCTIONS_QUALIF"),
    )
    id_knowledge = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature(
            "FONCTIONS_CONNAISSANCE"),
    )

    def get_functions_by_id_and_category(id_zh, category, is_eval=False):
        eval_qualification = ['Moyenne', 'Forte']
        function_ids = [
            nomenclature.id_nomenclature for nomenclature in Nomenclatures.get_nomenclature_info(category)
        ]
        if is_eval:
            qualif_ids = [
                nomenclature.id_nomenclature for nomenclature in Nomenclatures.get_nomenclature_info('FONCTIONS_QUALIF') if nomenclature.mnemonique in eval_qualification
            ]
        else:
            qualif_ids = [
                nomenclature.id_nomenclature for nomenclature in Nomenclatures.get_nomenclature_info('FONCTIONS_QUALIF')
            ]

        return DB.session.query(TFunctions).filter(
            TFunctions.id_zh == id_zh).filter(
                TFunctions.id_function.in_(function_ids)).filter(
                    TFunctions.id_qualification.in_(qualif_ids)).all()


class THabHeritage(DB.Model):
    __tablename__ = "t_hab_heritage"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    id_corine_bio = DB.Column(
        DB.Unicode,
        ForeignKey(BibCb.lb_code),
        primary_key=True
    )
    id_cahier_hab = DB.Column(
        DB.Unicode,
        primary_key=True
    )
    id_preservation_state = DB.Column(
        DB.Unicode,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("ETAT_CONSERVATION")
    )
    hab_cover = DB.Column(
        DB.Unicode,
        nullable=False
    )

    def get_hab_heritage_by_id(id_zh):
        return DB.session.query(THabHeritage).filter(
            THabHeritage.id_zh == id_zh).all()


class CorUrbanTypeRange(DB.Model):
    __tablename__ = "cor_urban_type_range"
    __table_args__ = {"schema": "pr_zh"}
    id_cor = DB.Column(
        DB.Integer,
        primary_key=True
    )
    id_range_type = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature)
    )
    id_doc_type = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature)
    )

    def get_range_by_doc(doc_id):
        q_ranges = DB.session.query(CorUrbanTypeRange).filter(
            CorUrbanTypeRange.id_range_type == doc_id).all()
        ranges = []
        for range in q_ranges:
            ranges.append({
                "id_nomenclature": range.id_doc_type,
                "mnemonique": DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == range.id_doc_type).one().mnemonique
            })
        return ranges


class CorProtectionLevelType(DB.Model):
    __tablename__ = "cor_protection_level_type"
    __table_args__ = {"schema": "pr_zh"}
    id_protection = DB.Column(
        DB.Integer,
        primary_key=True
    )
    id_protection_status = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        nullable=False
    )
    id_protection_type = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature)
    )
    id_protection_level = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        nullable=False
    )

    def get_status_by_type(type_id):
        q_protection_types = DB.session.query(CorProtectionLevelType).filter(
            CorProtectionLevelType.id_protection_type == type_id).all()
        protection_status = []
        for protection in q_protection_types:
            protection_status.append({
                "id_protection_status": protection.id_protection_status,
                "mnemonique_status": DB.session.query(TNomenclatures).filter(
                    TNomenclatures.id_nomenclature == protection.id_protection_status).one().mnemonique,
                "id_protection_level": protection.id_protection_level,
                "mnemonique_level": DB.session.query(TNomenclatures).filter(
                    TNomenclatures.id_nomenclature == protection.id_protection_level).one().mnemonique

            })
        return protection_status


@serializable
class BibActions(DB.Model):
    __tablename__ = "bib_actions"
    __table_args__ = {"schema": "pr_zh"}
    id_action = DB.Column(
        DB.Integer,
        primary_key=True
    )
    name = DB.Column(
        DB.Unicode(length=100),
        nullable=False
    )

    def get_bib_actions():
        q_bib_actions = DB.session.query(BibActions).all()
        bib_actions_list = [
            bib_action.as_dict() for bib_action in q_bib_actions
        ]
        return bib_actions_list


@serializable
class TActions(DB.Model):
    __tablename__ = "t_actions"
    __table_args__ = {"schema": "pr_zh"}
    id_action = DB.Column(
        DB.Integer,
        ForeignKey(BibActions.id_action),
        primary_key=True
    )
    id_zh = DB.Column(
        DB.Integer,
        ForeignKey(TZH.id_zh),
        primary_key=True
    )
    id_priority_level = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature)
    )
    remark = DB.Column(
        DB.Unicode(length=2000)
    )

    def get_actions_by_id(id_zh):
        return DB.session.query(TActions).filter(
            TActions.id_zh == id_zh).all()
