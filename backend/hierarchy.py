# from abc import get_cache_token
import sys

import numpy as np

import sqlalchemy
from sqlalchemy import and_, distinct
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.sqltypes import INTEGER, Boolean, Integer

from pypnnomenclature.models import (
    BibNomenclaturesTypes
)

from geonature.utils.env import DB

from .api_error import ZHApiError
from .model.zh_schema import *
from .model.zh import ZH

import pdb


class Item:

    def __init__(self, id_zh, rb_id, abb, cd_nomenclature=None):
        self.id_zh = id_zh
        self.abb = abb
        self.rule_id = self.__get_rule_id(abb)
        self.rb_id = rb_id
        self.active = self.__is_rb_rule()
        self.cor_rule_id = self.__get_cor_rule_id()
        self.cd_nomenclatures = self.__get_cd_nomenclature()
        self.id_qualif = self.__check_qualif(self.__get_qualif())
        self.knowledge = self.__get_knowledge()
        self.note = self.__get_note()
        self.denominator = self.__get_denominator()

    def __get_rule_id(self, abb):
        try:
            return getattr(DB.session.query(TRules).filter(TRules.abbreviation == abb).one(), 'rule_id')
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_rule_id", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __is_rb_rule(self):
        try:
            q_rule = DB.session.query(CorRbRules).filter(
                and_(CorRbRules.rb_id == self.rb_id, CorRbRules.rule_id == self.rule_id)).first()
            if q_rule:
                return True
            return False
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __is_rb_rule", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_cor_rule_id(self):
        try:
            if self.active:
                return getattr(DB.session.query(CorRbRules).filter(and_(CorRbRules.rb_id == self.rb_id, CorRbRules.rule_id == self.rule_id)).one(), 'cor_rule_id')
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_cor_rule_id", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_cd_nomencs(self, mnemo_type):
        return [getattr(q_.TNomenclatures, 'cd_nomenclature') for q_ in DB.session.query(BibNomenclaturesTypes, TNomenclatures).join(TNomenclatures).filter(BibNomenclaturesTypes.mnemonique == 'STATUT_PROTECTION').all()]

    def __get_cd_nomenclature(self):
        if self.abb == 'protection':
            return ['41', '42', '51']
        if self.abb == 'epuration':
            return ['44']
        if self.abb == 'support':
            return ['43']
        if self.abb == 'eco':
            return ['61', '62']
        if self.abb == 'pedagogy':
            return ['4', '5', '6', '7', '8']
        if self.abb == 'production':
            return ['1', '2', '3']
        if self.abb == 'status':
            total = self.__get_cd_nomencs('STATUT_PROTECTION')
            nothing = ['0', '1']
            high = ['11', '13', '15', '16', '17', '31', '32', '33',
                    '34', '35', '36', '37', '38', '39', '40', '41', '100']
            low = sorted(np.setdiff1d(total, nothing+high))
            return {
                "nothing": nothing,
                "low": low,
                "high": high
            }

    def __get_qualif_sdage(self):
        try:
            return self.__get_qualif_val()
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_sdage", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_qualif_cat7(self):
        try:
            id_nomenc = self.__get_qualif_val()
            if getattr(DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == id_nomenc).one(), 'cd_nomenclature') == '0':
                return getattr(DB.session.query(BibNomenclaturesTypes, TNomenclatures).join(TNomenclatures, TNomenclatures.id_type == BibNomenclaturesTypes.id_type).filter(and_(BibNomenclaturesTypes.mnemonique == 'HIERARCHY', TNomenclatures.cd_nomenclature == 'NE')).one().TNomenclatures, 'id_nomenclature')
            if getattr(DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == id_nomenc).one(), 'cd_nomenclature') == '1':
                return getattr(DB.session.query(BibNomenclaturesTypes, TNomenclatures).join(TNomenclatures, TNomenclatures.id_type == BibNomenclaturesTypes.id_type).filter(and_(BibNomenclaturesTypes.mnemonique == 'HIERARCHY', TNomenclatures.cd_nomenclature == 'mauvais')).one().TNomenclatures, 'id_nomenclature')
            if getattr(DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == id_nomenc).one(), 'cd_nomenclature') == '2':
                return getattr(DB.session.query(BibNomenclaturesTypes, TNomenclatures).join(TNomenclatures, TNomenclatures.id_type == BibNomenclaturesTypes.id_type).filter(and_(BibNomenclaturesTypes.mnemonique == 'HIERARCHY', TNomenclatures.cd_nomenclature == 'moyen')).one().TNomenclatures, 'id_nomenclature')
            if getattr(DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == id_nomenc).one(), 'cd_nomenclature') == '3':
                return getattr(DB.session.query(BibNomenclaturesTypes, TNomenclatures).join(TNomenclatures, TNomenclatures.id_type == BibNomenclaturesTypes.id_type).filter(and_(BibNomenclaturesTypes.mnemonique == 'HIERARCHY', TNomenclatures.cd_nomenclature == 'bon')).one().TNomenclatures, 'id_nomenclature')
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_val", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_qualif_val(self):
        try:
            if self.abb == 'sdage':
                return self.__get_tzh_val('id_sdage')
            if self.abb == 'hab':
                return self.__get_tzh_val('nb_hab')
            if self.abb == 'flore':
                return self.__get_tzh_val('nb_flora_sp')
            if self.abb == 'vertebrates':
                return self.__get_tzh_val('nb_vertebrate_sp')
            if self.abb == 'invertebrates':
                return self.__get_tzh_val('nb_invertebrate_sp')
            if self.abb == 'hydro':
                return self.__get_tzh_val('id_diag_hydro')
            if self.abb == 'bio':
                return self.__get_tzh_val('id_diag_bio')
            if self.abb == 'thread':
                return self.__get_tzh_val('id_thread')
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_val", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_qualif_heritage(self):
        try:
            nb = self.__get_qualif_val()
            if not nb:
                nb = 0
            try:
                qualif = DB.session.query(CorRbRules, TItems, CorItemValue).join(TItems, TItems.cor_rule_id == CorRbRules.cor_rule_id).join(CorItemValue, TItems.attribute_id == CorItemValue.attribute_id).filter(
                    and_(CorRbRules.rb_id == self.rb_id, CorRbRules.rule_id == self.rule_id)).filter(and_(CorItemValue.val_min.__le__(nb), CorItemValue.val_max.__ge__(nb))).first()
            except Exception as e:
                exc_type, value, tb = sys.exc_info()
                raise ZHApiError(
                    message="__get_id_qualif_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
            return qualif.TItems.attribute_id
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_heritage", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_qualif_status(self):
        try:
            hier_id_type = self.__get_hier_nomenc_id()

            # get selected status cds
            q_status = self.__get_selected_status()

            # if nothing selected
            if not q_status:
                return getattr(DB.session.query(TNomenclatures).filter(and_(TNomenclatures.id_type ==
                                                                            hier_id_type, TNomenclatures.cd_nomenclature == '0')).one(), 'id_nomenclature')

            # get id_qualif
            for cd in q_status:
                if cd in self.cd_nomenclatures['high']:
                    return getattr(DB.session.query(TNomenclatures).filter(and_(TNomenclatures.id_type == hier_id_type, TNomenclatures.cd_nomenclature == 'fort')).one(), 'id_nomenclature')
                elif cd in self.cd_nomenclatures['nothing']:
                    return getattr(DB.session.query(TNomenclatures).filter(and_(TNomenclatures.id_type == hier_id_type, TNomenclatures.cd_nomenclature == '0')).one(), 'id_nomenclature')
                else:
                    return getattr(DB.session.query(TNomenclatures).filter(and_(TNomenclatures.id_type == hier_id_type, TNomenclatures.cd_nomenclature == 'faible')).one(), 'id_nomenclature')

        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_status", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_qualif_eco(self):
        try:
            # get selected functions
            q_functions = self.__get_selected_functions(
                'FONCTIONS_BIO', self.cd_nomenclatures)

            # get id_type of 'hierarchy' in TNomenclatures
            hier_type_id = self.__get_hier_nomenc_id()

            if len(q_functions) >= 1:
                # if 61 and/or 62 : get nomenc id of continum ('res')
                return getattr(DB.session.query(TNomenclatures).filter(and_(TNomenclatures.id_type == hier_type_id, TNomenclatures.cd_nomenclature == 'res')).one(), 'id_nomenclature')
            else:
                return getattr(DB.session.query(TNomenclatures).filter(and_(TNomenclatures.id_type == hier_type_id, TNomenclatures.cd_nomenclature == 'iso')).one(), 'id_nomenclature')
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_eco", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_selected_status(self):
        try:
            return [getattr(q_.TNomenclatures, 'cd_nomenclature') for q_ in DB.session.query(CorZhProtection, CorProtectionLevelType, TNomenclatures).join(CorProtectionLevelType, CorZhProtection.id_protection == CorProtectionLevelType.id_protection).join(TNomenclatures, TNomenclatures.id_nomenclature == CorProtectionLevelType.id_protection_status).all()]
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_selected_status", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_selected_functions(self, nomenc_type_mnemo, cd_ids):
        try:
            # get nomenclature id
            type_id = getattr(DB.session.query(BibNomenclaturesTypes).filter(
                BibNomenclaturesTypes.mnemonique == nomenc_type_mnemo).one(), 'id_type')
            # get selected functions
            q_ = DB.session.query(TFunctions, TNomenclatures).join(TNomenclatures, TNomenclatures.id_nomenclature == TFunctions.id_function).filter(
                TFunctions.id_zh == self.id_zh).filter(and_(TNomenclatures.id_type == type_id, TNomenclatures.cd_nomenclature.in_(cd_ids))).all()
            return q_
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_selected_functions", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_hier_nomenc_id(self):
        try:
            # get id_type of 'hierarchy' in TNomenclatures
            return getattr(DB.session.query(BibNomenclaturesTypes).filter(
                BibNomenclaturesTypes.mnemonique == 'HIERARCHY').one(), 'id_type')
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_hier_nomenc_id", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
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
            if function['mnemo'] == 'Non évaluée':
                res_list.insert(0, self.__get_count(
                    selected_ids, function['id']))
            if function['mnemo'] == 'Nulle à faible':
                res_list.insert(1, self.__get_count(
                    selected_ids, function['id']))
            if function['mnemo'] == 'Moyenne':
                res_list.insert(2, self.__get_count(
                    selected_ids, function['id']))
            if function['mnemo'] == 'Forte':
                res_list.insert(3, self.__get_count(
                    selected_ids, function['id']))
        res_strings = [str(res) for res in res_list]
        return "".join(res_strings)

    def __get_combination(self, mnemo_type):
        # get selected functions ids
        q_functions = self.__get_selected_functions(
            mnemo_type, self.cd_nomenclatures)
        selected_ids = [getattr(function.TFunctions, 'id_qualification')
                        for function in q_functions]

        # get function qualifications in TNomenclatures
        functions_qualif = [
            {
                "mnemo": nomenc.TNomenclatures.mnemonique,
                "id": nomenc.TNomenclatures.id_nomenclature
            } for nomenc in DB.session.query(BibNomenclaturesTypes, TNomenclatures).join(BibNomenclaturesTypes).filter(BibNomenclaturesTypes.mnemonique == 'FONCTIONS_QUALIF').all()
        ]

        # get qualif combination of selected functions
        combination = self.__set_combination(
            functions_qualif, selected_ids)

        return combination

    def __get_qualif_cat4_cat5(self):
        try:
            if self.abb in ['protection', 'epuration', 'support', 'pedagogy', 'production']:
                combination = self.__get_combination('FONCTIONS_HYDRO')
            if self.abb in ['pedagogy', 'production']:
                combination = self.__get_combination('VAL_SOC_ECO')
            # set id_qualif
            id_qualif = getattr(DB.session.query(TCorQualif).filter(
                TCorQualif.combination == combination).one(), 'id_qualification')
            return id_qualif
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_cat4_cat5", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_tzh_val(self, field):
        try:
            return getattr(DB.session.query(TZH).filter(TZH.id_zh == self.id_zh).one(), field)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_tzh_val", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_qualif(self):
        try:
            if self.active:
                if self.abb == 'sdage':
                    return self.__get_qualif_val()
                if self.abb in ['hab', 'flore', 'vertebrates', 'invertebrates']:
                    return self.__get_qualif_heritage()
                if self.abb == 'eco':
                    return self.__get_qualif_eco()
                if self.abb in ['protection', 'epuration', 'support', 'pedagogy', 'production']:
                    return self.__get_qualif_cat4_cat5()
                if self.abb == 'status':
                    return self.__get_qualif_status()
                if self.abb == 'management':
                    return self.__get_qualif_management()
                if self.abb in ['hydro', 'bio']:
                    return self.__get_qualif_cat7()
                if self.abb == 'thread':
                    return self.__get_qualif_val()
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_qualif_management(self):
        try:
            cd_id_nature_naturaliste = getattr(DB.session.query(BibNomenclaturesTypes, TNomenclatures).join(TNomenclatures, TNomenclatures.id_type == BibNomenclaturesTypes.id_type).filter(
                and_(BibNomenclaturesTypes.mnemonique == 'PLAN_GESTION', TNomenclatures.cd_nomenclature == '5')).one().TNomenclatures, 'id_nomenclature')
            selected_id_nature = [getattr(q_.TManagementPlans, 'id_nature') for q_ in DB.session.query(TManagementPlans, TManagementStructures).join(
                TManagementStructures, TManagementPlans.id_structure == TManagementStructures.id_structure).filter(TManagementStructures.id_zh == self.id_zh).all()]
            if cd_id_nature_naturaliste in selected_id_nature:
                # if id_nature == 'naturaliste' in selected plans : return
                return getattr(DB.session.query(TNomenclatures).filter(and_(TNomenclatures.id_type == self.__get_hier_nomenc_id(), TNomenclatures.cd_nomenclature == 'OUI')).one(), 'id_nomenclature')
            else:
                return getattr(DB.session.query(TNomenclatures).filter(and_(TNomenclatures.id_type == self.__get_hier_nomenc_id(), TNomenclatures.cd_nomenclature == 'NON')).one(), 'id_nomenclature')
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_management", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_knowledge(self):
        try:
            if self.active:
                if self.abb == 'hab':
                    is_carto = DB.session.query(TZH).filter(
                        TZH.id_zh == self.id_zh).one().is_carto_hab
                    if is_carto:
                        return 3
                    return 2
                elif self.abb in ['flore', 'vertebrates', 'invertebrates']:
                    is_other_inventory = DB.session.query(TZH).filter(
                        TZH.id_zh == self.id_zh).one().is_other_inventory
                    is_id_nature_plan_2 = self.__get_id_plan()
                    if is_other_inventory or is_id_nature_plan_2:
                        return 3
                    return 2
                elif self.abb == 'protection':
                    return self.__set_protection_knowledge()
                elif self.abb in ['epuration', 'support']:
                    try:
                        # return id_knowledge if abb function selected
                        return getattr(DB.session.query(TFunctions, BibNoteTypes).join(TFunctions, TFunctions.id_knowledge == BibNoteTypes.id_knowledge).filter(and_(TFunctions.id_zh == self.id_zh, TFunctions.id_qualification == self.id_qualif)).one().BibNoteTypes, 'note_id')
                    except:
                        pass
                    # if no function selected, return lacunaire ou nulle
                    return 2
                else:
                    return 1
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_knowledge", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __set_protection_knowledge(self):
        try:
            selected_functions = self.__get_selected_functions(
                'FONCTIONS_HYDRO', self.cd_nomenclatures)
            if len(selected_functions) in [0, 1]:
                # if 0 or 1 functions selected: low_knowlege
                return 2
            else:
                # if more than 1 functions selected :
                #   if 2 or more functions qualified as 'good knowledge': 'good knowledge'
                #   else: 'low knowledge'

                # get good knowldege id in TNomenclatures
                id_type = getattr(DB.session.query(BibNomenclaturesTypes).filter(
                    BibNomenclaturesTypes.mnemonique == 'FONCTIONS_CONNAISSANCE').one(), 'id_type')
                high_know_id = DB.session.query(TNomenclatures).filter(and_(
                    TNomenclatures.cd_nomenclature == '1', TNomenclatures.id_type == id_type)).one().id_nomenclature

                # count good knowledge ids in user selected functions
                selected_functions_ids = [
                    getattr(function.TFunctions, 'id_knowledge') for function in selected_functions]
                count = self.__get_count(selected_functions_ids, high_know_id)
                if count >= 2:
                    return 3
                else:
                    return 2
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __set_protection_knowledge", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_id_plan(self):
        q_plans = DB.session.query(TManagementStructures, TManagementPlans).join(TManagementPlans, TManagementStructures.id_structure ==
                                                                                 TManagementPlans.id_structure).filter(and_(TManagementStructures.id_zh == self.id_zh, TManagementPlans.id_nature == 2)).all()
        if q_plans:
            return True
        return False

    def __check_qualif(self, id_qualif):
        try:
            # todo: in db, add unique constraint on rb_id,rule_id in cor_rb_rules table
            if self.active:
                attribute_id_list = [getattr(item, 'attribute_id') for item in DB.session.query(
                    TItems).filter(TItems.cor_rule_id == self.cor_rule_id).all()]
                if id_qualif not in attribute_id_list:
                    raise ZHApiError(
                        message='wrong_qualif', details='zh qualif ({}) provided for {} rule is not part of the qualif list defined in the river basin hierarchy rules'.format(str(id_qualif), self.abb), status_code=400)
                return id_qualif
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __check_qualif", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.close()

    def __get_note(self):
        try:
            if self.active:
                return round(getattr(DB.session.query(TItems).filter(and_(TItems.attribute_id == self.id_qualif, TItems.cor_rule_id == self.cor_rule_id, TItems.note_type_id == self.knowledge)).one(), 'note'))
        except ZHApiError as e:
            raise ZHApiError(
                message=str(e.message), details=str(e.details), status_code=e.status_code)
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_note", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))

    def __get_denominator(self):
        try:
            if self.active:
                return max(getattr(val, 'note') for val in DB.session.query(TItems).filter(TItems.cor_rule_id == self.cor_rule_id).all())
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_denominator", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))

    def __get_rule_name(self):
        try:
            return DB.session.query(TRules, BibHierSubcategories).join(TRules).filter(
                TRules.rule_id == self.rule_id).one().BibHierSubcategories.label
        except NoResultFound:
            pass
        return DB.session.query(TRules, BibHierCategories).join(TRules).filter(
            TRules.rule_id == self.rule_id).one().BibHierCategories.label

    def __get_knowledge_mnemo(self):
        try:
            if self.active:
                if self.knowledge == 1:
                    return 'pas de connaissance pour cette sous-rubrique'
                else:
                    return getattr(DB.session.query(TNomenclatures, BibNoteTypes).join(BibNoteTypes, TNomenclatures.id_nomenclature == BibNoteTypes.id_knowledge).filter(BibNoteTypes.note_id == self.knowledge).one().TNomenclatures, 'mnemonique')
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_knowledge_mnemo", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))

    def __get_qualif_mnemo(self):
        try:
            if self.active:
                return getattr(DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == self.id_qualif).one(), 'label_default')
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Item class: __get_qualif_mnemo", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))

    def __str__(self):
        # if self.abb == 'hab':
        # pdb.set_trace()
        return {
            "active": self.active,
            "qualification": self.__get_qualif_mnemo(),
            "connaissance": self.__get_knowledge_mnemo(),
            "nom sous-rubrique": self.__get_rule_name(),
            "note sous-rubrique": self.note,
            "denominateur sous-rubrique": self.denominator
        }


