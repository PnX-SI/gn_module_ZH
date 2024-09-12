import geoalchemy2
from flask import Blueprint
from geoalchemy2.types import Geography
from ref_geo.models import BibAreasTypes, LAreas, LiMunicipalities
from geonature.utils.env import DB
from pypn_habref_api.models import CorespHab, Habref
from pypnnomenclature.models import BibNomenclaturesTypes, TNomenclatures
from pypnusershub.db.models import User
from pypnusershub.db.tools import InsufficientRightsError
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.sql import and_, cast, func, select

# méthode de sérialisation
from utils_flask_sqla.serializers import serializable
from utils_flask_sqla_geo.serializers import geoserializable

blueprint = Blueprint("pr_zh", __name__)


class ZhModel(DB.Model):
    """
    Classe abstraite permettant d'ajout des méthodes
    de controle d'accès à la donnée en fonction
    des droits associés à un utilisateur
    """

    __abstract__ = True

    def user_is_owner(self, user):
        return user.id_role == self.create_author

    def user_is_in_dataset_actor(self, user):
        return user.id_organisme == self.authors.id_organisme

    def user_is_allowed_to(self, user, level):
        """
        Fonction permettant de dire si un utilisateur
        peu ou non agir sur une donnée
        """
        # Si l'utilisateur n'a pas de droit d'accès aux données
        if level == 0 or level not in (1, 2, 3):
            return False

        # Si l'utilisateur à le droit d'accéder à toutes les données
        if level == 3:
            return True

        # Si l'utilisateur est propriétaire de la données
        if self.user_is_owner(user):
            return True

        # Si l'utilisateur appartient à un organisme
        # qui a un droit sur la données et
        # que son niveau d'accès est 2 ou 3
        if self.user_is_in_dataset_actor(user) and level in (2, 3):
            return True
        return False

    def get_zh_if_allowed(self, user, action, level):
        """
        Return the zh if the user is allowed
        params:
            user: object from TRole
        """
        if self.user_is_allowed_to(user, level):
            return self

        raise InsufficientRightsError(
            ('User "{}" cannot "{}" this current zh').format(user.id_role),
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
            action: self.user_is_allowed_to(user, level) for action, level in user_cruved.items()
        }


class Nomenclatures(TNomenclatures):
    __abstract__ = True

    @staticmethod
    def get_nomenclature_info(bib_mnemo):
        # todo
        q = select(TNomenclatures).where(
            TNomenclatures.id_type == (func.ref_nomenclatures.get_id_nomenclature_type(bib_mnemo))
        )
        if bib_mnemo == "SDAGE":
            q = q.order_by(TNomenclatures.id_nomenclature)
        return DB.session.scalars(q).all()


@serializable
class DefaultsNomenclaturesValues(DB.Model):
    __tablename__ = "defaults_nomenclatures_value"
    __table_args__ = {"schema": "ref_nomenclatures"}
    mnemonique_type = DB.Column(
        DB.Unicode(length=255),
        ForeignKey(BibNomenclaturesTypes.mnemonique),
        primary_key=True,
    )
    id_organism = DB.Column(
        DB.Integer,
        ForeignKey("utilisateurs.bib_organismes.id_organisme"),
        primary_key=True,
    )
    id_nomenclature = DB.Column(
        DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), nullable=False
    )


@serializable
class BibSiteSpace(DB.Model):
    __tablename__ = "bib_site_space"
    __table_args__ = {"schema": "pr_zh"}
    id_site_space = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.Unicode)

    @staticmethod
    def get_bib_site_spaces():
        # bib_site_spaces = DB.session.execute(select(BibSiteSpace)).scalars().all()
        bib_site_spaces = DB.session.scalars(select(BibSiteSpace)).all()
        bib_site_spaces_list = [bib_site_space.as_dict() for bib_site_space in bib_site_spaces]
        return bib_site_spaces_list


