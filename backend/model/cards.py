from datetime import datetime

from sqlalchemy.sql.expression import true

from geonature.utils.env import DB
from geonature.core.ref_geo.models import LAreas

from .zh_schema import *
from .zh import ZH


class Card(ZH):

    def __init__(self, id_zh, type):
        self.id_zh = id_zh
        self.type = type
        self.__properties = self.get_properties()
        self.__eval = self.get_eval()

    def get_properties(self):
        return ZH(self.id_zh).__repr__()['properties']

    def get_eval(self):
        return ZH(self.id_zh).get_eval()

    def __repr__(self):
        return {
            "data": [
                {
                    "name": "name",
                    "label": "Nom usuel de la zone humide",
                    "value": self.__properties['main_name'],
                    "group": "identification"
                },
                {
                    "name": "other_name",
                    "label": "Autre nom",
                    "value": self.__properties['secondary_name'],
                    "group": "identification"
                },
                {
                    "name": "is_site_space",
                    "label": "Partie d'un ensemble",
                    "value": self.get_bool(self.__properties['is_id_site_space']),
                    "group": "identification"
                },
                {
                    "name": "site_space",
                    "label": "Nom du grand ensemble",
                    "value": TZH.get_site_space_name(self.__properties['id_site_space']) if self.__properties['is_id_site_space'] and self.__properties['id_site_space'] else "Ne fait pas partie d'un grand ensemble",
                    "group": "identification"
                },
                {
                    "name": "code",
                    "label": "Code de la zone humide",
                    "value": self.__properties['code'],
                    "group": "identification"
                },
                {
                    "name": "river_basin",
                    "label": "Bassin versant",
                    "value": self.get_river_basin(),
                    "group": "identification"
                },
                {
                    "name": "region",
                    "label": "Région",
                    "value": self.__properties['geo_info']['regions'],
                    "group": "localisation"
                },
                {
                    "name": "department",
                    "label": "Département",
                    "value": self.__properties['geo_info']['departments'],
                    "group": "localisation"
                },
                {
                    "name": "municipality",
                    "label": "Commune",
                    "value": self.get_communes_info(),
                    "group": "localisation"
                },
                {
                    "name": "author",
                    "label": "Auteur de la fiche",
                    "value": self.get_author(),
                    "group": "author"
                },
                {
                    "name": "author_edition",
                    "label": "Auteur des dernières modifications",
                    "value": self.get_author(type='co-author'),
                    "group": "author"
                },
                {
                    "name": "date",
                    "label": "Date d'établissement",
                    "value": datetime.strptime(self.__properties['create_date'], '%Y-%m-%d %H:%M:%S').date().strftime("%d/%m/%Y"),
                    "group": "author"
                },
                {
                    "name": "date_edition",
                    "label": "Date des dernières modifications",
                    "value": datetime.strptime(self.__properties['update_date'], '%Y-%m-%d %H:%M:%S.%f').date().strftime("%d/%m/%Y"),
                    "group": "author"
                },
                {
                    "name": "references",
                    "label": None,
                    "value": self.get_references(self.__properties['id_references']),
                    "group": "references"
                },
                {
                    "name": "used_crit1",
                    "label": "Critères utilisés",
                    "value": self.get_mnemo(self.__properties['id_lims']),
                    "group": "crit1"
                },
                {
                    "name": "remark_crit1",
                    "label": "Remarque",
                    "value": self.__properties['remark_lim'],
                    "group": "crit1"
                },
                {
                    "name": "used_crit2",
                    "label": "Critères utilisés",
                    "value": self.get_mnemo(self.__properties['id_lims_fs']),
                    "group": "crit2"
                },
                {
                    "name": "remark_crit2",
                    "label": "Remarque",
                    "value": self.__properties['remark_lim_fs'],
                    "group": "crit2"
                },
                {
                    "name": "typo_sdage",
                    "label": "Typologie SDAGE",
                    "value": self.get_mnemo(self.__properties['id_sdage']),
                    "group": "presentation"
                },
                {
                    "name": "typo_locale",
                    "label": "Typologie locale",
                    "value": self.get_mnemo(self.__properties['id_sage']),
                    "group": "presentation"
                },
                {
                    "name": "corine_biotope",
                    "label": "Corine Biotope",
                    "value": self.get_cb(self.__properties['cb_codes_corine_biotope']),
                    "group": "presentation"
                },
                {
                    "name": "remark_pres",
                    "label": "Remarques",
                    "value": self.__properties['remark_pres'],
                    "group": "presentation"
                },
                {
                    "name": "occupation",
                    "label": "Occupation des sols",
                    "value": self.get_mnemo(self.__properties['id_corine_landcovers']),
                    "group": "description"
                },
                {
                    "name": "activities",
                    "label": "Activités",
                    "value": self.get_activities(self.__properties['activities']),
                    "group": "usage"
                },
                {
                    "name": "thread",
                    "label": "Evaluation globale des menaces potentielles ou avérées",
                    "value": self.get_mnemo(self.__properties['id_thread']),
                    "group": "usage"
                },
                {
                    "name": "remark_usage",
                    "label": "Remarques",
                    "value": self.__properties['global_remark_activity'],
                    "group": "usage"
                }
            ],
            "tabs": [
                {
                    "name": "tab1",
                    "label": "1- Renseignements généraux"
                },
                {
                    "name": "tab2",
                    "label": "2- Délimitation de la zone humide et de l'espace de fonctionnalité"
                },
                {
                    "name": "tab3",
                    "label": "3- Description du bassin versant et de la zone humide"
                },
                {
                    "name": "tab4",
                    "label": "4- Fonctionnement de la zone humide"
                },
                {
                    "name": "tab5",
                    "label": "5- Fonctions écologiques, valeurs socio-écologiques, intérêt patrimonial"
                },
                {
                    "name": "tab6",
                    "label": "6- Statuts et gestion de la zone humide"
                },
                {
                    "name": "tab7",
                    "label": "7- Evaluation générale du site"
                }
            ],
            "groups": [
                {
                    "name": "identification",
                    "label": "Identification de la zone humide",
                    "tab": "tab1"
                },
                {
                    "name": "localisation",
                    "label": "Localisation de la zone humide",
                    "tab": "tab1"
                },
                {
                    "name": "author",
                    "label": "Auteur",
                    "tab": "tab1"
                },
                {
                    "name": "references",
                    "label": "Principales références bibliographiques",
                    "tab": "tab1"
                },
                {
                    "name": "crit1",
                    "label": "Critères de délimitation de la zone humide",
                    "tab": "tab2"
                },
                {
                    "name": "crit2",
                    "label": "Critère de délimitation de l'espace de fonctionnalité",
                    "tab": "tab2"
                },
                {
                    "name": "presentation",
                    "label": "Présentation de la zone humide et de ses milieux",
                    "tab": "tab3"
                },
                {
                    "name": "description",
                    "label": "Description de l'espace de fonctionnalité",
                    "tab": "tab3"
                },
                {
                    "name": "usage",
                    "label": "Usage et processus naturels",
                    "tab": "tab3"
                }
            ],
            "geometry": ZH(self.id_zh).__repr__()["geometry"]
        }

    def get_bool(self, bool):
        if bool:
            return 'Oui'
        return 'Non'

    def get_communes(self, communes):
        commune_insee = [k for k, v in [(k, v)
                                        for x in communes for (k, v) in x.items()]]
        commune_names = [v for k, v in [(k, v)
                                        for x in communes for (k, v) in x.items()]]
        return {
            "communes": commune_names,
            "code_insee": commune_insee
        }

    def get_communes_info(self):
        return [
            {
                "Commune": commune.LiMunicipalities.nom_com,
                "Code INSEE": commune.LiMunicipalities.insee_com,
                "Couverture ZH par rapport à la surface de la commune": str(commune.CorZhArea.cover) if commune.CorZhArea.cover is not None else 'Non renseigné'
            } for commune in CorZhArea.get_municipalities_info(self.id_zh)
        ]

    def get_river_basin(self):
        return [
            DB.session.query(TRiverBasin)
            .filter(TRiverBasin.id_rb == id).one().name
            for id in [rb.id_rb for rb in DB.session.query(CorZhRb).filter(CorZhRb.id_zh == self.id_zh).all()]
        ]

    def get_author(self, type='author'):
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

    def get_references(self, ref_list):
        if ref_list:
            return [
                {
                    "Titre du document": ref['title'],
                    "Auteurs": ref['authors'],
                    "Année de parution": ref['pub_year'],
                    "Bassins versants": 'en attente',
                    "Editeur": ref['editor'],
                    "Lieu": ref['editor_location']
                }
                for ref in ref_list
            ]
        return "Non renseigné"

    def get_mnemo(self, ids):
        if ids:
            if type(ids) is int:
                return DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == ids).one().label_default
            return [DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == id).one().label_default for id in ids]
        return "Non renseigné"

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
