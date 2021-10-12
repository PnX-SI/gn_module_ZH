from datetime import datetime

from sqlalchemy.sql.expression import true
from sqlalchemy.util.langhelpers import dependencies

from geonature.utils.env import DB
from geonature.core.ref_geo.models import LAreas

from .zh_schema import *
from .zh import ZH
from ..nomenclatures import get_corine_biotope

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
    def get_bool(bool):
        if bool:
            return 'Oui'
        return 'Non'

    @staticmethod
    def get_string(string):
        if string:
            return string
        return ''

    @staticmethod
    def get_int(nb):
        return nb  # if nb is not None else 'Non évalué'

    @staticmethod
    def is_valid(obj, classe):
        if isinstance(obj, classe):
            return obj
        else:
            raise ValueError("{} is not of {} class".format(obj, classe))


class Limits:

    def __init__(self):
        self.area_limits = Criteria([], None)
        self.function_limits = Criteria([], None)

    def set_area_limits(self, criteria, remark):
        self.area_limits.criteria = criteria
        self.area_limits.remark = remark

    def set_function_limits(self, criteria, remark):
        self.function_limits.criteria = criteria
        self.function_limits.remark = remark

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
        return TZH.get_site_space_name(self.id_site_space) if self.is_id_site_space and self.id_site_space else "Ne fait pas partie d'un grand ensemble"


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

    def __init__(self, id_zh, create_date, update_date):
        self.id_zh = id_zh
        self.create_date = create_date
        self.update_date = update_date
        self.create_author = self.__get_author()
        self.edit_author = self.__get_author(type='co-author')

    def __str__(self):
        return {
            "auteur": self.create_author,
            "auteur_modif": self.edit_author,
            "date": datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S').date().strftime("%d/%m/%Y"),
            "date_modif": datetime.strptime(self.update_date, '%Y-%m-%d %H:%M:%S.%f').date().strftime("%d/%m/%Y")
        }

    def __get_author(self, type='author'):
        if type == 'author':
            prenom = DB.session.query(TZH).filter(
                TZH.id_zh == self.id_zh).one().authors.prenom_role
            nom = DB.session.query(TZH).filter(
                TZH.id_zh == self.id_zh).one().authors.nom_role
        else:
            prenom = DB.session.query(TZH).filter(
                TZH.id_zh == self.id_zh).one().coauthors.prenom_role
            nom = DB.session.query(TZH).filter(
                TZH.id_zh == self.id_zh).one().coauthors.nom_role
        return prenom + ' ' + nom.upper()


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
        self.frequency: int
        self.spread: int

    def __str__(self):
        return {
            "entree": [flow.__str__() for flow in self.inflows],
            "sortie": [flow.__str__() for flow in self.outflows],
            "etendue": Utils.get_mnemo(self.spread),
            "frequence": Utils.get_mnemo(self.frequency)
        }

    def set_regime(self, flows, frequency, spread):
        self.inflows = self.__set_flows(flows[1]['inflows'], type='id_inflow')
        self.outflows = self.__set_flows(
            flows[0]['outflows'], type='id_outflow')
        self.spread = spread
        self.frequency = frequency

    def __set_flows(self, flows, type):
        if flows:
            return [
                Flow(
                    flow[type],
                    flow['id_permanance'],
                    flow['topo']
                ) for flow in flows
            ]
        return []


class Flow:

    def __init__(self, type, permanence, topo):
        self.type = type
        self.permanence = permanence
        self.topo = topo

    def __str__(self):
        return {
            "type": Utils.get_mnemo(self.type),
            "permanence": Utils.get_mnemo(self.permanence),
            "toponymie": Utils.get_string(self.topo)
        }


class Functioning:

    def __init__(self):
        self.regime: Regime
        self.connexion: int
        self.diagnostic: Diagnostic

    def __str__(self):
        return {
            "regime": self.regime.__str__(),
            "connexion": Utils.get_mnemo(self.connexion),
            "diagnostic": self.diagnostic.__str__()
        }


class Diagnostic:

    def __init__(self, diag_hydro, diag_bio, comment):
        self.diag_hydro = diag_hydro
        self.diag_bio = diag_bio
        self.comment = comment

    def __str__(self):
        return {
            "hydrologique": Utils.get_mnemo(self.diag_hydro),
            "biologique": Utils.get_mnemo(self.diag_bio),
            "commentaires": Utils.get_string(self.comment)
        }