@serializable
class BibOrganismes(DB.Model):
    __tablename__ = "bib_organismes"
    __table_args__ = {"schema": "pr_zh"}
    id_org = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.Unicode(length=6), nullable=False)
    abbrevation = DB.Column(DB.Unicode, nullable=False)
    is_op_org = DB.Column(DB.Boolean, default=False, nullable=False)

    @staticmethod
    def get_abbrevation(id_org):
        org = DB.session.execute(
            select(BibOrganismes).where(BibOrganismes.id_org == id_org)
        ).scalar_one()
        return org.abbrevation

    @staticmethod
    def get_bib_organisms(org_type):
        # bib_organismes = DB.session.execute(select(BibOrganismes)).scalars().all()
        bib_organismes = DB.session.scalars(select(BibOrganismes)).all()
        if org_type == "operator":
            return [bib_org.as_dict() for bib_org in bib_organismes if bib_org.is_op_org]
        elif org_type == "management_structure":
            return [bib_org.as_dict() for bib_org in bib_organismes]
        else:
            return "error in org type", 500


@serializable
class CorLimList(DB.Model):
    __tablename__ = "cor_lim_list"
    __table_args__ = {"schema": "pr_zh"}
    id_lim_list = DB.Column(UUID(as_uuid=True), primary_key=True)
    id_lim = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True)

    def get_lims_by_id(id):
        return DB.session.scalars(select(CorLimList).where(CorLimList.id_lim_list == id)).all()


@serializable
@geoserializable
class TZH(ZhModel):
    __tablename__ = "t_zh"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    zh_uuid = DB.Column(UUID(as_uuid=True), default=select([func.uuid_generate_v4()]))
    code = DB.Column(DB.Unicode, nullable=False)
    main_name = DB.Column(DB.Unicode, nullable=False)
    fullname = column_property(main_name + " " + code)
    secondary_name = DB.Column(DB.Unicode)
    is_id_site_space = DB.Column(DB.Boolean, default=False)
    id_site_space = DB.Column(DB.Integer, ForeignKey(BibSiteSpace.id_site_space))
    id_org = DB.Column(DB.Integer, ForeignKey(BibOrganismes.id_org))
    create_author = DB.Column(DB.Integer, ForeignKey(User.id_role), nullable=False)
    update_author = DB.Column(DB.Integer, ForeignKey(User.id_role), nullable=False)
    create_date = DB.Column(DB.DateTime)
    update_date = DB.Column(DB.DateTime)
    geom = DB.Column(geoalchemy2.Geometry("GEOMETRY", 4326), nullable=False)
    id_lim_list = DB.Column(UUID(as_uuid=True), ForeignKey(CorLimList.id_lim_list), nullable=False)
    remark_lim = DB.Column(DB.Unicode)
    remark_lim_fs = DB.Column(DB.Unicode)
    id_sdage = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), nullable=False)
    id_sage = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))
    remark_pres = DB.Column(DB.Unicode)
    v_habref = DB.Column(DB.Unicode)
    ef_area = DB.Column(DB.Integer)
    global_remark_activity = DB.Column(DB.Unicode)
    id_thread = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("EVAL_GLOB_MENACES"),
    )
    id_frequency = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("SUBMERSION_FREQ"),
    )
    id_spread = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("SUBMERSION_ETENDUE"),
    )
    id_connexion = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))
    id_diag_hydro = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("FONCTIONNALITE_HYDRO"),
    )
    id_diag_bio = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("FONCTIONNALITE_BIO"),
    )
    id_strat_gestion = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("STRAT_GESTION"),
    )
    remark_diag = DB.Column(DB.Unicode)
    is_other_inventory = DB.Column(DB.Boolean, default=False)
    is_carto_hab = DB.Column(DB.Boolean, default=False)
    nb_hab = DB.Column(DB.Integer)
    total_hab_cover = DB.Column(DB.Integer)
    nb_flora_sp = DB.Column(DB.Integer)
    nb_vertebrate_sp = DB.Column(DB.Integer)
    nb_invertebrate_sp = DB.Column(DB.Integer)
    remark_eval_functions = DB.Column(DB.Unicode)
    remark_eval_heritage = DB.Column(DB.Unicode)
    remark_eval_thread = DB.Column(DB.Unicode)
    remark_eval_actions = DB.Column(DB.Unicode)
    remark_is_other_inventory = DB.Column(DB.Unicode)
    main_pict_id = DB.Column(DB.Integer)
    area = DB.Column(DB.Float)
    main_id_rb = DB.Column(DB.Integer, nullable=True)

    sdage = DB.relationship(
        TNomenclatures,
        lazy="joined",
        primaryjoin=(TNomenclatures.id_nomenclature == id_sdage),
    )

    authors = DB.relationship(User, lazy="joined", primaryjoin=(User.id_role == create_author))

    coauthors = DB.relationship(User, lazy="joined", primaryjoin=(User.id_role == update_author))

    def get_geofeature(self, recursif=True, relationships=()):
        return self.as_geofeature(
            "geom",
            "id_zh",
            fields=["authors", "coauthors", "authors.organisme", "coauthors.organisme"],
        )

    @staticmethod
    def get_site_space_name(id):
        return DB.session.scalar(select(BibSiteSpace.name).where(BibSiteSpace.id_site_space == id))

    @staticmethod
    def get_tzh_by_id(id):
        return DB.session.scalar(select(TZH).where(TZH.id_zh == id))

    @staticmethod
    def get_zh_area_intersected(zh_area_type, id_zh_geom):
        if zh_area_type == "river_basin":
            q = DB.session.scalars(
                select(TRiverBasin).where(
                    TRiverBasin.geom.ST_Intersects(cast(id_zh_geom, Geography))
                )
            ).all()
        if zh_area_type == "hydro_area":
            q = DB.session.scalars(
                select(THydroArea).where(THydroArea.geom.ST_Intersects(cast(id_zh_geom, Geography)))
            ).all()
        if zh_area_type == "fct_area":
            q = DB.session.scalars(
                select(TFctArea).where(TFctArea.geom.ST_Intersects(cast(id_zh_geom, Geography)))
            ).all()
        return q

    @hybrid_property
    def delims(self):
        query = select(CorLimList, TNomenclatures).where(
            and_(
                TNomenclatures.id_nomenclature == CorLimList.id_lim,
                CorLimList.id_lim_list == self.id_lim_list,
            )
        )
        delims = [element.TNomenclatures.mnemonique for element in DB.session.execute(query).all()]
        return ", ".join([str(item) for item in delims])

    @hybrid_property
    def bassin_versant(self):
        bassin_versant = [
            name
            for name in DB.session.scalars(
                select(TRiverBasin.name).where(
                    TRiverBasin.id_rb == CorZhRb.id_rb, CorZhRb.id_zh == self.id_zh
                )
            ).all()
        ]
        return ", ".join([str(item) for item in bassin_versant])

    @hybrid_property
    def main_rb_name(self):
        return DB.session.scalar(
            select(TRiverBasin.name).where(TRiverBasin.id_rb == self.main_id_rb)
        )


