from datetime import datetime

from sqlalchemy import text
#from pypnusershub.db.models import Organisme

from geonature.utils.env import DB
from geonature.core.ref_geo.models import LAreas

from .zh_schema import *
from .zh import ZH
from ..nomenclatures import get_corine_biotope
from ..hierarchy import Hierarchy
from ..api_error import ZHApiError

import pdb


class Utils(ZH):

    @staticmethod
    def get_mnemo(ids):
        if ids:
            if type(ids) is int:
                return DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == ids).one().label_default
            return [DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == id).one().label_default for id in ids]
        return []

    @staticmethod
    def get_cd_and_mnemo(ids):
        if ids:
            if type(ids) is int:
                result = DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == ids).one()
                return (result.cd_nomenclature, result.label_default)
            
            results = []
            for id in ids:
                res = DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == id).one()
                results.append((res.cd_nomenclature, res.label_default))
            return results
        return []

    @staticmethod
    def get_bool(bool):
        if bool:
            return 'Oui'
        return 'Non'

    @staticmethod
    def get_string(string):
        if string:
            return string
        return ''


class Limits:

    def __init__(self):
        self.area_limits = Criteria
        self.function_limits = Criteria

    @property
    def area_limits(self):
        return self.__area_limits

    @area_limits.setter
    def area_limits(self, val):
        self.__area_limits = val

    @property
    def function_limits(self):
        return self.__function_limits

    @function_limits.setter
    def function_limits(self, val):
        self.__function_limits = val

    def __str__(self):
        return {
            "delimitation_zone": self.area_limits.__str__(),
            "delimitation_fonctions": self.function_limits.__str__()
        }


class Criteria:

    def __init__(self, criteria, remark):
        self.criteria = criteria
        self.remark = remark

    def __str__(self):
        return {
            "critere": Utils.get_mnemo(self.criteria),
            "remark": self.remark
        }


class Identification:

    def __init__(self, main_name, other_name, is_id_site_space, id_site_space, code):
        self.main_name = main_name
        self.other_name = other_name
        self.is_id_site_space = is_id_site_space
        self.id_site_space = id_site_space
        self.code = code

    def __str__(self):
        return {
            "nom": self.main_name,
            "autre": self.other_name,
            "inclus": Utils.get_bool(self.is_id_site_space),
            "ensemble": self.__get_site_space_name(),
            "code": self.code
        }

    def __get_site_space_name(self):
        return TZH.get_site_space_name(self.id_site_space) if self.is_id_site_space and self.id_site_space else ''


class Info:

    def __init__(self):
        self.identification: Identification
        self.localisation: Localisation
        self.authors: Author
        self.references: list[Reference]

    def __str__(self):
        return {
            "identification": self.identification.__str__(),
            "localisation": self.localisation.__str__(),
            "auteur": self.authors.__str__(),
            "references": self.references
        }


class Localisation:

    def __init__(self, id_zh, regions, departments):
        self.id_zh = id_zh
        self.regions = regions
        self.departments = departments
        self.municipalities = self.__get_municipalities_info()
        self.river_basin = self.__get_river_basin()

    def __str__(self):
        return {
            "region": self.regions,
            "departement": self.departments,
            "commune": self.municipalities,
            "bassin_versant": self.river_basin
        }

    def __get_river_basin(self):
        return [
            DB.session.query(TRiverBasin)
            .filter(TRiverBasin.id_rb == id).one().name
            for id in [rb.id_rb for rb in DB.session.query(CorZhRb).filter(CorZhRb.id_zh == self.id_zh).all()]
        ]

    def __get_municipalities_info(self):
        return [
            Municipalities(
                municipality.LiMunicipalities.nom_com,
                municipality.LiMunicipalities.insee_com,
                municipality.CorZhArea.cover
            ).__str__()
            for municipality in CorZhArea.get_municipalities_info(self.id_zh)
        ]