class Cat:

    def __init__(self, id_zh, rb_id, abb_cat, cat_class):
        self.id_zh: int = id_zh
        self.rb_id: int = rb_id
        self.abb: str = abb_cat
        self.items: cat_class = cat_class(self.id_zh, self.rb_id)
        self.denominator: int
        self.note: int
        # self.active = Hierarchy.set_active(cat_id, type='cat')

    @property
    def denominator(self):
        return self.__denominator

    @denominator.setter
    def denominator(self, value):
        self.__denominator = Hierarchy.get_denom(self.rb_id, value)

    def __get_name(self):
        return getattr(DB.session.query(BibHierCategories).filter(BibHierCategories.abbreviation == self.abb).one(), 'label')

    @staticmethod
    def get_note(value):
        try:
            return sum(filter(None, [item['note sous-rubrique'] for item in value]))
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="Cat class: get_note", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))

    def __str__(self):
        return {
            "items": [item for item in self.items.__str__()],
            "note rubrique": self.note,
            "denominateur rubrique": self.denominator,
            "nom rubrique": self.__get_name()
        }


class Sdage:

    def __init__(self, id_zh, rb_id):
        self.sdage = Item(id_zh, rb_id, 'sdage')

    def __str__(self):
        items = []
        items.append(self.sdage.__str__())
        return items