@serializable
class CorZhArea(DB.Model):
    __tablename__ = "cor_zh_area"
    __table_args__ = {"schema": "pr_zh"}
    id_area = DB.Column(DB.Integer, ForeignKey(LAreas.id_area), primary_key=True)
    id_zh = DB.Column(DB.Integer, primary_key=True)
    cover = DB.Column(DB.Integer)

    @staticmethod
    def get_id_type(mnemo):
        return (
            DB.session.scalars(select(BibAreasTypes).where(BibAreasTypes.type_name == mnemo))
            .one()
            .id_type
        )

    @staticmethod
    def get_departments(id_zh):
        query = (
            select(CorZhArea, LAreas, TZH)
            .join(LAreas)
            .where(
                CorZhArea.id_zh == id_zh,
                LAreas.id_type == CorZhArea.get_id_type("Départements"),
                TZH.id_zh == id_zh,
            )
        )
        return DB.session.execute(query).all()

    @staticmethod
    def get_municipalities_info(id_zh):
        return DB.session.execute(
            select(CorZhArea, LiMunicipalities, TZH)
            .join(LiMunicipalities, LiMunicipalities.id_area == CorZhArea.id_area)
            .where(CorZhArea.id_zh == id_zh, TZH.id_zh == id_zh)
            .order_by(LiMunicipalities.nom_com)
        ).all()

    @staticmethod
    def get_id_types_ref_geo(id_zh, ref_geo_config):
        ids = []
        for ref in ref_geo_config:
            if ref["active"]:
                ids.append(
                    DB.session.scalar(
                        select(BibAreasTypes.id_type).where(
                            BibAreasTypes.type_code == ref["type_code_ref_geo"]
                        )
                    )
                )
        return ids

    @staticmethod
    def get_ref_geo_info(id_zh, id_types):
        return [
            DB.session.execute(
                select(CorZhArea, LAreas, TZH)
                .join(LAreas)
                .where(CorZhArea.id_zh == id_zh, LAreas.id_type == id_type, TZH.id_zh == id_zh)
            ).all()
            for id_type in id_types
        ]