class Author:

    def __init__(self, id_zh, create_date, update_date, id_organisme):
        self.id_zh = id_zh
        self.create_date = create_date
        self.update_date = update_date
        self.create_author = self.__get_author()
        self.edit_author = self.__get_author(type='coauthors')
        self.id_organisme = id_organisme

    def __str__(self):
        return {
            "auteur": self.create_author,
            "auteur_modif": self.edit_author,
            "date": datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S').date().strftime("%d/%m/%Y"),
            "date_modif": datetime.strptime(self.update_date, '%Y-%m-%d %H:%M:%S.%f').date().strftime("%d/%m/%Y"),
            # "organism": DB.session.query(Organisme).filter(Organisme.id_organisme == self.id_organisme).one().nom_organisme
            "organism": self.__temporary_get_organism(self.id_organisme)
        }

    def __get_author(self, type='authors'):
        zh = TZH.get_tzh_by_id(self.id_zh)
        prenom = getattr(zh, type).prenom_role
        nom = getattr(zh, type).nom_role
        return prenom + ' ' + nom.upper()

    def __temporary_get_organism(self, id_organism):
        # waiting for update of pypnusershub with Organisme class
        query = \
            """
                SELECT nom_organisme
                FROM utilisateurs.bib_organismes
                WHERE id_organisme = {id_organisme}
            """.format(id_organisme=id_organism)
        return DB.session.execute(text(query)).fetchone().nom_organisme


class Municipalities:

    def __init__(self, name, insee, cover):
        self.name = name
        self.insee = insee
        self.cover = cover

    def __str__(self):
        return {
            "nom": self.name,
            "insee": self.insee,
            "couverture": self.__get_cover()
        }

    def __get_cover(self):
        return str(self.cover) if self.cover is not None else ''


class Reference:

    def __init__(self, id_reference, authors, title, editor, editor_location, pub_year):
        self.id_reference = id_reference
        self.authors = authors
        self.title = title
        self.editor = editor
        self.editor_location = editor_location
        self.pub_year = pub_year

    def __str__(self):
        return {
            "reference": self.id_reference,
            "titre": self.title,
            "auteurs": self.authors,
            "editeur": self.editor,
            "lieu": self.editor_location,
            "annee": self.pub_year
        }


class Regime:

    def __init__(self):
        self.inflows: list(Flow)
        self.outflows: list(Flow)
        self.id_frequency: int
        self.id_spread: int

    @property
    def inflows(self):
        return self.__inflows

    @property
    def outflows(self):
        return self.__outflows

    @property
    def id_frequency(self):
        return self.__id_frequency

    @property
    def id_spread(self):
        return self.__id_spread

    @inflows.setter
    def inflows(self, value):
        self.__inflows = [
            Flow(
                flow['id_inflow'],
                flow['id_permanance'],
                flow['topo']
            ) for flow in value
        ]

    @outflows.setter
    def outflows(self, value):
        self.__outflows = [
            Flow(
                flow['id_outflow'],
                flow['id_permanance'],
                flow['topo']
            ) for flow in value
        ]

    @id_frequency.setter
    def id_frequency(self, value):
        self.__id_frequency = value

    @id_spread.setter
    def id_spread(self, value):
        self.__id_spread = value

    def __str__(self):
        return {
            "entree": [flow.__str__() for flow in self.inflows],
            "sortie": [flow.__str__() for flow in self.outflows],
            "etendue": Utils.get_mnemo(self.id_spread),
            "frequence": Utils.get_mnemo(self.id_frequency)
        }


class Flow:

    def __init__(self, id_flow, id_permanance, topo):
        self.id_flow = id_flow
        self.id_permanance = id_permanance
        self.topo = topo

    def __str__(self):
        return {
            "type": Utils.get_mnemo(self.id_flow),
            "permanence": Utils.get_mnemo(self.id_permanance),
            "toponymie": Utils.get_string(self.topo)
        }


class Functioning:

    def __init__(self):
        self.regime = Regime()
        self.id_connexion: int
        self.diagnostic: Diagnostic

    def __str__(self):
        return {
            "regime": self.regime.__str__(),
            "connexion": Utils.get_mnemo(self.id_connexion),
            "diagnostic": self.diagnostic.__str__()
        }


