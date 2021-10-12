from datetime import datetime

from sqlalchemy.sql.expression import true

from geonature.utils.env import DB
from geonature.core.ref_geo.models import LAreas

from .zh_schema import *
from .zh import ZH

import pdb


class Utils(ZH):

    @staticmethod
    def get_mnemo(ids):
        if ids:
            if type(ids) is int:
                return DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == ids).one().label_default
            return [DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == id).one().label_default for id in ids]
        return "Non renseigné"

    @staticmethod
    def get_bool(bool):
        if bool:
            return 'Oui'
        return 'Non'

    @staticmethod
    def get_string(string):
        if string:
            return string
        return 'Non renseigné'


class Delimitations:

    def __init__(self):
        self.area_limits = Criteria([], None)
        self.function_limits = Criteria([], None)

    def set_area_limits(self, criteria, remark):
        self.area_limits.criteria = criteria
        self.function_limits.remark = remark

    def set_function_limits(self, criteria, remark):
        self.area_limits.criteria = criteria
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


class Info:

    def __init__(self, identification, localisation, authors, references):
        self.identification = identification
        self.localisation = localisation
        self.authors = authors
        self.references = references

    def __str__(self):
        return {
            "identification": self.identification.__str__(),
            "localisation": self.localisation.__str__(),
            "auteur": self.authors.__str__(),
            "references": self.references
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
        self.create_author = self.__get_author(),
        self.edit_author = self.__get_author(type='co-author'),

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
        return str(self.cover) if self.cover is not None else 'Non renseigné'


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

    def __init__(self, flows, frequency, spread):
        self.inflows = flows[1]['inflows'],
        self.outflows = flows[0]['outflows'],
        self.frequency = frequency,
        self.spread = spread

    def __str__(self):
        return {
            "entree": self.__get_flows(self.inflows, type='id_inflow'),
            "sortie": self.__get_flows(self.outflows, type='id_outflow'),
            "frequence": Utils.get_mnemo(self.frequency[0]),
            "etendue": Utils.get_mnemo(self.spread)
        }

    def __get_flows(self, flows, type):
        if flows[0]:
            return [
                Flow(
                    flow[type],
                    flow['id_permanance'],
                    flow['topo']
                ).__str__() for flow in flows[0]
            ]
        return "Non renseigné"


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

    def __init__(self, regime, connexion, diagnostic):
        self.regime = regime
        self.connexion = connexion
        self.diagnostic = diagnostic

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


class Card(ZH):

    def __init__(self, id_zh, type):
        self.id_zh = id_zh
        self.type = type
        self.properties = self.get_properties()
        self.eval = self.get_eval()
        self.na_hab_cover = "999"

    def get_properties(self):
        return ZH(self.id_zh).__repr__()['properties']

    def get_eval(self):
        return ZH(self.id_zh).get_eval()

    def __repr__(self):
        return {
            "renseignements": self.__get_info(),
            "delimitation": self.__get_delimitations(),
            "description": "",
            "fonctionnement": self.__get_functioning(),
            "fonctions": "",
            "statuts": "",
            "evaluation": ""
        }

    def __get_info(self):
        identification = self.__get_identification()
        localisation = self.__get_localisation()
        authors = self.__get_author()
        references = self.__get_references()
        info = Info(identification, localisation, authors, references)
        return info.__str__()

    def __get_identification(self):
        return Identification(
            self.properties['main_name'],
            self.properties['secondary_name'],
            self.properties['is_id_site_space'],
            self.properties['id_site_space'],
            self.properties['code']
        )

    def __get_localisation(self):
        return Localisation(
            self.id_zh,
            self.properties['geo_info']['regions'],
            self.properties['geo_info']['departments']
        )

    def __get_author(self):
        return Author(
            self.id_zh,
            self.properties['create_date'],
            self.properties['update_date']
        )

    def __get_references(self):
        return [
            Reference(
                ref["id_reference"],
                ref["authors"],
                ref["title"],
                ref["editor"],
                ref["editor_location"],
                ref["pub_year"]
            ).__str__()
            for ref in self.properties['id_references']
        ]

    def __get_delimitations(self):
        delimitation = Delimitations()
        delimitation.set_area_limits(
            self.properties['id_lims'],
            self.properties['remark_lim'])
        delimitation.set_function_limits(
            self.properties['id_lims_fs'],
            self.properties['remark_lim_fs'])
        return delimitation.__str__()

    def __get_functioning(self):
        regime = self.__get_regime()
        connexion = self.properties['id_connexion']
        diagnostic = self.__get_diagnostic()
        functioning = Functioning(regime, connexion, diagnostic)
        return functioning.__str__()

    def __get_regime(self):
        return Regime(
            self.properties['flows'],
            self.properties['id_frequency'],
            self.properties['id_spread']
        )

    def __get_diagnostic(self):
        return Diagnostic(
            self.properties['id_diag_hydro'],
            self.properties['id_diag_bio'],
            self.properties['remark_diag']
        )

    def get_na_hab_cover(self):
        return self.__na_hab_cover

    def get_activities(self, activities):
        if activities:
            return [
                {
                    "Activité humaine": self.get_mnemo(activity['id_human_activity']),
                    "Localisation": self.get_mnemo(activity['id_localisation']),
                    "Impacts": self.get_mnemo(activity['ids_impact']),
                    "Remarques": activity['remark_activity']
                }
                for activity in activities
            ]
        return "Non renseigné"

    def get_cb(self, cb_ids):
        if cb_ids:
            cbs = BibCb.get_label()
            cbs_info = {}
            for cb in cbs:
                if cb.BibCb.lb_code in cb_ids:
                    cbs_info.update({
                        "Code Corine Biotope": cb.BibCb.lb_code,
                        "Libellé Corine Biotope": cb.Habref.lb_hab_fr,
                        "Humidité": cb.BibCb.humidity
                    })
            return cbs_info
        return "Non renseigné"

    def get_flows(self, flows, type):
        if type == "inflows":
            flow_type = "Entrée d'eau"
            id_key = "id_inflow"
            flows = flows[1]  # to do : correct json input
        else:
            flow_type = "Sortie d'eau"
            id_key = "id_outflow"
            flows = flows[0]  # to do : correct json input
        if flows[type]:
            return [
                {
                    flow_type: self.get_mnemo(flow[id_key]),
                    "Permanence": self.get_mnemo(flow["id_permanance"]),
                    "Toponymie et compléments d'information": flow["topo"]
                }
                for flow in flows[type]
            ]
        return "Non renseigné"

    def get_function_info(self, functions, type):
        if functions:
            return [
                {
                    type: self.get_mnemo(function['id_function']),
                    "Justification": function['justification'],
                    "Qualification": self.get_mnemo(function['id_qualification']),
                    "Connaissance": self.get_mnemo(function['id_knowledge'])
                }
                for function in functions
            ]
        return "Non renseigné"

    def get_int(self, nb):
        return nb if nb is not None else 'Non évalué'

    def get_hab_heritages(self, habs):
        if habs:
            return [
                {
                    "Corine Biotope": DB.session.query(Habref).filter(Habref.lb_code == hab['id_corine_bio']).filter(Habref.cd_typo == 22).one().lb_hab_fr,
                    "Cahier Habitats": DB.session.query(Habref).filter(Habref.cd_hab == hab['id_cahier_hab']).one().lb_hab_fr,
                    "Etat de préservation": self.get_mnemo(hab['id_preservation_state']),
                    "Recouvrement de la ZH (%)": "Non évalué" if hab["hab_cover"] == "999" else hab["hab_cover"]
                }
                for hab in habs
            ]
        return "Non renseigné"

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