class Function:

    def __init__(self, type, qualification, knowledge, justif):
        self.type = type
        self.qualification = qualification
        self.knowledge = knowledge
        self.justif = justif

    def __str__(self):
        return {
            "type": Utils.get_mnemo(self.type),
            "qualification": Utils.get_mnemo(self.qualification),
            "connaissance": Utils.get_mnemo(self.knowledge),
            "justification": Utils.get_string(self.justif)
        }


class Taxa:

    def __init__(self, nb_flora_sp, nb_vertebrate_sp, nb_invertebrate_sp):
        self.nb_flora_sp = nb_flora_sp
        self.nb_vertebrate_sp = nb_vertebrate_sp
        self.nb_invertebrate_sp = nb_invertebrate_sp

    def __str__(self):
        return {
            "nb_flore": Utils.get_int(self.nb_flora_sp),
            "nb_vertebre": Utils.get_int(self.nb_vertebrate_sp),
            "nb_invertebre": Utils.get_int(self.nb_invertebrate_sp)
        }


class HabHeritage:

    def __init__(self, id_corine_bio, id_cahier_hab, id_preservation_state, hab_cover):
        self.id_corine_bio = id_corine_bio
        self.id_cahier_hab = id_cahier_hab
        self.id_preservation_state = id_preservation_state
        self.hab_cover = hab_cover

    def __str__(self):
        return {
            "biotope": DB.session.query(Habref).filter(Habref.lb_code == self.id_corine_bio).filter(Habref.cd_typo == 22).one().lb_hab_fr,
            "etat": Utils.get_mnemo(self.id_preservation_state),
            "cahier": DB.session.query(Habref).filter(Habref.cd_hab == self.id_cahier_hab).one().lb_hab_fr,
            "recouvrement": int(self.hab_cover)
        }


class Habs:

    def __init__(self):
        self.is_carto_hab: bool
        self.nb_hab: int
        self.total_hab_cover: int
        self.hab_heritage: list(HabHeritage)

    def set_hab_heritage(self, habs):
        if habs:
            self.hab_heritage = [HabHeritage(
                hab['id_corine_bio'],
                hab['id_cahier_hab'],
                hab['id_preservation_state'],
                int(hab["hab_cover"])
            ) for hab in habs
            ]
        else:
            self.hab_heritage = []

    def __str__(self):
        return {
            "cartographie": Utils.get_bool(self.is_carto_hab),
            "nombre": Utils.get_int(self.nb_hab),
            "recouvrement": Utils.get_int(int(self.total_hab_cover)),
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
            "espace": Utils.get_mnemo(self.id_corine_landcovers),
            "usage": self.use.__str__()
        }


class Presentation:

    def __init__(self, id_sdage, id_sage, cb_codes_corine_biotope, remark_pres):
        self.id_sdage = id_sdage
        self.id_sage = id_sage
        self.cb_codes_corine_biotope = cb_codes_corine_biotope
        self.remark_pres = remark_pres

    def __str__(self):
        return {
            "sdage": Utils.get_mnemo(self.id_sdage),
            "typologie_locale": Utils.get_mnemo(self.id_sage),
            "corine_biotope": [cb.__str__() for cb in self.cb_codes_corine_biotope],
            "remarques": Utils.get_string(self.remark_pres)
        }


class CorineBiotope:

    def __init__(self, cb_code):
        self.cb_code = cb_code

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
            "Remarques": Utils.get_string(self.remark_activity)
        }


class Activity:

    def __init__(self, id_human_activity, id_localisation, ids_impact, remark_activity):
        self.id_human_activity = id_human_activity
        self.id_localisation = id_localisation
        self.ids_impact = ids_impact
        self.remark_activity = remark_activity

    def __str__(self):
        return {
            "activite": Utils.get_mnemo(self.id_human_activity),
            "impacts": Utils.get_mnemo(self.ids_impact),
            "localisation": Utils.get_mnemo(self.id_localisation),
            "remarques": Utils.get_string(self.remark_activity)
        }