class TRiverBasin(DB.Model):
    __tablename__ = "t_river_basin"
    __table_args__ = {"schema": "pr_zh"}
    id_rb = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.Unicode, nullable=False)
    geom = DB.Column(geoalchemy2.Geometry("GEOMETRY", 4326), nullable=False)
    id_climate_class = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))
    id_river_flow = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))


class CorZhRb(DB.Model):
    __tablename__ = "cor_zh_rb"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    id_rb = DB.Column(DB.Integer, ForeignKey(TRiverBasin.id_rb), primary_key=True)


class THydroArea(DB.Model):
    __tablename__ = "t_hydro_area"
    __table_args__ = {"schema": "pr_zh"}
    id_hydro = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.Unicode, nullable=False)
    geom = DB.Column(geoalchemy2.Geometry("GEOMETRY", 4326), nullable=False)


class CorZhHydro(DB.Model):
    __tablename__ = "cor_zh_hydro"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    id_hydro = DB.Column(DB.Integer, ForeignKey(THydroArea.id_hydro), primary_key=True)


class TFctArea(DB.Model):
    __tablename__ = "t_fct_area"
    __table_args__ = {"schema": "pr_zh"}
    id_fct_area = DB.Column(DB.Integer, primary_key=True)
    geom = DB.Column(geoalchemy2.Geometry("GEOMETRY", 4326), nullable=False)
    area = DB.Column(DB.REAL, nullable=False)


class CorZhFctArea(DB.Model):
    __tablename__ = "cor_zh_fct_area"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    id_fct_area = DB.Column(DB.Integer, ForeignKey(TFctArea.id_fct_area), primary_key=True)


@serializable
class TReferences(DB.Model):
    __tablename__ = "t_references"
    __table_args__ = {"schema": "pr_zh"}
    id_reference = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    authors = DB.Column(DB.Unicode)
    pub_year = DB.Column(DB.Integer)
    title = DB.Column(DB.Unicode, nullable=False)
    editor = DB.Column(DB.Unicode)
    editor_location = DB.Column(DB.Unicode)


class CorZhRef(DB.Model):
    __tablename__ = "cor_zh_ref"
    __table_args__ = {"schema": "pr_zh"}
    id_ref = DB.Column(DB.Integer, ForeignKey(TReferences.id_reference), primary_key=True)
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)

    @staticmethod
    def get_references_by_id(id_zh):
        return DB.session.scalars(
            select(TReferences)
            .join(CorZhRef)
            .where(CorZhRef.id_zh == id_zh)
            .order_by(TReferences.pub_year.desc())
        ).all()


class CorZhLimFs(DB.Model):
    __tablename__ = "cor_zh_lim_fs"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    id_lim_fs = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True)


class CorSdageSage(DB.Model):
    __tablename__ = "cor_sdage_sage"
    __table_args__ = {"schema": "pr_zh"}
    id_sdage = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True)
    id_sage = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True)

    @staticmethod
    def get_id_sdage_list():
        q_id_sdages = DB.session.execute(select(func.distinct(CorSdageSage.id_sdage))).all()
        return [id[0] for id in q_id_sdages]

    @staticmethod
    def get_sage_by_id(id):
        return DB.session.execute(
            select(CorSdageSage, TNomenclatures)
            .join(TNomenclatures, TNomenclatures.id_nomenclature == CorSdageSage.id_sage)
            .where(CorSdageSage.id_sdage == id)
        ).all()