class Diagnostic:

    def __init__(self, id_diag_hydro, id_diag_bio, remark_diag):
        self.id_diag_hydro: int = id_diag_hydro
        self.id_diag_bio: int = id_diag_bio
        self.remark_diag: str = remark_diag

    def __str__(self):
        return {
            "hydrologique": Utils.get_mnemo(self.id_diag_hydro),
            "biologique": Utils.get_mnemo(self.id_diag_bio),
            "commentaires": Utils.get_string(self.remark_diag)
        }


class Function:

    def __init__(self, type, qualification, knowledge, justif):
        self.type: int = type
        self.qualification: int = qualification
        self.knowledge: int = knowledge
        self.justif: str = justif

    def __str__(self):
        return {
            "type": Utils.get_mnemo(self.type),
            "qualification": Utils.get_mnemo(self.qualification),
            "connaissance": Utils.get_mnemo(self.knowledge),
            "justification": Utils.get_string(self.justif)
        }


class Taxa:

    def __init__(self, nb_flora_sp, nb_vertebrate_sp, nb_invertebrate_sp):
        self.nb_flora_sp: int = nb_flora_sp
        self.nb_vertebrate_sp: int = nb_vertebrate_sp
        self.nb_invertebrate_sp: int = nb_invertebrate_sp

    def __str__(self):
        return {
            "nb_flore": self.nb_flora_sp,
            "nb_vertebre": self.nb_vertebrate_sp,
            "nb_invertebre": self.nb_invertebrate_sp
        }


class HabHeritage:

    def __init__(self, id_corine_bio, id_cahier_hab, id_preservation_state, hab_cover):
        self.id_corine_bio: str = id_corine_bio
        self.id_cahier_hab: str = id_cahier_hab
        self.id_preservation_state: int = id_preservation_state
        self.hab_cover: int = hab_cover

    def __str__(self):
        return {
            "biotope": DB.session.query(Habref).filter(Habref.lb_code == self.id_corine_bio).filter(Habref.cd_typo == 22).one().lb_hab_fr,
            "etat": Utils.get_mnemo(self.id_preservation_state),
            "cahier": DB.session.query(Habref).filter(Habref.cd_hab == self.id_cahier_hab).one().lb_hab_fr,
            "recouvrement": self.hab_cover
        }


class Habs:

    def __init__(self):
        self.is_carto_hab: bool
        self.nb_hab: int
        self.total_hab_cover: int
        self.hab_heritage: list(HabHeritage)

    @property
    def hab_heritage(self):
        return self.__hab_heritage

    @hab_heritage.setter
    def hab_heritage(self, habs):
        if habs:
            self.__hab_heritage = [
                HabHeritage(
                    hab['id_corine_bio'],
                    hab['id_cahier_hab'],
                    hab['id_preservation_state'],
                    hab["hab_cover"]
                ) for hab in habs
            ]
        else:
            self.__hab_heritage = []

    def __str__(self):
        return {
            "cartographie": Utils.get_bool(self.is_carto_hab),
            "nombre": self.nb_hab,
            "recouvrement": self.total_hab_cover,
            "corine": [hab.__str__() for hab in self.hab_heritage]
        }


class Functions:

    def __init__(self):
        self.hydro: list(Function)
        self.bio: list(Function)
        self.interest: list(Function)
        self.habs: Habs
        self.taxa: Taxa
        self.val_soc_eco: list(Function)

    def set_function(self, functions):
        return [
            Function(
                function["id_function"],
                function["id_qualification"],
                function["id_knowledge"],
                function["justification"]
            ) for function in functions
        ]

    def __str__(self):
        return {
            "hydrologie": [hydro.__str__() for hydro in self.hydro],
            "biologie": [bio.__str__() for bio in self.bio],
            "interet": [interest.__str__() for interest in self.interest],
            "habitats": self.habs.__str__(),
            "taxons": self.taxa.__str__(),
            "socio": [val_soc_eco.__str__() for val_soc_eco in self.val_soc_eco]
        }


class Description:

    def __init__(self):
        self.presentation: Presentation
        self.id_corine_landcovers: list(int)
        self.use: Use

    def __str__(self):
        return {
            "presentation": self.presentation.__str__(),
            "espace": [f"{cd} - {label}" for cd, label in Utils.get_cd_and_mnemo(self.id_corine_landcovers)],
            "usage": self.use.__str__()
        }


