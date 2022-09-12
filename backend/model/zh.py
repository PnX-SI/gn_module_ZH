# instance de la BDD
from geonature.utils.env import DB

from .zh_schema import (
    TZH,
    CorLimList,
    CorZhLimFs,
    TFunctions,
    TActivity,
    TUrbanPlanningDocs,
    CorZhArea,
    InseeRegions,
    TActions,
    CorZhDocRange,
    TOwnership,
    TInflow,
    TOutflow,
    TInstruments,
    TManagementPlans,
    TManagementStructures,
    CorZhProtection,
    CorProtectionLevelType,
    CorImpactList,
    CorZhCorineCover,
    CorZhRef,
    CorZhCb,
    THabHeritage
)


class ZH(TZH):
    __abstract__ = True

    def __init__(self, id_zh):
        self.zh = DB.session.query(TZH).filter(TZH.id_zh == id_zh).one()

    @staticmethod
    def get_data_by_id(table_name, id_zh):
        return DB.session.query(table_name).filter(table_name.id_zh == id_zh).all()

    def get_id_lims(self):
        lim_list = CorLimList.get_lims_by_id(self.zh.id_lim_list)
        return {"id_lims": [id.id_lim for id in lim_list]}

    def get_id_lims_fs(self):
        lim_fs_list = ZH.get_data_by_id(CorZhLimFs, self.zh.id_zh)
        return {"id_lims_fs": [id.id_lim_fs for id in lim_fs_list]}

    def get_id_references(self):
        ref_list = CorZhRef.get_references_by_id(self.zh.id_zh)
        return {"id_references": [ref.as_dict() for ref in ref_list]}

    def get_cb_codes(self):
        corine_biotopes = ZH.get_data_by_id(CorZhCb, self.zh.id_zh)
        return {"cb_codes_corine_biotope": [cb_code.lb_code for cb_code in corine_biotopes]}

    def get_corine_landcovers(self):
        landcovers = ZH.get_data_by_id(CorZhCorineCover, self.zh.id_zh)
        return {"id_corine_landcovers": [landcover.id_cover for landcover in landcovers]}

    def get_activities(self):
        return {
            "activities": [
                {
                    "id_human_activity": activity.id_activity,
                    "id_localisation": activity.id_position,
                    "ids_impact": [
                        impact.id_cor_impact_types
                        for impact in CorImpactList.get_impacts_by_uuid(activity.id_impact_list)
                    ],
                    "remark_activity": activity.remark_activity,
                }
                for activity in ZH.get_data_by_id(TActivity, self.zh.id_zh)
            ]
        }

    def get_flows(self):
        q_outflows = ZH.get_data_by_id(TOutflow, self.zh.id_zh)
        q_inflows = ZH.get_data_by_id(TInflow, self.zh.id_zh)
        flows = [
            {
                "outflows": [
                    {
                        "id_outflow": flow.id_outflow,
                        "id_permanance": flow.id_permanance,
                        "topo": flow.topo,
                    }
                    for flow in q_outflows
                ]
            },
            {
                "inflows": [
                    {
                        "id_inflow": flow.id_inflow,
                        "id_permanance": flow.id_permanance,
                        "topo": flow.topo,
                    }
                    for flow in q_inflows
                ]
            },
        ]
        return {"flows": flows}

    def get_functions(self, category, is_eval=False):
        return {
            category.lower(): [
                {
                    "id_function": function.id_function,
                    "justification": function.justification,
                    "id_qualification": function.id_qualification,
                    "id_knowledge": function.id_knowledge,
                }
                for function in TFunctions.get_functions_by_id_and_category(
                    self.zh.id_zh, category, is_eval
                )
            ]
        }

    def get_hab_heritages(self):
        return {
            "hab_heritages": [
                {
                    "id_corine_bio": hab_heritage.id_corine_bio,
                    "id_cahier_hab": hab_heritage.id_cahier_hab,
                    "id_preservation_state": hab_heritage.id_preservation_state,
                    "hab_cover": hab_heritage.hab_cover,
                }
                for hab_heritage in ZH.get_data_by_id(THabHeritage, self.zh.id_zh)
            ]
        }

    def get_ownerships(self):
        return {
            "ownerships": [
                {"id_status": ownership.id_status, "remark": ownership.remark}
                for ownership in ZH.get_data_by_id(TOwnership, self.zh.id_zh)
            ]
        }

    def get_managements(self):
        q_management_structures = ZH.get_data_by_id(TManagementStructures, self.zh.id_zh)
        managements = []
        for management in q_management_structures:
            q_management_plans = (
                DB.session.query(TManagementPlans)
                .filter(TManagementPlans.id_structure == management.id_structure)
                .all()
            )
            plans = []
            if q_management_plans:
                for plan in q_management_plans:
                    plans.append(
                        {
                            "id_nature": plan.id_nature,
                            "plan_date": plan.plan_date.date().strftime("%d/%m/%Y"),
                            "duration": plan.duration,
                            "remark": plan.remark,
                        }
                    )
            managements.append({"structure": management.id_org, "plans": plans})
        return {"managements": managements}

    def get_instruments(self):
        return {
            "instruments": [
                {
                    "id_instrument": instrument.id_instrument,
                    "instrument_date": instrument.instrument_date.date().strftime("%d/%m/%Y")
                    if instrument.instrument_date
                    else None,
                }
                for instrument in ZH.get_data_by_id(TInstruments, self.zh.id_zh)
            ]
        }

    def get_protections(self):
        return {
            "protections": [
                DB.session.query(CorProtectionLevelType)
                .filter(CorProtectionLevelType.id_protection == protec)
                .one()
                .id_protection_status
                for protec in [
                    protection.id_protection
                    for protection in ZH.get_data_by_id(CorZhProtection, self.zh.id_zh)
                ]
            ]
        }

    def get_urban_docs(self):
        return {
            "urban_docs": [
                {
                    "id_area": urban_doc.id_area,
                    "id_doc_type": urban_doc.id_doc_type,
                    "id_cors": [
                        doc.id_cor
                        for doc in DB.session.query(CorZhDocRange)
                        .filter(CorZhDocRange.id_doc == urban_doc.id_doc)
                        .all()
                    ],
                    "remark": urban_doc.remark,
                }
                for urban_doc in ZH.get_data_by_id(TUrbanPlanningDocs, self.zh.id_zh)
            ]
        }

    def get_actions(self):
        return {
            "actions": [
                {
                    "id_action": action.id_action,
                    "id_priority_level": action.id_priority_level,
                    "remark": action.remark,
                }
                for action in ZH.get_data_by_id(TActions, self.zh.id_zh)
            ]
        }

    def get_fauna_nb(self):
        vertebrates = self.zh.as_dict()["nb_vertebrate_sp"]
        invertebrates = self.zh.as_dict()["nb_invertebrate_sp"]

        if vertebrates is None and invertebrates is None:
            return None
        try:
            vertebrates = int(vertebrates)
        except TypeError:
            vertebrates = 0
        try:
            invertebrates = int(invertebrates)
        except TypeError:
            invertebrates = 0
        return vertebrates + invertebrates

    def get_departments(self):
        return [
            {"code": dep.LAreas.area_code, "nom": dep.LAreas.area_name}
            for dep in CorZhArea.get_departments(self.zh.id_zh)
        ]

    def get_municipalities(self, query):
        return [
            {municipality.LiMunicipalities.insee_com: municipality.LiMunicipalities.nom_com}
            for municipality in query
        ]

    def get_regions(self, query):
        region_list = []
        for municipality in query:
            if municipality.LiMunicipalities.insee_reg not in region_list:
                region_list.append(municipality.LiMunicipalities.insee_reg)
        q_region = (
            DB.session.query(InseeRegions).filter(InseeRegions.insee_reg.in_(region_list)).all()
        )
        regions = [region.region_name for region in q_region]
        return regions

    def get_area(self):
        return {"area": self.zh.area}

    def get_geo_info(self):
        departments = self.get_departments()
        q_municipalities = CorZhArea.get_municipalities_info(self.zh.id_zh)
        municipalities = self.get_municipalities(q_municipalities)
        regions = self.get_regions(q_municipalities)
        return {
            "geo_info": {
                "departments": departments,
                "municipalities": municipalities,
                "regions": regions,
            }
        }

    def get_eval(self):
        eval = {}
        eval.update(self.get_functions("FONCTIONS_HYDRO", is_eval=True))
        eval.update(self.get_functions("FONCTIONS_BIO", is_eval=True))
        eval.update(self.get_functions("INTERET_PATRIM", is_eval=True))
        eval.update(self.get_functions("VAL_SOC_ECO", is_eval=True))
        eval.update(
            {
                "nb_flora_sp": self.zh.as_dict()["nb_flora_sp"],
                "nb_hab": self.zh.as_dict()["nb_hab"],
                "nb_fauna_sp": self.get_fauna_nb(),
                "total_hab_cover": self.zh.as_dict()["total_hab_cover"],
                "id_thread": self.zh.as_dict()["id_thread"],
                "id_diag_hydro": self.zh.as_dict()["id_diag_hydro"],
                "id_diag_bio": self.zh.as_dict()["id_diag_bio"],
            }
        )
        return eval

    def __repr__(self):
        zh = self.zh.get_geofeature()
        zh.properties.update(self.get_area())
        zh.properties.update(self.get_geo_info())
        zh.properties.update(self.get_id_lims())
        zh.properties.update(self.get_id_lims_fs())
        zh.properties.update(self.get_id_references())
        zh.properties.update(self.get_cb_codes())
        zh.properties.update(self.get_corine_landcovers())
        zh.properties.update(self.get_activities())
        zh.properties.update(self.get_flows())
        zh.properties.update(self.get_functions("FONCTIONS_HYDRO"))
        zh.properties.update(self.get_functions("FONCTIONS_BIO"))
        zh.properties.update(self.get_functions("INTERET_PATRIM"))
        zh.properties.update(self.get_functions("VAL_SOC_ECO"))
        zh.properties.update(self.get_hab_heritages())
        zh.properties.update(self.get_managements())
        zh.properties.update(self.get_actions())
        zh.properties.update(self.get_ownerships())
        zh.properties.update(self.get_instruments())
        zh.properties.update(self.get_protections())
        zh.properties.update(self.get_urban_docs())
        return zh