class BibCb(DB.Model):
    __tablename__ = "bib_cb"
    __table_args__ = {"schema": "pr_zh"}
    lb_code = DB.Column(DB.Unicode, primary_key=True)
    humidity = DB.Column(DB.Unicode, nullable=False)
    is_ch = DB.Column(DB.Boolean, nullable=False)

    @staticmethod
    def get_label():
        return DB.session.execute(
            select(BibCb, Habref)
            .join(Habref, BibCb.lb_code == Habref.lb_code)
            .where(Habref.cd_typo == 22)
            .order_by(BibCb.lb_code)
        ).all()

    @staticmethod
    def get_ch(lb_code):
        # get cd_hab_sortie from lb_code of selected Corine Biotope
        # !!! est-ce que method utilisée qqpart ?
        # todo
        """
        cd_hab_sortie = (
            DB.session.query(Habref)
            .filter(and_(Habref.lb_code == lb_code, Habref.cd_typo == 22))
            .one()
            .cd_hab
        )
        # get all cd_hab_entre corresponding to cd_hab_sortie
        #todo
        q_cd_hab_entre = (
            DB.session.query(CorespHab).filter(CorespHab.cd_hab_sortie == cd_hab_sortie).all()
        )
        # get list of cd_hab_entre/lb_code/lb_hab_fr for each cahier habitat
        ch = []
        #todo
        for q in q_cd_hab_entre:
            ch.append(
                {
                    "cd_hab": q.cd_hab_entre,
                    "lb_code": DB.session.query(Habref)
                    .filter(Habref.cd_hab == q.cd_hab_entre)
                    .one()
                    .lb_code,
                    "lb_hab_fr": DB.session.query(Habref)
                    .filter(Habref.cd_hab == q.cd_hab_entre)
                    .one()
                    .lb_hab_fr,
                }
            )
        return ch
        """


class CorChStatus(DB.Model):
    __tablename__ = "cor_ch_status"
    __table_args__ = {"schema": "pr_zh"}
    lb_code = DB.Column(DB.Unicode(length=50), primary_key=True, nullable=False)
    priority = DB.Column(DB.Unicode(length=10), nullable=False)


class CorImpactTypes(DB.Model):
    __tablename__ = "cor_impact_types"
    __table_args__ = {"schema": "pr_zh"}
    id_cor_impact_types = DB.Column(DB.Integer, primary_key=True)
    id_impact = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), nullable=False)
    id_impact_type = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))
    active = DB.Column(DB.Integer, nullable=False)

    @staticmethod
    def get_impacts():
        return DB.session.execute(
            select(CorImpactTypes, TNomenclatures)
            .join(
                TNomenclatures,
                TNomenclatures.id_nomenclature == CorImpactTypes.id_impact,
            )
            .where(CorImpactTypes.active)
        ).all()

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
        DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True
    )
    id_main_function = DB.Column(
        DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), nullable=False
    )
    active = DB.Column(DB.Integer, nullable=False)

    @staticmethod
    def get_functions(nomenc_ids):
        return DB.session.execute(
            select(CorMainFct, TNomenclatures)
            .join(TNomenclatures, TNomenclatures.id_nomenclature == CorMainFct.id_function)
            .where(CorMainFct.active, CorMainFct.id_function.in_(nomenc_ids))
        ).all()

    @staticmethod
    def get_all_functions(nomenc_ids):
        query = (
            select(CorMainFct, TNomenclatures)
            .join(TNomenclatures, TNomenclatures.id_nomenclature == CorMainFct.id_function)
            .where(CorMainFct.id_function.in_(nomenc_ids))
        )
        return DB.session.execute(query).all()

    @staticmethod
    def get_main_function_list(ids):
        # méthode utilisée ?
        q_id_types = DB.session.scalars(select(func.distinct(CorMainFct.id_main_function))).all()
        return [id[0] for id in q_id_types if id[0] in ids]

    @staticmethod
    def get_function_by_main_function(id_main):
        # TODO: méthode utilisée ?
        return DB.session.execute(
            select(CorMainFct, TNomenclatures)
            .join(TNomenclatures, TNomenclatures.id_nomenclature == CorMainFct.id_function)
            .where(and_(CorMainFct.id_main_function == id_main, CorMainFct.active))
        ).all()

    @staticmethod
    def get_mnemo_type(id_type):
        # TODO: methode utilisée ?
        if id_type:
            return DB.session.scalar(
                select(TNomenclatures).where(TNomenclatures.id_nomenclature == id_type)
            )
        else:
            return ""


class CorZhCb(DB.Model):
    __tablename__ = "cor_zh_cb"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    lb_code = DB.Column(DB.Integer, ForeignKey(BibCb.lb_code), primary_key=True)


class CorZhCorineCover(DB.Model):
    __tablename__ = "cor_zh_corine_cover"
    __table_args__ = {"schema": "pr_zh"}
    id_cover = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True)
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)