class Presentation:

    def __init__(self, area, id_sdage, id_sage, cb_codes_corine_biotope, remark_pres):
        self.area: float = area
        self.id_sdage: int = id_sdage
        self.id_sage: int = id_sage
        self.cb_codes_corine_biotope: list(
            CorineBiotope) = cb_codes_corine_biotope
        self.remark_pres: str = remark_pres

    def __str__(self):
        return {
            "area": self.area,
            "sdage": Utils.get_mnemo(self.id_sdage),
            "typologie_locale": Utils.get_mnemo(self.id_sage),
            "corine_biotope": [cb.__str__() for cb in self.cb_codes_corine_biotope],
            "remarques": Utils.get_string(self.remark_pres)
        }


class CorineBiotope:

    def __init__(self, cb_code):
        self.cb_code: str = cb_code

    def __str__(self):
        cbs = get_corine_biotope()
        for cb in cbs:
            if cb["CB_code"] == self.cb_code:
                return {
                    "code": cb["CB_code"],
                    "label": cb["CB_label"],
                    "Humidité": cb["CB_humidity"]
                }


class Use:

    def __init__(self):
        self.activities: list(Activity)
        self.id_thread: int
        self.remark_activity: str

    def __str__(self):
        return {
            "activities": [activity.__str__() for activity in self.activities],
            "evaluation_menaces": Utils.get_mnemo(self.id_thread),
            "remarques": Utils.get_string(self.remark_activity)
        }


class Activity:

    def __init__(self, id_human_activity, id_localisation, ids_impact, remark_activity):
        self.id_human_activity: int = id_human_activity
        self.id_localisation: int = id_localisation
        self.ids_impact: list(int) = ids_impact
        self.remark_activity: str = remark_activity

    def __str_impact(self):
        return [cor.TNomenclatures.mnemonique for cor in CorImpactTypes.get_impacts() if cor.CorImpactTypes.id_cor_impact_types in self.ids_impact]

    def __str__(self):
        return {
            "activite": Utils.get_mnemo(self.id_human_activity),
            "impacts": self.__str_impact(),
            "localisation": Utils.get_mnemo(self.id_localisation),
            "remarques": Utils.get_string(self.remark_activity)
        }


