import sys
from itertools import groupby
from werkzeug.exceptions import NotFound


from geonature.utils.env import DB
from pypnnomenclature.models import BibNomenclaturesTypes, TNomenclatures
from sqlalchemy import and_
from sqlalchemy.sql import select
from sqlalchemy.orm.exc import NoResultFound
from utils_flask_sqla.generic import GenericQuery

from .api_error import ZHApiError
from .constants import HIERARCHY_GLOBAL_MARKS
from .forms import post_note
from .geometry import get_main_rb
from .model.hierarchy import GlobalItem
from .model.zh import ZH
from .model.zh_schema import (
    TZH,
    BibHierCategories,
    BibHierSubcategories,
    BibNoteTypes,
    CorItemValue,
    CorProtectionLevelType,
    CorRbRules,
    CorRuleNomenc,
    CorZhProtection,
    CorZhRb,
    RbNotesSummary,
    TCorQualif,
    TFunctions,
    TItems,
    TManagementPlans,
    TManagementStructures,
    TRiverBasin,
    TRules,
)


class Item:
    def __init__(self, id_zh, rb_id, abb):
        self.id_zh = id_zh
        self.abb = abb
        self.rule_id = self.__get_rule_id(abb)
        self.rb_id = rb_id
        self.active = self.__is_rb_rule()
        self.cor_rule_id = self.__get_cor_rule_id()
        self.nomenc_ids = self.__get_nomenc_ids()
        self.qualif_id = self.__check_qualif(self.__get_qualif())
        self.knowledge = self.__get_knowledge()
        self.note = self.__set_note()
        self.denominator = self.__get_denominator()

    def __get_rule_id(self, abb):
        try:
            return getattr(
                DB.session.execute(select(TRules).where(TRules.abbreviation == abb)).scalar_one(),
                "rule_id",
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_rule_id",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __is_rb_rule(self):
        try:
            q_rule = DB.session.scalars(
                select(CorRbRules).where(
                    and_(
                        CorRbRules.rb_id == self.rb_id,
                        CorRbRules.rule_id == self.rule_id,
                    )
                )
            ).first()
            if q_rule:
                return True
            return False
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __is_rb_rule",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_cor_rule_id(self):
        try:
            if self.active:
                return getattr(
                    DB.session.execute(
                        select(CorRbRules).where(
                            and_(
                                CorRbRules.rb_id == self.rb_id,
                                CorRbRules.rule_id == self.rule_id,
                            )
                        )
                    ).scalar_one(),
                    "cor_rule_id",
                )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_cor_rule_id",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_id_nomenc(self, id_type: int, cd_nomenc: str) -> int:
        return getattr(
            DB.session.scalars(
                select(TNomenclatures).where(
                    and_(
                        TNomenclatures.id_type == id_type,
                        TNomenclatures.cd_nomenclature == cd_nomenc,
                    )
                )
            ).first(),
            "id_nomenclature",
            None,
        )

    def __get_nomencs(self, abb, cat=None):
        cat_id = self.__get_id_nomenc(self.__get_id_type("HIERARCHY"), cat)
        return [
            getattr(q_.CorRuleNomenc, "nomenc_id")
            for q_ in DB.session.execute(
                select(CorRuleNomenc, TRules)
                .join(TRules)
                .where(and_(TRules.abbreviation == abb, CorRuleNomenc.qualif_id == cat_id))
            ).all()
        ]

    def __get_nomenc_ids(self):
        if self.abb in [
            "protection",
            "epuration",
            "support",
            "eco",
            "pedagogy",
            "production",
        ]:
            return self.__get_nomencs(self.abb)
        elif self.abb == "status":
            return {
                "nothing": self.__get_nomencs(self.abb, "0"),
                "low": self.__get_nomencs(self.abb, "faible"),
                "high": self.__get_nomencs(self.abb, "fort"),
            }
        else:
            return None

    def __get_qualif_cat7(self):
        try:
            id_nomenc = self.__get_qualif_val()
            if (
                getattr(
                    DB.session.execute(
                        select(TNomenclatures).where(TNomenclatures.id_nomenclature == id_nomenc)
                    ).scalar_one(),
                    "cd_nomenclature",
                )
                == "0"
            ):
                return self.__get_id_nomenc(self.__get_id_type("HIERARCHY"), "NE")
            if (
                getattr(
                    DB.session.execute(
                        select(TNomenclatures).where(TNomenclatures.id_nomenclature == id_nomenc)
                    ).scalar_one(),
                    "cd_nomenclature",
                )
                == "1"
            ):
                return self.__get_id_nomenc(self.__get_id_type("HIERARCHY"), "bon")
            if (
                getattr(
                    DB.session.execute(
                        select(TNomenclatures).where(TNomenclatures.id_nomenclature == id_nomenc)
                    ).scalar_one(),
                    "cd_nomenclature",
                )
                == "2"
            ):
                return self.__get_id_nomenc(self.__get_id_type("HIERARCHY"), "moyen")
            if (
                getattr(
                    DB.session.execute(
                        select(TNomenclatures).where(TNomenclatures.id_nomenclature == id_nomenc)
                    ).scalar_one(),
                    "cd_nomenclature",
                )
                == "3"
            ):
                return self.__get_id_nomenc(self.__get_id_type("HIERARCHY"), "mauvais")
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_val",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_qualif_val(self):
        try:
            if self.abb == "sdage":
                return self.__get_tzh_val("id_sdage")
            if self.abb == "hab":
                return self.__get_tzh_val("nb_hab")
            if self.abb == "flore":
                return self.__get_tzh_val("nb_flora_sp")
            if self.abb == "vertebrates":
                return self.__get_tzh_val("nb_vertebrate_sp")
            if self.abb == "invertebrates":
                return self.__get_tzh_val("nb_invertebrate_sp")
            if self.abb == "hydro":
                return self.__get_tzh_val("id_diag_hydro")
            if self.abb == "bio":
                return self.__get_tzh_val("id_diag_bio")
            if self.abb == "thread":
                return self.__get_tzh_val("id_thread")
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_val",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_qualif_heritage(self):
        try:
            nb = self.__get_qualif_val()
            if not nb:
                nb = 0
            try:
                qualif = DB.session.execute(
                    select(CorRbRules, TItems, CorItemValue)
                    .join(TItems, TItems.cor_rule_id == CorRbRules.cor_rule_id)
                    .join(CorItemValue, TItems.attribute_id == CorItemValue.attribute_id)
                    .where(
                        and_(
                            CorRbRules.rb_id == self.rb_id,
                            CorRbRules.rule_id == self.rule_id,
                        )
                    )
                    .where(
                        and_(
                            CorItemValue.val_min.__le__(nb),
                            CorItemValue.val_max.__ge__(nb),
                        )
                    )
                ).first()
            except Exception as e:
                exc_type, value, tb = sys.exc_info()
                raise ZHApiError(
                    message="__get_qualif_id_error",
                    details=str(exc_type) + ": " + str(e.with_traceback(tb)),
                )
            return qualif.TItems.attribute_id
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_heritage",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_qualif_status(self):
        try:
            # get selected status cds
            q_status = self.__get_selected_status()

            # if nothing selected
            if not q_status:
                return self.__get_id_nomenc(self.__get_id_type("HIERARCHY"), "0")

            # get qualif_id :

            # if 'nothing' cd in values -> return 0
            for cd in q_status:
                if cd in self.nomenc_ids["nothing"]:
                    return self.__get_id_nomenc(self.__get_id_type("HIERARCHY"), "0")
            # if one 'high' cd is part of the cds -> return 'fort'
            for cd in q_status:
                if cd in self.nomenc_ids["high"]:
                    return self.__get_id_nomenc(self.__get_id_type("HIERARCHY"), "fort")
            # if no 'high' cd and no 'nothing' cd in values -> return 'faible'
            return self.__get_id_nomenc(self.__get_id_type("HIERARCHY"), "faible")

        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_status",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_qualif_eco(self):
        try:
            # get selected functions
            q_functions = self.__get_selected_functions(self.nomenc_ids)

            # get id_type of 'hierarchy' in TNomenclatures
            hier_type_id = self.__get_id_type("HIERARCHY")

            if len(q_functions) >= 1:
                # if 61 and/or 62 : get nomenc id of continum ('res')
                return getattr(
                    DB.session.execute(
                        select(TNomenclatures).where(
                            and_(
                                TNomenclatures.id_type == hier_type_id,
                                TNomenclatures.cd_nomenclature == "res",
                            )
                        )
                    ).scalar_one(),
                    "id_nomenclature",
                )
            else:
                return getattr(
                    DB.session.execute(
                        select(TNomenclatures).where(
                            and_(
                                TNomenclatures.id_type == hier_type_id,
                                TNomenclatures.cd_nomenclature == "iso",
                            )
                        )
                    ).scalar_one(),
                    "id_nomenclature",
                )
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_eco",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_selected_status(self):
        try:
            return [
                getattr(q_.TNomenclatures, "id_nomenclature")
                for q_ in DB.session.execute(
                    select(CorZhProtection, CorProtectionLevelType, TNomenclatures)
                    .join(
                        CorProtectionLevelType,
                        CorZhProtection.id_protection == CorProtectionLevelType.id_protection,
                    )
                    .join(
                        TNomenclatures,
                        TNomenclatures.id_nomenclature
                        == CorProtectionLevelType.id_protection_status,
                    )
                    .where(CorZhProtection.id_zh == self.id_zh)
                ).all()
            ]
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_selected_status",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_selected_functions(self, nomenc_ids):
        try:
            # get nomenclature id
            # type_id = getattr(DB.session.query(BibNomenclaturesTypes).filter(
            #     BibNomenclaturesTypes.mnemonique == nomenc_type_mnemo).one(), 'id_type')
            # get selected functions
            q_ = DB.session.execute(
                select(TFunctions, TNomenclatures)
                .join(
                    TNomenclatures,
                    TNomenclatures.id_nomenclature == TFunctions.id_function,
                )
                .where(TFunctions.id_zh == self.id_zh)
                .where(TNomenclatures.id_nomenclature.in_(nomenc_ids))
            ).all()
            return q_
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_selected_functions",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_id_type(self, mnemo):
        try:
            # get id_type in TNomenclatures
            return getattr(
                DB.session.execute(
                    select(BibNomenclaturesTypes).where(BibNomenclaturesTypes.mnemonique == mnemo)
                ).scalar_one(),
                "id_type",
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_id_type",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_count(self, id_list, function_id):
        count = 0
        for id in id_list:
            if id == function_id:
                count += 1
        return count

    def __set_combination(self, qualif_list, selected_ids):
        res_list = []
        for function in qualif_list:
            if function["mnemo"] == "Non évaluée":
                res_list.insert(0, self.__get_count(selected_ids, function["id"]))
            if function["mnemo"] == "Nulle à faible":
                res_list.insert(1, self.__get_count(selected_ids, function["id"]))
            if function["mnemo"] == "Moyenne":
                res_list.insert(2, self.__get_count(selected_ids, function["id"]))
            if function["mnemo"] == "Forte":
                res_list.insert(3, self.__get_count(selected_ids, function["id"]))
        res_strings = [str(res) for res in res_list]
        return "".join(res_strings)

    def __get_combination(self):
        # get selected functions ids
        q_functions = self.__get_selected_functions(self.nomenc_ids)
        selected_ids = [
            getattr(function.TFunctions, "id_qualification") for function in q_functions
        ]

        # get function qualifications in TNomenclatures
        functions_qualif = [
            {
                "mnemo": nomenc.TNomenclatures.mnemonique,
                "id": nomenc.TNomenclatures.id_nomenclature,
            }
            for nomenc in DB.session.execute(
                select(BibNomenclaturesTypes, TNomenclatures)
                .join(BibNomenclaturesTypes)
                .where(BibNomenclaturesTypes.mnemonique == "FONCTIONS_QUALIF")
                .order_by(TNomenclatures.id_nomenclature)
            ).all()
        ]

        # get qualif combination of selected functions
        combination = self.__set_combination(functions_qualif, selected_ids)

        return combination

    def __get_qualif_cat4_cat5(self):
        try:
            combination = self.__get_combination()
            # set qualif_id
            qualif_id = getattr(
                DB.session.scalars(
                    select(TCorQualif).where(TCorQualif.combination == combination)
                ).first(),
                "id_qualification",
            )
            return qualif_id
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_cat4_cat5",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_tzh_val(self, field):
        try:
            return getattr(
                DB.session.execute(select(TZH).where(TZH.id_zh == self.id_zh)).scalar_one(), field
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_tzh_val",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_qualif(self):
        try:
            if self.active:
                if self.abb == "sdage":
                    return self.__get_qualif_val()
                if self.abb in ["hab", "flore", "vertebrates", "invertebrates"]:
                    return self.__get_qualif_heritage()
                if self.abb == "eco":
                    return self.__get_qualif_eco()
                if self.abb in [
                    "protection",
                    "epuration",
                    "support",
                    "pedagogy",
                    "production",
                ]:
                    return self.__get_qualif_cat4_cat5()
                if self.abb == "status":
                    return self.__get_qualif_status()
                if self.abb == "management":
                    return self.__get_qualif_management()
                if self.abb in ["hydro", "bio"]:
                    return self.__get_qualif_cat7()
                if self.abb == "thread":
                    return self.__get_qualif_val()
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_qualif_management(self):
        try:
            cd_id_nature_naturaliste = getattr(
                DB.session.execute(
                    select(BibNomenclaturesTypes, TNomenclatures)
                    .join(
                        TNomenclatures,
                        TNomenclatures.id_type == BibNomenclaturesTypes.id_type,
                    )
                    .where(
                        and_(
                            BibNomenclaturesTypes.mnemonique == "PLAN_GESTION",
                            TNomenclatures.cd_nomenclature == "5",
                        )
                    )
                )
                .all()[0]
                .TNomenclatures,
                "id_nomenclature",
            )
            selected_id_nature = [
                getattr(q_.TManagementPlans, "id_nature")
                for q_ in DB.session.execute(
                    select(TManagementPlans, TManagementStructures)
                    .join(
                        TManagementStructures,
                        TManagementPlans.id_structure == TManagementStructures.id_structure,
                    )
                    .where(TManagementStructures.id_zh == self.id_zh)
                ).all()
            ]
            if cd_id_nature_naturaliste in selected_id_nature:
                # if id_nature == 'naturaliste' in selected plans : return
                return getattr(
                    DB.session.execute(
                        select(TNomenclatures).where(
                            and_(
                                TNomenclatures.id_type == self.__get_id_type("HIERARCHY"),
                                TNomenclatures.cd_nomenclature == "OUI",
                            )
                        )
                    ).scalar_one(),
                    "id_nomenclature",
                )
            else:
                return getattr(
                    DB.session.execute(
                        select(TNomenclatures).where(
                            and_(
                                TNomenclatures.id_type == self.__get_id_type("HIERARCHY"),
                                TNomenclatures.cd_nomenclature == "NON",
                            )
                        )
                    ).scalar_one(),
                    "id_nomenclature",
                )
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_management",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_knowledge(self):
        try:
            if self.active:
                if self.abb == "hab":
                    is_carto = (
                        DB.session.execute(select(TZH).where(TZH.id_zh == self.id_zh))
                        .scalar_one()
                        .is_carto_hab
                    )
                    if is_carto:
                        return 3
                    return 2
                elif self.abb in ["flore", "vertebrates", "invertebrates"]:
                    is_other_inventory = (
                        DB.session.execute(select(TZH).where(TZH.id_zh == self.id_zh))
                        .scalar_one()
                        .is_other_inventory
                    )
                    is_id_nature_plan_2 = self.__get_id_plan()
                    if is_other_inventory or is_id_nature_plan_2:
                        return 3
                    return 2
                elif self.abb == "protection":
                    return self.__set_protection_knowledge()
                elif self.abb in ["epuration", "support"]:
                    try:
                        # return id_knowledge if abb function selected
                        knowledge_id = (
                            DB.session.execute(
                                select(TFunctions.id_knowledge)
                                .where(
                                    and_(
                                        TFunctions.id_zh == self.id_zh,
                                        TFunctions.id_qualification == self.qualif_id,
                                    )
                                )
                                .where(TFunctions.id_function == CorRuleNomenc.nomenc_id)
                                .where(CorRuleNomenc.rule_id == self.rule_id)
                            )
                            .scalar_one()
                            .id_knowledge
                        )
                        return (
                            DB.session.execute(
                                select(BibNoteTypes).where(
                                    BibNoteTypes.id_knowledge == knowledge_id
                                )
                            )
                            .scalar_one()
                            .note_id
                        )
                    except:
                        pass
                    # if no function selected, return lacunaire ou nulle
                    return 2
                else:
                    return 1
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_knowledge",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __set_protection_knowledge(self):
        try:
            selected_functions = self.__get_selected_functions(self.nomenc_ids)
            if len(selected_functions) in [0, 1]:
                # if 0 or 1 functions selected: low_knowlege
                return 2
            else:
                # if more than 1 functions selected :
                #   if 2 or more functions qualified as 'good knowledge': 'good knowledge'
                #   else: 'low knowledge'

                # get good knowldege id in TNomenclatures
                id_type = self.__get_id_type("FONCTIONS_CONNAISSANCE")
                high_know_id = self.__get_id_nomenc(id_type, "1")

                # count good knowledge ids in user selected functions
                selected_functions_ids = [
                    getattr(function.TFunctions, "id_knowledge") for function in selected_functions
                ]
                count = self.__get_count(selected_functions_ids, high_know_id)
                if count >= 2:
                    return 3
                else:
                    return 2
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __set_protection_knowledge",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __get_id_plan(self):
        q_plans = DB.session.execute(
            select(TManagementStructures, TManagementPlans)
            .join(
                TManagementPlans,
                TManagementStructures.id_structure == TManagementPlans.id_structure,
            )
            .join(
                TNomenclatures,
                TNomenclatures.id_nomenclature == TManagementPlans.id_nature,
            )
            .where(
                and_(
                    TManagementStructures.id_zh == self.id_zh,
                    TNomenclatures.mnemonique == "Naturaliste",
                )
            )
        ).all()
        if q_plans:
            return True
        return False

    def __check_qualif(self, qualif_id):
        try:
            if self.active:
                attribute_id_list = [
                    getattr(item, "attribute_id")
                    for item in DB.session.scalars(
                        select(TItems).where(TItems.cor_rule_id == self.cor_rule_id)
                    ).all()
                ]
                if qualif_id not in attribute_id_list:
                    raise ZHApiError(
                        message="wrong_qualif",
                        details="zh qualif ({}) provided for {} rule is not part of the qualif list defined in the river basin hierarchy rules".format(
                            DB.session.execute(
                                select(TNomenclatures).where(
                                    TNomenclatures.id_nomenclature == qualif_id
                                )
                            )
                            .scalar_one()
                            .mnemonique,
                            self.abb,
                        ),
                        status_code=400,
                    )
                return qualif_id
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __check_qualif",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    def __set_note(self):
        try:
            if self.active:
                result = DB.session.execute(
                    select(TItems).where(
                        and_(
                            TItems.attribute_id == self.qualif_id,
                            TItems.cor_rule_id == self.cor_rule_id,
                            TItems.note_type_id == self.knowledge,
                        )
                    )
                ).scalar_one()
                note = round(result.note, 2)
                attribute_id = result.attribute_id
                note_type_id = result.note_type_id
                post_note(
                    self.id_zh,
                    self.cor_rule_id,
                    note,
                    attribute_id=attribute_id,
                    note_type_id=note_type_id,
                )
                DB.session.commit()
                return note
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message),
                details=str(e.details),
                status_code=e.status_code,
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __set_note",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )

    def __get_denominator(self):
        try:
            if self.active:
                return max(
                    getattr(val, "note")
                    for val in DB.session.scalars(
                        select(TItems).where(TItems.cor_rule_id == self.cor_rule_id)
                    ).all()
                )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_denominator",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )

    def __get_rule_name(self):
        try:
            return (
                DB.session.execute(
                    select(TRules, BibHierCategories)
                    .join(TRules)
                    .where(TRules.rule_id == self.rule_id)
                )
                .all()[0]
                .BibHierCategories.label.capitalize()
            )
        except NoResultFound:
            pass
        return (
            DB.session.execute(
                select(TRules, BibHierCategories)
                .join(TRules)
                .where(TRules.rule_id == self.rule_id)
            )
            .all()[0]
            .BibHierCategories.label.capitalize()
        )

    def __get_knowledge_mnemo(self):
        try:
            if self.active:
                if self.knowledge == 1:
                    return None
                else:
                    return getattr(
                        DB.session.execute(
                            select(TNomenclatures, BibNoteTypes)
                            .join(
                                BibNoteTypes,
                                TNomenclatures.id_nomenclature == BibNoteTypes.id_knowledge,
                            )
                            .where(BibNoteTypes.note_id == self.knowledge)
                        ).scalar_one(),
                        "mnemonique",
                    )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_knowledge_mnemo",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )

    def __get_qualif_mnemo(self):
        try:
            if self.active:
                return getattr(
                    DB.session.execute(
                        select(TNomenclatures).where(
                            TNomenclatures.id_nomenclature == self.qualif_id
                        )
                    ).scalar_one(),
                    "label_default",
                )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_mnemo",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )

    def __str__(self):
        return {
            "active": self.active,
            "qualification": self.__get_qualif_mnemo(),
            "knowledge": self.__get_knowledge_mnemo(),
            "name": self.__get_rule_name(),
            "note": (
                Hierarchy.get_str_note(self.note, self.denominator)
                if self.active
                else "Non paramétrée"
            ),
        }


class Cat:
    def __init__(self, id_zh, rb_id, abb_cat, cat_class):
        self.id_zh: int = id_zh
        self.rb_id: int = rb_id
        self.abb: str = abb_cat
        self.items: cat_class = cat_class(self.id_zh, self.rb_id)
        self.denominator: int
        self.note: int

    @property
    def denominator(self):
        return self.__denominator

    @denominator.setter
    def denominator(self, value):
        self.__denominator = Hierarchy.get_denom(self.rb_id, value)

    def __get_name(self):
        return getattr(
            DB.session.execute(
                select(BibHierCategories).where(BibHierCategories.abbreviation == self.abb)
            ).scalar_one(),
            "label",
        )

    @staticmethod
    def get_note(value):
        try:
            return round(
                sum(
                    filter(
                        None,
                        [
                            (
                                (float(item["note"].split("/")[0]))
                                if item["note"] is not None
                                else None
                            )
                            for item in value
                            if item["active"]
                        ],
                    )
                )
            )
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Cat class: get_note",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )

    def __str__(self):
        return {
            "items": [item for item in self.items.__str__()],
            "note": Hierarchy.get_str_note(self.note, self.denominator),
            "name": self.__get_name(),
        }


class Sdage:
    def __init__(self, id_zh, rb_id):
        self.sdage = Item(id_zh, rb_id, "sdage")

    def __str__(self):
        items = []
        items.append(self.sdage.__str__())
        return items


class Heritage:
    def __init__(self, id_zh, rb_id):
        self.hab = Item(id_zh, rb_id, "hab")
        self.flora = Item(id_zh, rb_id, "flore")
        self.vertebrates = Item(id_zh, rb_id, "vertebrates")
        self.invertebrates = Item(id_zh, rb_id, "invertebrates")

    def __str__(self):
        items = []
        items.append(self.hab.__str__())
        items.append(self.flora.__str__())
        items.append(self.vertebrates.__str__())
        items.append(self.invertebrates.__str__())
        return items


class EcoFunction:
    def __init__(self, id_zh, rb_id):
        self.eco = Item(id_zh, rb_id, "eco")

    def __str__(self):
        items = []
        items.append(self.eco.__str__())
        return items


class HydroFunction:
    def __init__(self, id_zh, rb_id):
        self.protection = Item(id_zh, rb_id, "protection")
        self.epuration = Item(id_zh, rb_id, "epuration")
        self.soutien = Item(id_zh, rb_id, "support")

    def __str__(self):
        items = []
        items.append(self.protection.__str__())
        items.append(self.epuration.__str__())
        items.append(self.soutien.__str__())
        return items


class SocEco:
    def __init__(self, id_zh, rb_id):
        self.pedagogy = Item(id_zh, rb_id, "pedagogy")
        self.production = Item(id_zh, rb_id, "production")

    def __str__(self):
        items = []
        items.append(self.pedagogy.__str__())
        items.append(self.production.__str__())
        return items


class Status:
    def __init__(self, id_zh, rb_id):
        self.status = Item(id_zh, rb_id, "status")
        self.management = Item(id_zh, rb_id, "management")

    def __str__(self):
        items = []
        items.append(self.status.__str__())
        items.append(self.management.__str__())
        return items


class FctState:
    def __init__(self, id_zh, rb_id):
        self.hydro = Item(id_zh, rb_id, "hydro")
        self.bio = Item(id_zh, rb_id, "bio")

    def __str__(self):
        items = []
        items.append(self.hydro.__str__())
        items.append(self.bio.__str__())
        return items


class Thread:
    def __init__(self, id_zh, rb_id):
        self.thread = Item(id_zh, rb_id, "thread")

    def __str__(self):
        items = []
        items.append(self.thread.__str__())
        return items


class Volet:
    def __init__(self, id_zh, rb_id, view_abb):
        self.id_zh = id_zh
        self.rb_id = rb_id
        self.note = 0
        self.denom = Hierarchy.get_denom(self.rb_id, view_abb)

    def set_cat(self, cat_abb, cat_class, view_abb):
        cat = Cat(self.id_zh, self.rb_id, cat_abb, cat_class)
        cat.denominator = view_abb
        cat.note = cat.get_note(cat.items.__str__())
        if cat.note is not None:
            self.note += cat.note
        return cat

    def __str__(self):
        return Hierarchy.get_str_note(self.note, self.denom)


class Volet1(Volet):
    def __init__(self, id_zh, rb_id):
        self.volet = Volet(id_zh, rb_id, "volet_1")
        self.cat1 = self.volet.set_cat("cat1", Sdage, "rub_sdage")
        self.cat2 = self.volet.set_cat("cat2", Heritage, "rub_interet_pat")
        self.cat3 = self.volet.set_cat("cat3", EcoFunction, "rub_eco")
        self.cat4 = self.volet.set_cat("cat4", HydroFunction, "rub_hydro")
        self.cat5 = self.volet.set_cat("cat5", SocEco, "rub_socio")

    def __str__(self):
        return {
            "cat1_sdage": self.cat1.__str__(),
            "cat2_heritage": self.cat2.__str__(),
            "cat3_eco": self.cat3.__str__(),
            "cat4_hydro": self.cat4.__str__(),
            "cat5_soc_eco": self.cat5.__str__(),
            "note": self.volet.__str__(),
        }


class Volet2(Volet):
    def __init__(self, id_zh, rb_id):
        self.volet = Volet(id_zh, rb_id, "volet_2")
        self.cat6 = self.volet.set_cat("cat6", Status, "rub_statut")
        self.cat7 = self.volet.set_cat("cat7", FctState, "rub_etat_fonct")
        self.cat8 = self.volet.set_cat("cat8", Thread, "rub_menaces")

    def __str__(self):
        return {
            "cat6_status": self.cat6.__str__(),
            "cat7_fct_state": self.cat7.__str__(),
            "cat8_thread": self.cat8.__str__(),
            "note": self.volet.__str__(),
        }


class Hierarchy(ZH):
    def __init__(self, id_zh):
        self.id_zh = id_zh
        self.rb_id = self.__get_rb()
        if not self.rb_id:
            raise NotFound("The ZH is not in a river basin")
        self.is_rules = self.__check_if_rules()
        self.volet1 = Volet1(self.id_zh, self.rb_id)
        self.volet2 = Volet2(self.id_zh, self.rb_id)
        self.total_denom = self.__get_total_denom()
        self.global_note = self.__get_global_note()
        self.final_note = self.__get_final_note()

    def __get_total_denom(self):
        return sum(filter(None, [self.volet1.volet.denom, self.volet2.volet.denom]))

    def __get_global_note(self):
        return sum(filter(None, [self.volet1.volet.note, self.volet2.volet.note]))

    def __get_final_note(self):
        if self.total_denom != 0:
            return (
                round(((self.global_note / self.total_denom) * 100), 1)
                if self.global_note != 0
                else 0
            )
        else:
            return None

    def __get_rb(self):
        q_rb = ZH.get_data_by_id(CorZhRb, self.id_zh)
        if not q_rb:
            return None
        if len(q_rb) > 1:
            return get_main_rb(q_rb)
        return (
            DB.session.execute(
                select(CorZhRb, TRiverBasin).join(TRiverBasin).where(CorZhRb.id_zh == self.id_zh)
            )
            .scalar_one()
            .id_rb
        )

    def __check_if_rules(self):
        try:
            if not DB.session.scalars(
                select(CorRbRules).where(CorRbRules.rb_id == self.rb_id)
            ).first():
                raise ZHApiError(
                    message="no_rb_rules",
                    details="no existing rules for the river basin",
                )
        except ZHApiError:
            raise
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Hierarchy class: __get_is_rules",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )
        finally:
            DB.session.close()

    @staticmethod
    def get_denom(rb_id, col_name):
        rb_name = (
            DB.session.execute(select(TRiverBasin).where(TRiverBasin.id_rb == rb_id))
            .scalar_one()
            .name
        )
        return getattr(
            DB.session.execute(
                select(RbNotesSummary).where(RbNotesSummary.bassin_versant == rb_name)
            ).scalar_one(),
            col_name,
        )

    @staticmethod
    def get_str_note(note, denominator):
        try:
            if (note is None) or (denominator is None):
                return None
            return str(note) + "/" + str(denominator)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Hierarchy class: get_str_note",
                details=str(exc_type) + ": " + str(e.with_traceback(tb)),
            )

    def as_dict(self):
        return {
            "river_basin_name": DB.session.execute(
                select(TRiverBasin).where(TRiverBasin.id_rb == self.rb_id)
            )
            .scalar_one()
            .name,
            "volet1": self.volet1.__str__(),
            "volet2": self.volet2.__str__(),
            "global_note": Hierarchy.get_str_note(self.global_note, self.total_denom),
            "final_note": Hierarchy.get_str_note(self.final_note, 100),
        }


def get_all_hierarchy_fields(id_rb: int):
    query = GenericQuery(
        DB=DB,
        tableName="all_rb_rules",
        schemaName="pr_zh",
        filters={"id_rb": id_rb, "orderby": "name"},
        limit=100000,
    )

    results = query.return_query()

    notes = [note for note in results.get("items", [])]

    if len(notes) == 0:
        return notes

    # TODO: to optimize with recursive function
    fields = {"categories": []}
    for name, items in groupby(notes, lambda note: note["volet"]):
        temp = {"name": name, "subcategory": []}
        for subname, subitems in groupby(list(items), lambda note: note["rubrique"]):
            temp["subcategory"].append({"name": subname, "subcategory": []})
            for subsubname, subsubitems in groupby(
                list(subitems), lambda note: note["sousrubrique"]
            ):
                temp["subcategory"][-1]["subcategory"].append(
                    {"name": subsubname, "subcategory": []}
                )
        fields["categories"].append(temp)

    for mark in HIERARCHY_GLOBAL_MARKS:
        for i, attribut in enumerate(mark.attributes):
            notes.append(
                GlobalItem(
                    volet=mark.volet,
                    rubrique=mark.rubrique,
                    sous_rubrique=mark.sous_rubrique,
                    attribut=attribut,
                    id_attribut=i,
                ).dict()
            )
    fields["items"] = notes
    return fields