class CorImpactList(DB.Model):
    __tablename__ = "cor_impact_list"
    __table_args__ = {"schema": "pr_zh"}
    id_impact_list = DB.Column(
        UUID(as_uuid=True),
        ForeignKey("pr_zh.t_activity.id_impact_list", ondelete="CASCADE"),
        primary_key=True,
    )
    id_cor_impact_types = DB.Column(
        DB.Integer, ForeignKey(CorImpactTypes.id_cor_impact_types), primary_key=True
    )

    @staticmethod
    def get_impacts_by_uuid(uuid_activity):
        return DB.session.scalars(
            select(CorImpactList).where(CorImpactList.id_impact_list == uuid_activity)
        ).all()


class TActivity(DB.Model):
    __tablename__ = "t_activity"
    __table_args__ = {"schema": "pr_zh"}
    id_activity = DB.Column(
        DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True
    )
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    id_position = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), nullable=False)
    id_impact_list = DB.Column(UUID(as_uuid=True), nullable=False)
    remark_activity = DB.Column(DB.Unicode)
    child = relationship(CorImpactList, backref="parent", passive_deletes=True)


class TOutflow(DB.Model):
    __tablename__ = "t_outflow"
    __table_args__ = {"schema": "pr_zh"}
    id_outflow = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True)
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    id_permanance = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("PERMANENCE_SORTIE"),
    )
    topo = DB.Column(DB.Unicode)


class TInflow(DB.Model):
    __tablename__ = "t_inflow"
    __table_args__ = {"schema": "pr_zh"}
    id_inflow = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True)
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    id_permanance = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("PERMANENCE_ENTREE"),
    )
    topo = DB.Column(DB.Unicode)


class TFunctions(DB.Model):
    __tablename__ = "t_functions"
    __table_args__ = {"schema": "pr_zh"}
    id_function = DB.Column(
        DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True
    )
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    justification = DB.Column(DB.Unicode(length=2000))
    id_qualification = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("FONCTIONS_QUALIF"),
    )
    id_knowledge = DB.Column(
        DB.Integer,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("FONCTIONS_CONNAISSANCE"),
    )

    @staticmethod
    def get_functions_by_id_and_category(id_zh, category, is_eval=False):
        eval_qualification = ["Moyenne", "Forte"]
        function_ids = [
            nomenclature.id_nomenclature
            for nomenclature in Nomenclatures.get_nomenclature_info(category)
        ]
        if is_eval:
            qualif_ids = [
                nomenclature.id_nomenclature
                for nomenclature in Nomenclatures.get_nomenclature_info("FONCTIONS_QUALIF")
                if nomenclature.mnemonique in eval_qualification
            ]
        else:
            qualif_ids = [
                nomenclature.id_nomenclature
                for nomenclature in Nomenclatures.get_nomenclature_info("FONCTIONS_QUALIF")
            ]

        return DB.session.scalars(
            select(TFunctions).where(
                TFunctions.id_zh == id_zh,
                TFunctions.id_function.in_(function_ids),
                TFunctions.id_qualification.in_(qualif_ids),
            )
        ).all()


class THabHeritage(DB.Model):
    __tablename__ = "t_hab_heritage"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    id_corine_bio = DB.Column(DB.Unicode, ForeignKey(BibCb.lb_code), primary_key=True)
    id_cahier_hab = DB.Column(DB.Unicode, primary_key=True)
    id_preservation_state = DB.Column(
        DB.Unicode,
        ForeignKey(TNomenclatures.id_nomenclature),
        default=TNomenclatures.get_default_nomenclature("ETAT_CONSERVATION"),
    )
    hab_cover = DB.Column(DB.Integer)


class CorUrbanTypeRange(DB.Model):
    __tablename__ = "cor_urban_type_range"
    __table_args__ = {"schema": "pr_zh"}
    id_cor = DB.Column(DB.Integer, primary_key=True)
    id_doc_type = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))
    id_range_type = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))

    @staticmethod
    def get_range_by_doc(doc_id):
        q_ranges = DB.session.scalars(
            select(CorUrbanTypeRange).where(CorUrbanTypeRange.id_doc_type == doc_id)
        ).all()
        ranges = []
        for range in q_ranges:
            ranges.append(
                {
                    "id_cor": range.id_cor,
                    "id_nomenclature": range.id_range_type,
                    "mnemonique": DB.session.scalar(
                        select(TNomenclatures.mnemonique).where(
                            TNomenclatures.id_nomenclature == range.id_range_type
                        )
                    ),
                }
            )
        return ranges