class Heritage:

    def __init__(self, id_zh, rb_id):
        self.hab = Item(id_zh, rb_id, 'hab')
        self.flora = Item(id_zh, rb_id, 'flore')
        self.vertebrates = Item(id_zh, rb_id, 'vertebrates')
        self.invertebrates = Item(id_zh, rb_id, 'invertebrates')

    def __str__(self):
        items = []
        items.append(self.hab.__str__())
        items.append(self.flora.__str__())
        items.append(self.vertebrates.__str__())
        items.append(self.invertebrates.__str__())
        return items


class EcoFunction:

    def __init__(self, id_zh, rb_id):
        self.eco = Item(id_zh, rb_id, 'eco')

    def __str__(self):
        items = []
        items.append(self.eco.__str__())
        return items


class HydroFunction:

    def __init__(self, id_zh, rb_id):
        self.protection = Item(id_zh, rb_id, 'protection')
        self.epuration = Item(id_zh, rb_id, 'epuration')
        self.soutien = Item(id_zh, rb_id, 'support')

    def __str__(self):
        items = []
        items.append(self.protection.__str__())
        items.append(self.epuration.__str__())
        items.append(self.soutien.__str__())
        return items


class SocEco:

    def __init__(self, id_zh, rb_id):
        self.pedagogy = Item(id_zh, rb_id, 'pedagogy')
        self.production = Item(id_zh, rb_id, 'production')

    def __str__(self):
        items = []
        items.append(self.pedagogy.__str__())
        items.append(self.production.__str__())
        return items