class Card(ZH):

    def __init__(self, id_zh, type):
        self.id_zh = id_zh
        self.type = type
        self.properties = self.get_properties()
        self.eval = self.get_eval()
        self.info = Info()
        self.limits = Limits()
        self.functioning = Functioning()
        self.functions = Functions()
        self.description = Description()
        # self.status
        # self.evaluation

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
            "statuts": "",
            "evaluation": ""
        }

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
        )

    def __set_author(self):
        self.info.authors = Author(
            self.id_zh,
            self.properties['create_date'],
            self.properties['update_date']
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
        self.limits.set_area_limits(
            self.properties['id_lims'],
            self.properties['remark_lim'])
        self.limits.set_function_limits(
            self.properties['id_lims_fs'],
            self.properties['remark_lim_fs'])
        return self.limits.__str__()

    def __set_functioning(self):
        self.__set_regime()
        self.__set_connexion()
        self.__set_diagnostic()
        return self.functioning.__str__()

    def __set_regime(self):
        self.functioning.regime = Regime()
        self.functioning.regime.set_regime(
            self.properties['flows'],
            self.properties['id_frequency'],
            self.properties['id_spread']
        )

    def __set_connexion(self):
        self.functioning.connexion = self.properties['id_connexion']

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
        self.functions.habs.set_hab_heritage(self.properties['hab_heritages'])

    def __set_taxa(self):
        self.functions.taxa = Taxa(
            self.properties['nb_flora_sp'],
            self.properties['nb_vertebrate_sp'],
            self.properties['nb_invertebrate_sp']
        )

    def __set_description(self):
        self.description.presentation = Presentation(
            self.properties['id_sdage'],
            self.properties['id_sage'],
            [CorineBiotope(cb)
             for cb in self.properties['cb_codes_corine_biotope']],
            self.properties['remark_pres']
        )
        self.description.id_corine_landcovers = self.properties['id_corine_landcovers']
        self.__set_use()
        return self.description.__str__()

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

    def get_ownerships_info(self, ownerships):
        if ownerships:
            return [
                {
                    "Statut": self.get_mnemo(ownership['id_status']),
                    "Remarque": ownership['remark']
                }
                for ownership in ownerships
            ]
        return "Non renseigné"

    def get_instruments_info(self, instruments):
        if instruments:
            return [
                {
                    "Instruments contractuels et financiers": self.get_mnemo(instrument['id_instrument']),
                    "Date de mise en oeuvre": str(instrument['instrument_date'])
                }
                for instrument in instruments
            ]
        return "Non renseigné"

    def get_urban_doc_info(self, urban_docs):
        if urban_docs:
            return [
                {
                    "Communes": DB.session.query(LAreas).filter(LAreas.id_area == urban_doc['id_area']).one().area_name,
                    "Type de document communal": self.get_mnemo(urban_doc['id_doc_type']),
                    "Type de classement": [self.get_mnemo(DB.session.query(CorUrbanTypeRange).filter(CorUrbanTypeRange.id_cor == id).one().id_range_type) for id in urban_doc['id_cors']],
                    "Remarques": urban_doc['remark']
                }
                for urban_doc in urban_docs
            ]
        return "Non renseigné"

    def get_protection_names(self, protection_ids):
        q_protections = DB.session.query(CorProtectionLevelType).filter(
            CorProtectionLevelType.id_protection.in_(protection_ids)).all()
        return [
            self.get_mnemo(protection.id_protection_status) for protection in q_protections
        ]

    def get_managements_info(self, managements):
        if managements:
            management_list = []
            for management in managements:
                structure_gestion = DB.session.query(BibOrganismes).filter(
                    BibOrganismes.id_org == management["structure"]).one().name
                if management["plans"]:
                    plan_gestion = {}
                    for plan in management["plans"]:
                        plan_gestion.update({
                            "Nature du plan": self.get_mnemo(plan["id_nature"]),
                            "Date de réalisation": str(plan['plan_date']),
                            "Durée (années)": plan['duration']
                        })
                else:
                    plan_gestion = 'Pas de plan de gestion de la zone humide renseigné pour cette structure'
                management_list.append({
                    "Structure de gestion": structure_gestion,
                    "Plan de gestion": plan_gestion
                })
            return management_list
        return "Non renseigné"

    def get_actions_info(self, actions):
        if actions:
            return [
                {
                    "Proposition d'action": DB.session.query(BibActions).filter(BibActions.id_action == action['id_action']).one().name,
                    "Niveau de priorité": self.get_mnemo(action['id_priority_level']),
                    "Remarques": action['remark']
                }
                for action in actions
            ]
        return "Non renseigné"