class TUrbanPlanningDocs(DB.Model):
    __tablename__ = "t_urban_planning_docs"
    __table_args__ = {"schema": "pr_zh"}
    id_area = DB.Column(DB.Integer, primary_key=True)
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    id_doc_type = DB.Column(
        DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True
    )
    id_doc = DB.Column(UUID(as_uuid=True), nullable=False)
    remark = DB.Column(DB.Unicode)


class CorZhDocRange(DB.Model):
    __tablename__ = "cor_zh_doc_range"
    __table_args__ = {"schema": "pr_zh"}
    id_doc = DB.Column(DB.Integer, ForeignKey(TUrbanPlanningDocs.id_doc), primary_key=True)
    id_cor = DB.Column(DB.Integer, ForeignKey(CorUrbanTypeRange.id_cor), primary_key=True)


class CorProtectionLevelType(DB.Model):
    __tablename__ = "cor_protection_level_type"
    __table_args__ = {"schema": "pr_zh"}
    id_protection = DB.Column(DB.Integer, primary_key=True)
    id_protection_status = DB.Column(
        DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), nullable=False
    )
    id_protection_type = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))
    id_protection_level = DB.Column(
        DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), nullable=False
    )


@serializable
class BibActions(DB.Model):
    __tablename__ = "bib_actions"
    __table_args__ = {"schema": "pr_zh"}
    id_action = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.Unicode(length=255), nullable=False)

    @staticmethod
    def get_bib_actions():
        q_bib_actions = DB.session.scalars(select(BibActions)).all()
        bib_actions_list = [bib_action.as_dict() for bib_action in q_bib_actions]
        return bib_actions_list


@serializable
class TActions(DB.Model):
    __tablename__ = "t_actions"
    __table_args__ = {"schema": "pr_zh"}
    id_action = DB.Column(DB.Integer, ForeignKey(BibActions.id_action), primary_key=True)
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    id_priority_level = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))
    remark = DB.Column(DB.Unicode(length=2000))


class TInstruments(DB.Model):
    __tablename__ = "t_instruments"
    __table_args__ = {"schema": "pr_zh"}
    id_instrument = DB.Column(
        DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True
    )
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    instrument_date = DB.Column(DB.DateTime)


class TOwnership(DB.Model):
    __tablename__ = "t_ownership"
    __table_args__ = {"schema": "pr_zh"}
    id_status = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True)
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    remark = DB.Column(DB.Unicode(length=2000))


class CorZhProtection(DB.Model):
    __tablename__ = "cor_zh_protection"
    __table_args__ = {"schema": "pr_zh"}
    id_protection = DB.Column(
        DB.Integer, ForeignKey(CorProtectionLevelType.id_protection), primary_key=True
    )
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)


class InseeRegions(DB.Model):
    __tablename__ = "insee_regions"
    __table_args__ = {"schema": "ref_geo"}
    insee_reg = DB.Column(DB.Unicode(length=2), primary_key=True)
    region_name = DB.Column(DB.Unicode(length=50), nullable=False)


class TManagementStructures(DB.Model):
    __tablename__ = "t_management_structures"
    __table_args__ = {"schema": "pr_zh"}
    id_structure = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh))
    id_org = DB.Column(DB.Integer, ForeignKey(BibOrganismes.id_org))


class TManagementPlans(DB.Model):
    __tablename__ = "t_management_plans"
    __table_args__ = {"schema": "pr_zh"}
    id_plan = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    id_nature = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))
    id_structure = DB.Column(DB.Integer, ForeignKey(TManagementStructures.id_structure))
    plan_date = DB.Column(DB.DateTime)
    duration = DB.Column(DB.Integer)
    remark = DB.Column(DB.Unicode(length=2000))


class BibHierPanes(DB.Model):
    __tablename__ = "bib_hier_panes"
    __table_args__ = {"schema": "pr_zh"}
    pane_id = DB.Column(DB.Integer, primary_key=True)
    label = DB.Column(DB.Unicode, nullable=False)


class BibHierCategories(DB.Model):
    __tablename__ = "bib_hier_categories"
    __table_args__ = {"schema": "pr_zh"}
    cat_id = DB.Column(DB.Integer, primary_key=True)
    abbreviation = DB.Column(DB.Unicode(length=4), nullable=False)
    label = DB.Column(DB.Unicode, nullable=False)