class Status:

    def __init__(self, id_zh, rb_id):
        self.status = Item(id_zh, rb_id, 'status')
        self.management = Item(id_zh, rb_id, 'management')

    def __str__(self):
        items = []
        items.append(self.status.__str__())
        items.append(self.management.__str__())
        return items


class FctState:

    def __init__(self, id_zh, rb_id):
        self.hydro = Item(id_zh, rb_id, 'hydro')
        self.bio = Item(id_zh, rb_id, 'bio')

    def __str__(self):
        items = []
        items.append(self.hydro.__str__())
        items.append(self.bio.__str__())
        return items


class Thread:

    def __init__(self, id_zh, rb_id):
        self.thread = Item(id_zh, rb_id, 'thread')

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
        self.note += cat.note
        return cat


class Volet1(Volet):

    def __init__(self, id_zh, rb_id):
        self.volet = Volet(id_zh, rb_id, 'volet_1')
        self.cat1 = self.volet.set_cat('cat1', Sdage, 'rub_sdage')
        self.cat2 = self.volet.set_cat(
            'cat2', Heritage, 'rub_interet_pat')
        self.cat3 = self.volet.set_cat('cat3', EcoFunction, 'rub_eco')
        self.cat4 = self.volet.set_cat('cat4', HydroFunction, 'rub_hydro')
        self.cat5 = self.volet.set_cat('cat5',  SocEco, 'rub_socio')

    def __str__(self):
        return {
            "cat1_sdage": self.cat1.__str__(),
            "cat2_heritage": self.cat2.__str__(),
            "cat3_eco": self.cat3.__str__(),
            "cat4_hydro": self.cat4.__str__(),
            "cat5_soc_eco": self.cat5.__str__(),
            "note rubrique": self.volet.note,
            "denominateur rubrique": self.volet.denom
        }