class Status:

    def __init__(self):
        self.id_zh: int
        self.ownerships: list(Ownership)
        self.managements: list(Management)
        self.instruments: list(Instrument)
        self.other_ref_geo: list(dict)
        self.is_other_inventory: bool
        self.remark_is_other_inventory: str
        self.protections: list(int)
        self.urban_docs: list(UrbanDoc)

    @property
    def id_zh(self):
        return self.__id_zh

    @property
    def ownerships(self):
        return self.__ownerships

    @property
    def managements(self):
        return self.__managements

    @property
    def instruments(self):
        return self.__instruments

    @property
    def other_ref_geo(self):
        return self.__other_ref_geo

    @property
    def is_other_inventory(self):
        return self.__is_other_inventory

    @property
    def remark_is_other_inventory(self):
        return self.__remark_is_other_inventory

    @property
    def protections(self):
        return self.__protections

    @property
    def urban_docs(self):
        return self.__urban_docs

    @id_zh.setter
    def id_zh(self, value):
        self.__id_zh = value

    @ownerships.setter
    def ownerships(self, value):
        self.__ownerships = [
            Ownership(
                ownership['id_status'],
                ownership['remark']
            ) for ownership in value
        ]

    @managements.setter
    def managements(self, value):
        self.__managements = []
        for management in value:
            plans = [
                Plan(
                    plan['id_nature'],
                    plan['plan_date'],
                    plan['duration']
                ) for plan in management['plans']
            ]
            mng = Management()
            mng.set_management(
                management['structure'],
                plans
            )
            self.__managements.append(mng)

    @instruments.setter
    def instruments(self, instruments):
        self.__instruments = [
            Instrument(
                instrument['id_instrument'],
                instrument['instrument_date']
            ) for instrument in instruments
        ]

    @other_ref_geo.setter
    def other_ref_geo(self, ref_geo):
        id_types = CorZhArea.get_id_types_ref_geo(self.id_zh, ref_geo)
        refs = []
        for ref in CorZhArea.get_ref_geo_info(self.id_zh, id_types):
            for i in ref:
                type_code = DB.session.query(BibAreasTypes).filter(
                    BibAreasTypes.id_type == i.LAreas.id_type).one().type_code
                refs.append({
                    "area_name": i.LAreas.area_name,
                    "area_code": i.LAreas.area_code,
                    "url": i.LAreas.source,
                    "type_code": type_code,
                    "zh_type_name": [ref['zh_name'] for ref in ref_geo if ref['type_code_ref_geo'] == type_code][0]
                })
        self.__other_ref_geo = refs

    @is_other_inventory.setter
    def is_other_inventory(self, value):
        self.__is_other_inventory = value

    @remark_is_other_inventory.setter
    def remark_is_other_inventory(self, value):
        self.__remark_is_other_inventory = value

    @urban_docs.setter
    def urban_docs(self, urban_docs):
        self.__urban_docs = [
            UrbanDoc(
                urban_doc['id_area'],
                urban_doc['id_doc_type'],
                urban_doc['id_cors'],
                urban_doc['remark']
            ) for urban_doc in urban_docs
        ]

    @protections.setter
    def protections(self, protections):
        self.__protections: list(int) = protections

    def __str_protections(self):
        q_protections = DB.session.query(CorProtectionLevelType)\
            .filter(CorProtectionLevelType.id_protection_status.in_(self.protections))\
            .all()
        return [
            Utils.get_mnemo(protection.id_protection_status)
            for protection in q_protections
        ]

    def __str__(self):
        return {
            "regime": [ownership.__str__() for ownership in self.ownerships],
            "structure": [management.__str__() for management in self.managements],
            "instruments": [instrument.__str__() for instrument in self.instruments],
            "autre_inventaire": self.__other_ref_geo,
            "autre_etude": Utils.get_bool(self.is_other_inventory),
            "autre_etude_commentaire": self.remark_is_other_inventory,
            "statuts": self.__str_protections(),
            "zonage": [urban_doc.__str__() for urban_doc in self.urban_docs]
        }


class Ownership:

    def __init__(self, id_status, remark):
        self.id_status: int = id_status
        self.remark: str = remark

    def __str__(self):
        return {
            "status": Utils.get_mnemo(self.id_status),
            "remarques": Utils.get_string(self.remark)
        }


class Management:

    def __init__(self):
        self.id_org: int
        self.plans: list(Plan)

    def set_management(self, id_org, plans):
        self.id_org = id_org
        self.plans = plans

    def __str__(self):
        return {
            "structure": DB.session.query(BibOrganismes).filter(BibOrganismes.id_org == self.id_org).one().name,
            "plans": [plan.__str__() for plan in self.plans]
        }


class Plan:

    def __init__(self, id_nature, plan_date, duration):
        self.id_nature: int = id_nature
        self.plan_date: str = plan_date
        self.duration: int = duration

    def __str__(self):
        return {
            "plan": Utils.get_mnemo(self.id_nature),
            "date": Utils.get_string(str(self.plan_date)),
            "duree": self.duration
        }


class Instrument:

    def __init__(self, id_instrument, instrument_date):
        self.id_instrument: int = id_instrument
        self.instrument_date: str = instrument_date

    def __str__(self):
        return {
            "instrument": Utils.get_mnemo(self.id_instrument),
            "date": self.instrument_date
        }


class UrbanDoc:

    def __init__(self, id_area, id_doc_type, id_cors, remark):
        self.id_area: int = id_area
        self.id_doc_type: int = id_doc_type
        self.id_cors: list(int) = id_cors
        self.remark: str = remark

    def __str__(self):
        return {
            "commune": DB.session.query(LAreas).filter(LAreas.id_area == self.id_area).one().area_name,
            "type_doc": Utils.get_mnemo(self.id_doc_type),
            "type_classement": [Utils.get_mnemo(DB.session.query(CorUrbanTypeRange).filter(CorUrbanTypeRange.id_cor == id).one().id_range_type) for id in self.id_cors],
            "remarque": Utils.get_string(self.remark)
        }