class BibHierSubcategories(DB.Model):
    __tablename__ = "bib_hier_subcategories"
    __table_args__ = {"schema": "pr_zh"}
    subcat_id = DB.Column(DB.Integer, primary_key=True)
    label = DB.Column(DB.Unicode, nullable=False)


class BibNoteTypes(DB.Model):
    __tablename__ = "bib_note_types"
    __table_args__ = {"schema": "pr_zh"}
    note_id = DB.Column(DB.Integer, primary_key=True)
    id_knowledge = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), nullable=True)


class TRules(DB.Model):
    __tablename__ = "t_rules"
    __table_args__ = {"schema": "pr_zh"}
    rule_id = DB.Column(DB.Integer, primary_key=True)
    abbreviation = DB.Column(DB.Unicode(length=15), nullable=False)
    pane_id = DB.Column(DB.Integer, ForeignKey(BibHierPanes.pane_id))
    cat_id = DB.Column(DB.Integer, ForeignKey(BibHierCategories.cat_id))
    subcat_id = DB.Column(DB.Integer, ForeignKey(BibHierSubcategories.subcat_id))


class CorRbRules(DB.Model):
    __tablename__ = "cor_rb_rules"
    __table_args__ = {"schema": "pr_zh"}
    cor_rule_id = DB.Column(DB.Integer, primary_key=True)
    rb_id = DB.Column(DB.Integer, ForeignKey(TRiverBasin.id_rb))
    rule_id = DB.Column(DB.Integer, ForeignKey(TRules.rule_id))


class TItems(DB.Model):
    __tablename__ = "t_items"
    __table_args__ = {"schema": "pr_zh"}
    val_id = DB.Column(DB.Integer, primary_key=True)
    cor_rule_id = DB.Column(DB.Integer, ForeignKey(CorRbRules.cor_rule_id))
    attribute_id = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))
    note = DB.Column(DB.Integer, nullable=False)
    note_type_id = DB.Column(DB.Integer, ForeignKey(BibNoteTypes.note_id))


class CorItemValue(DB.Model):
    __tablename__ = "cor_item_value"
    __table_args__ = {"schema": "pr_zh"}
    attribute_id = DB.Column(
        DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True
    )
    val_min = DB.Column(DB.Integer, nullable=False)
    val_max = DB.Column(DB.Integer, nullable=False)


class RbNotesSummary(DB.Model):
    __tablename__ = "rb_notes_summary"
    __table_args__ = {"schema": "pr_zh"}
    bassin_versant = DB.Column(DB.Unicode, primary_key=True)
    global_note = DB.Column(DB.Integer)
    volet_1 = DB.Column(DB.Integer)
    volet_2 = DB.Column(DB.Integer)
    rub_sdage = DB.Column(DB.Integer)
    rub_interet_pat = DB.Column(DB.Integer)
    rub_eco = DB.Column(DB.Integer)
    rub_hydro = DB.Column(DB.Integer)
    rub_socio = DB.Column(DB.Integer)
    rub_statut = DB.Column(DB.Integer)
    rub_etat_fonct = DB.Column(DB.Integer)
    rub_menaces = DB.Column(DB.Integer)


class TCorQualif(DB.Model):
    __tablename__ = "t_cor_qualif"
    __table_args__ = {"schema": "pr_zh"}
    combination = DB.Column(DB.Unicode(length=4), primary_key=True)
    id_qualification = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))


class CorRuleNomenc(DB.Model):
    __tablename__ = "cor_rule_nomenc"
    __table_args__ = {"schema": "pr_zh"}
    rule_id = DB.Column(DB.Integer, ForeignKey(TRules.rule_id), primary_key=True)
    nomenc_id = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature), primary_key=True)
    qualif_id = DB.Column(DB.Integer)


class CorZhNotes(DB.Model):
    __tablename__ = "cor_zh_notes"
    __table_args__ = {"schema": "pr_zh"}
    id_zh = DB.Column(DB.Integer, ForeignKey(TZH.id_zh), primary_key=True)
    cor_rule_id = DB.Column(DB.Integer, ForeignKey(CorRbRules.cor_rule_id), primary_key=True)
    note = DB.Column(DB.Float)
    attribute_id = DB.Column(DB.Integer, ForeignKey(TNomenclatures.id_nomenclature))
    note_type_id = DB.Column(DB.Integer, ForeignKey(BibNoteTypes.note_id))