class Volet2(Volet):

    def __init__(self, id_zh, rb_id):
        self.volet = Volet(id_zh, rb_id, 'volet_2')
        self.cat6 = self.volet.set_cat('cat6', Status, 'rub_statut')
        self.cat7 = self.volet.set_cat('cat7', FctState, 'rub_etat_fonct')
        self.cat8 = self.volet.set_cat('cat8', Thread, 'rub_menaces')

    def __str__(self):
        return {
            "cat6_status": self.cat6.__str__(),
            "cat7_fct_state": self.cat7.__str__(),
            "cat8_thread": self.cat8.__str__(),
            "note rubrique": self.volet.note,
            "denominateur rubrique": self.volet.denom
        }


class Hierarchy(ZH):

    def __init__(self, id_zh):
        self.id_zh = id_zh
        self.rb_id = self.__get_rb()
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
            return round(((self.global_note / self.total_denom) * 100), 2) if self.global_note != 0 else 0
        else:
            return None

    def __get_rb(self):
        try:
            q_rb = ZH.get_data_by_id(CorZhRb, self.id_zh)
            if not q_rb:
                raise ZHApiError(message='no_river_basin',
                                 details="zh is not part of any river basin", status_code=400)
            elif len(q_rb) > 1:
                # to do : if several rb intersect the zh polygon, calculate rb areas to determine which one is the main one
                # temp fix:
                raise ZHApiError(message='several_river_basin',
                                 details="zh is part of several river basins")
            else:
                return DB.session.query(CorZhRb, TRiverBasin).join(TRiverBasin).filter(CorZhRb.id_zh == self.id_zh).one().TRiverBasin.id_rb
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="get_rb_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        finally:
            DB.session.rollback()
            DB.session.close()

    @staticmethod
    def get_denom(rb_id, col_name):
        rb_name = DB.session.query(TRiverBasin).filter(
            TRiverBasin.id_rb == rb_id).one().name
        return getattr(DB.session.query(RbNotesSummary).filter(RbNotesSummary.bassin_versant == rb_name).one(), col_name)

    def __str__(self):
        return {
            "river_basin": DB.session.query(TRiverBasin).filter(TRiverBasin.id_rb == self.rb_id).one().name,
            "volet1": self.volet1.__str__(),
            "volet2": self.volet2.__str__(),
            "note globale": self.global_note,
            "denominateur": self.total_denom,
            "note finale": self.final_note
        }