class Evaluation:

    def __init__(self):
        self.main_functions = EvalMainFunction()
        self.interest = EvalInterest()
        self.thread = EvalThread()
        self.action = EvalAction()

    def __str__(self):
        return {
            "fonctions": self.main_functions.__str__(),
            "interet": self.interest.__str__(),
            "bilan": self.thread.__str__(),
            "strategie": self.action.__str__()
        }


class EvalMainFunction:

    def __init__(self):
        self.hydro: list(Function)
        self.bio: list(Function)

    @property
    def hydro(self):
        return self.__hydro

    @hydro.setter
    def hydro(self, val):
        self.__hydro = [
            Function(
                v['id_function'],
                v['id_knowledge'],
                v['id_qualification'],
                v['justification']
            ) for v in val
        ]

    @property
    def bio(self):
        return self.__bio

    @bio.setter
    def bio(self, value):
        self.__bio = [
            Function(
                v['id_function'],
                v['id_knowledge'],
                v['id_qualification'],
                v['justification']
            ) for v in value
        ]

    def __str__(self):
        return {
            "hydrologique": [hydro.__str__() for hydro in self.hydro],
            "biologique": [bio.__str__() for bio in self.bio]
        }


class EvalInterest:

    def __init__(self):
        self.interet_patrim: list(Function)
        self.nb_fauna_sp: int
        self.nb_flora_sp: int
        self.nb_hab: int
        self.total_hab_cover: int
        self.val_soc_eco: list(Function)
        self.remark_eval_functions: str

    @property
    def interet_patrim(self):
        return self.__interet_patrim

    @interet_patrim.setter
    def interet_patrim(self, val):
        self.__interet_patrim = [
            Function(
                i['id_function'],
                i['id_knowledge'],
                i['id_qualification'],
                i['justification']
            ) for i in val
        ]

    @property
    def val_soc_eco(self):
        return self.__val_soc_eco

    @val_soc_eco.setter
    def val_soc_eco(self, val):
        self.__val_soc_eco = [
            Function(
                i['id_function'],
                i['id_knowledge'],
                i['id_qualification'],
                i['justification']
            ) for i in val
        ]

    @interet_patrim.setter
    def interet_patrim(self, val):
        self.__interet_patrim = [
            Function(
                i['id_function'],
                i['id_knowledge'],
                i['id_qualification'],
                i['justification']
            ) for i in val
        ]

    def __str__(self):
        return {
            "interet": [interest.__str__() for interest in self.interet_patrim],
            "faunistique": self.nb_fauna_sp,
            "floristique": self.nb_flora_sp,
            "nb_hab": self.nb_hab,
            "total_hab_cover": self.total_hab_cover,
            "valeur": [val.__str__() for val in self.val_soc_eco],
            "Commentaire": self.remark_eval_functions
        }


class EvalThread:

    def __init__(self):
        self.id_thread: int
        self.id_diag_hydro: int
        self.id_diag_bio: int
        self.remark_eval_thread: str

    def set_thread(self, id_thread, id_diag_hydro, id_diag_bio, remark_eval_thread):
        self.id_thread = id_thread
        self.id_diag_hydro = id_diag_hydro
        self.id_diag_bio = id_diag_bio
        self.remark_eval_thread = remark_eval_thread

    def __str__(self):
        return {
            "menaces": Utils.get_mnemo(self.id_thread),
            "hydrologique": Utils.get_mnemo(self.id_diag_hydro),
            "biologique": Utils.get_mnemo(self.id_diag_bio),
            "Commentaire": self.remark_eval_thread,
        }


class EvalAction:

    def __init__(self):
        self.__actions: list(Action)
        self.__remark_eval_actions: str

    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, val):
        self.__actions = [
            Action(
                action["id_action"],
                action["id_priority_level"],
                action["remark"]
            ) for action in val
        ]

    @property
    def remark_eval_actions(self):
        return self.__remark_eval_actions

    @remark_eval_actions.setter
    def remark_eval_actions(self, val):
        self.__remark_eval_actions = val

    def __str__(self):
        return {
            "propositions": [action.__str__() for action in self.actions],
            "commentaires": Utils.get_string(self.remark_eval_actions)
        }


class Action:

    def __init__(self, id_action, id_priority_level, remark):
        self.id_action: int = id_action
        self.id_priority_level: int = id_priority_level
        self.remark: str = remark

    def __str__(self):
        return {
            "proposition": DB.session.query(BibActions).filter(BibActions.id_action == self.id_action).one().name,
            "niveau": Utils.get_mnemo(self.id_priority_level),
            "remarque": Utils.get_string(self.remark)
        }


class Card(ZH):

    def __init__(self, id_zh, type, ref_geo_config):
        self.id_zh = id_zh
        self.type = type
        self.ref_geo_config = ref_geo_config
        self.properties = self.get_properties()
        self.eval = self.get_eval()
        self.info = Info()
        self.limits = Limits()
        self.functioning = Functioning()
        self.functions = Functions()
        self.description = Description()
        self.status = Status()
        self.evaluation = Evaluation()
        try:
            self.hierarchy = Hierarchy(id_zh)
        except ZHApiError:
            self.hierarchy = None
    
    def get_properties(self):
        return ZH(self.id_zh).__repr__()['properties']

    def get_eval(self):
        return ZH(self.id_zh).get_eval()

    def __repr__(self):
        return {
            "renseignements": self.__set_info(),
            "delimitation": self.__set_limits(),
            "description": self.__set_description(),
            "fonctionnement": self.__set_functioning(),
            "fonctions": self.__set_zh_functions(),
            "statuts": self.__set_statuses(),
            "evaluation": self.__set_evaluation(),
            "hierarchy": self.__set_hierarchy(),
            "geometry": self.__set_geometry()
        }

    def __set_geometry(self):
        return ZH(self.id_zh).__repr__()["geometry"]

    def __set_info(self):
        self.__set_identification()
        self.__set_localisation()
        self.__set_author()
        self.__set_references()
        return self.info.__str__()

    def __set_identification(self):
        self.info.identification = Identification(
            self.properties['main_name'],
            self.properties['secondary_name'],
            self.properties['is_id_site_space'],
            self.properties['id_site_space'],
            self.properties['code']
        )

    def __set_localisation(self):
        self.info.localisation = Localisation(
            self.id_zh,
            self.properties['geo_info']['regions'],
            self.properties['geo_info']['departments']
            # self.ref_geo_config
        )

    def __set_author(self):
        self.info.authors = Author(
            self.id_zh,
            self.properties['create_date'],
            self.properties['update_date'],
            self.properties['authors']['id_organisme']
        )

    def __set_references(self):
        self.info.references = [Reference(
            ref["id_reference"],
            ref["authors"],
            ref["title"],
            ref["editor"],
            ref["editor_location"],
            ref["pub_year"]
        ).__str__()
            for ref in self.properties['id_references']
        ]

    def __set_limits(self):
        area_limits = Criteria(
            self.properties['id_lims'],
            self.properties['remark_lim']
        )
        self.limits.area_limits = area_limits
        function_limits = Criteria(
            self.properties['id_lims_fs'],
            self.properties['remark_lim_fs']
        )
        self.limits.function_limits = function_limits
        return self.limits.__str__()

    def __set_functioning(self):
        self.__set_regime()
        self.__set_connexion()
        self.__set_diagnostic()
        return self.functioning.__str__()

    def __set_regime(self):
        self.functioning.regime = Regime()
        self.functioning.regime.inflows = self.properties['flows'][1]['inflows']
        self.functioning.regime.outflows = self.properties['flows'][0]['outflows']
        self.functioning.regime.id_frequency = self.properties['id_frequency']
        self.functioning.regime.id_spread = self.properties['id_spread']

    def __set_connexion(self):
        self.functioning.id_connexion = self.properties['id_connexion']

    def __set_diagnostic(self):
        self.functioning.diagnostic = Diagnostic(
            self.properties['id_diag_hydro'],
            self.properties['id_diag_bio'],
            self.properties['remark_diag']
        )

    def __set_zh_functions(self):
        self.functions.hydro = self.functions.set_function(
            self.properties['fonctions_hydro'])
        self.functions.bio = self.functions.set_function(
            self.properties['fonctions_bio'])
        self.functions.interest = self.functions.set_function(
            self.properties['interet_patrim'])
        self.__set_habs()
        self.__set_taxa()
        self.functions.val_soc_eco = self.functions.set_function(
            self.properties['val_soc_eco'])
        return self.functions.__str__()

    def __set_habs(self):
        self.functions.habs = Habs()
        self.functions.habs.is_carto_hab = self.properties['is_carto_hab']
        self.functions.habs.nb_hab = self.properties['nb_hab']
        self.functions.habs.total_hab_cover = self.properties['total_hab_cover']
        self.functions.habs.hab_heritage = self.properties['hab_heritages']

    def __set_taxa(self):
        self.functions.taxa = Taxa(
            self.properties['nb_flora_sp'],
            self.properties['nb_vertebrate_sp'],
            self.properties['nb_invertebrate_sp']
        )

    def __set_description(self):
        self.description.presentation = Presentation(
            self.properties['area'],
            self.properties['id_sdage'],
            self.properties['id_sage'],
            self.__get_cb(),
            self.properties['remark_pres']
        )
        self.description.id_corine_landcovers = self.properties['id_corine_landcovers']
        self.__set_use()
        return self.description.__str__()

    def __get_cb(self):
        return [
            CorineBiotope(cb) for cb in self.properties['cb_codes_corine_biotope']
        ]

    def __set_use(self):
        self.description.use = Use()
        self.description.use.activities = [
            Activity(
                activity['id_human_activity'],
                activity['id_localisation'],
                activity['ids_impact'],
                activity['remark_activity']
            ) for activity in self.properties['activities']
        ]
        self.description.use.id_thread = self.properties['id_thread']
        self.description.use.remark_activity = self.properties['global_remark_activity']

    def __set_statuses(self):
        self.status.id_zh = self.id_zh
        self.status.ownerships = self.properties['ownerships']
        self.status.managements = self.properties['managements']
        self.status.instruments = self.properties['instruments']
        self.status.other_ref_geo = self.ref_geo_config
        self.status.is_other_inventory = self.properties['is_other_inventory']
        self.status.remark_is_other_inventory = self.properties['remark_is_other_inventory']
        self.status.protections = self.properties['protections']
        self.status.urban_docs = self.properties['urban_docs']
        return self.status.__str__()
    
    def __set_hierarchy(self):
        return self.hierarchy.__str__() if self.hierarchy is not None else None

    def __set_evaluation(self):
        self.__set_main_functions()
        self.__set_interests()
        self.__set_threads()
        self.__set_actions()
        return self.evaluation.__str__()

    def __set_interests(self):
        self.evaluation.interest.interet_patrim = self.eval['interet_patrim']
        self.evaluation.interest.nb_fauna_sp = self.eval['nb_fauna_sp']
        self.evaluation.interest.nb_flora_sp = self.eval['nb_flora_sp']
        self.evaluation.interest.nb_hab = self.eval['nb_hab']
        self.evaluation.interest.total_hab_cover = self.eval['total_hab_cover']
        self.evaluation.interest.val_soc_eco = self.eval['val_soc_eco']
        self.evaluation.interest.remark_eval_functions = self.properties['remark_eval_functions']

    def __set_main_functions(self):
        self.evaluation.main_functions.hydro = self.eval['fonctions_hydro']
        self.evaluation.main_functions.bio = self.eval['fonctions_bio']

    def __set_threads(self):
        self.evaluation.thread.set_thread(
            self.eval['id_thread'],
            self.eval['id_diag_hydro'],
            self.eval['id_diag_bio'],
            self.properties['remark_eval_thread']
        )

    def __set_actions(self):
        self.evaluation.action.actions = self.properties['actions']
        self.evaluation.action.remark_eval_actions = self.properties['remark_eval_actions']
