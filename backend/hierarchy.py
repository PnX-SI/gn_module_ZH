from abc import get_cache_token
import sys

import sqlalchemy
from sqlalchemy import and_, distinct
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.sqltypes import INTEGER, Boolean, Integer

from geonature.utils.env import DB

from .api_error import ZHApiError
from .model.zh_schema import *
from .model.zh import ZH

import pdb


class Item:

    def __init__(self, rule_id, rb_id, id_qualif, knowledge):
        self.rule_id = rule_id
        self.rb_id = rb_id
        self.active = self.__is_rb_rule()
        self.cor_rule_id = self.__get_cor_rule_id()
        self.id_qualif = self.__set_qualif(id_qualif)
        self.knowledge = knowledge
        self.note = self.__get_note()
        self.denominator = self.__get_denominator()

    def __is_rb_rule(self):
        q_rule = DB.session.query(CorRbRules).filter(
            and_(CorRbRules.rb_id == self.rb_id, CorRbRules.rule_id == self.rule_id)).first()
        if q_rule:
            return True
        return False

    def __set_qualif(self, id_qualif):
        # todo: in db, add unique constraint on rb_id,rule_id in cor_rb_rules table
        if self.active:
            attribute_id_list = [item.attribute_id for item in DB.session.query(
                TItems).filter(TItems.cor_rule_id == self.cor_rule_id).all()]
            if id_qualif not in attribute_id_list:
                raise ZHApiError(
                    message='wrong_qualif', details='zh qualif provided is not part of the qualif list defined in the river basin hierarchy rules', status_code=400)
            return id_qualif

    def __get_note(self):
        if self.active:
            type = self.__get_note_type()
            if type == 'single':
                return DB.session.query(TItems).filter(and_(TItems.attribute_id == self.id_qualif, TItems.cor_rule_id == self.cor_rule_id)).one().note
            else:
                return DB.session.query(TItems).filter(and_(TItems.attribute_id == self.id_qualif, TItems.cor_rule_id == self.cor_rule_id, TItems.note_type_id == self.knowledge)).one().note

    def __get_cor_rule_id(self):
        return DB.session.query(CorRbRules).filter(and_(CorRbRules.rb_id == self.rb_id, CorRbRules.rule_id == self.rule_id)).one().cor_rule_id

    def __get_note_type(self):
        note_type_list = [item.note_type_id for item in DB.session.query(
            TItems).filter(TItems.cor_rule_id == self.cor_rule_id).all()]
        if note_type_list[0] == 1:
            return 'single'
        else:
            return 'double'

    def __get_denominator(self):
        return max(val.note for val in DB.session.query(TItems).filter(TItems.cor_rule_id == self.cor_rule_id).all())

    # def __get_rule_name(self):
    #    pdb.set_trace()
    #    name = DB.session.query(TRules, BibHierSubcategories).join(
    #        TRules.subcat_id == BibHierSubcategories.subcat_id).filter(TRules.rule_id == self.rule_id).one().BibHierSubcategories.label
    #    if not name:
    #        return 'pas de sous-rubrique'
    #    return name

    def __str__(self):
        return {
            "active": self.active,
            "qualification": DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == self.id_qualif).one().label_default,
            # "connaissance": self.knowledge,
            # "nom sous-rubrique": self.__get_rule_name(),
            "note sous-rubrique": self.note,
            "denominateur sous-rubrique": self.denominator
        }


class Cat:

    def __init__(self, rb_id, id_zh, cat_class):
        self.id_zh = id_zh
        self.rb_id = rb_id
        self.items = cat_class(self.rb_id, self.id_zh)
        # self.active = Hierarchy.set_active(cat_id, type='cat')
        self.note = self.__get_note()

    def __get_note(self):
        return sum([item['note sous-rubrique'] for item in self.items.__str__()])

    def __str__(self):
        return {
            "items": self.items.__str__(),
            "note rubrique": self.note,
            "denominateur rubrique": self.items.denominator,
        }


class SdageCat:

    def __init__(self, rb_id, id_zh):
        self.id_zh = id_zh
        self.rb_id = rb_id
        self.sdage = self.__set_sdage()
        self.denominator = self.__get_denom()

    def __set_sdage(self):
        # id = DB.session.query(TRules, BibHierCategories).join(BibHierCategories, TRules.cat_id == BibHierCategories.cat_id).filter(
        #    BibHierCategories.label == 'type de zone humide').one().TRules.rule_id
        rule_id = 1
        return Item(rule_id, self.rb_id, self.__get_id_sdage(), 1)

    def __get_id_sdage(self):
        return TZH.get_tzh_by_id(self.id_zh).id_sdage

    def __get_denom(self):
        rb_name = DB.session.query(TRiverBasin).filter(
            TRiverBasin.id_rb == self.rb_id).one().name
        return DB.session.query(RbNotesSummary).filter(RbNotesSummary.bassin_versant == rb_name).one().rub_sdage

    def __repr__(self):
        items = []
        items.append(self.sdage.__str__())
        return items


class HeritageCat:

    def __init__(self, rb_id, id_zh):
        self.id_zh = id_zh
        self.rb_id = rb_id
        self.humid_hab = self.__set_humid_hab()
        self.flora = self.__set_flora()
        self.vertebrates = self.__set_vertebrates()
        self.invertebrates = self.__set_invertebrates()
        self.denominator = self.__get_denom()

    def __set_humid_hab(self):
        # id = DB.session.query(TRules, BibHierCategories).join(BibHierSubcategories, TRules.cat_id == BibHierSubcategories.cat_id).filter(
        #    BibHierSubcategories.label == 'habitats patrimoniaux humides').one().TRules.rule_id
        rule_id = 2
        id_knowledge = self.__get_knowledge(rule_id)
        return Item(rule_id, self.rb_id, self.__get_id_qualif(rule_id), id_knowledge)

    def __set_flora(self):
        # id = DB.session.query(TRules, BibHierCategories).join(BibHierSubcategories, TRules.cat_id == BibHierSubcategories.cat_id).filter(
        #    BibHierSubcategories.label == 'flore patrimoniale').one().TRules.rule_id
        rule_id = 3
        id_knowledge = self.__get_knowledge(rule_id)
        return Item(rule_id, self.rb_id, self.__get_id_qualif(rule_id), id_knowledge)

    def __set_vertebrates(self):
        # id = DB.session.query(TRules, BibHierCategories).join(BibHierSubcategories, TRules.cat_id == BibHierSubcategories.cat_id).filter(
        #    BibHierSubcategories.label == 'faune patrimoniale - vertébrés').one().TRules.rule_id
        rule_id = 4
        id_knowledge = self.__get_knowledge(rule_id)
        return Item(rule_id, self.rb_id, self.__get_id_qualif(rule_id), id_knowledge)

    def __set_invertebrates(self):
        # id = DB.session.query(TRules, BibHierCategories).join(BibHierSubcategories, TRules.cat_id == BibHierSubcategories.cat_id).filter(
        #    BibHierSubcategories.label == 'faune patrimoniale - vertébrés').one().TRules.rule_id
        rule_id = 5
        id_knowledge = self.__get_knowledge(rule_id)
        return Item(rule_id, self.rb_id, self.__get_id_qualif(rule_id), id_knowledge)

    def __get_knowledge(self, rule_id):
        if rule_id == 2:
            is_carto = DB.session.query(TZH).filter(
                TZH.id_zh == self.id_zh).one().is_carto_hab
            if is_carto:
                return 2
            return 3
        elif rule_id in [3, 4, 5]:
            is_other_inventory = DB.session.query(TZH).filter(
                TZH.id_zh == self.id_zh).one().is_other_inventory
            is_id_nature_plan_2 = self.__get_id_plan()
            if is_other_inventory or is_id_nature_plan_2:
                return 2
            return 3
        else:
            return 1

    def __get_id_plan(self):
        q_plans = DB.session.query(TManagementStructures, TManagementPlans).join(TManagementPlans, TManagementStructures.id_structure ==
                                                                                 TManagementPlans.id_structure).filter(and_(TManagementStructures.id_zh == self.id_zh, TManagementPlans.id_nature == 2)).all()
        if q_plans:
            return True
        return False

    def __get_denom(self):
        rb_name = DB.session.query(TRiverBasin).filter(
            TRiverBasin.id_rb == self.rb_id).one().name
        return DB.session.query(RbNotesSummary).filter(RbNotesSummary.bassin_versant == rb_name).one().rub_interet_pat

    def __get_id_qualif(self, rule_id):
        nb = None
        if rule_id == 2:
            nb = DB.session.query(TZH).filter(
                TZH.id_zh == self.id_zh).one().nb_hab
        if rule_id == 3:
            nb = DB.session.query(TZH).filter(
                TZH.id_zh == self.id_zh).one().nb_flora_sp
        if rule_id == 4:
            nb = DB.session.query(TZH).filter(
                TZH.id_zh == self.id_zh).one().nb_vertebrate_sp
        if rule_id == 5:
            nb = DB.session.query(TZH).filter(
                TZH.id_zh == self.id_zh).one().nb_invertebrate_sp
        if not nb:
            nb = 0
        try:
            qualif = DB.session.query(CorRbRules, TItems, CorItemValue).join(TItems, TItems.cor_rule_id == CorRbRules.cor_rule_id).join(CorItemValue, TItems.attribute_id == CorItemValue.attribute_id).filter(
                and_(CorRbRules.rb_id == self.rb_id, CorRbRules.rule_id == rule_id)).filter(and_(CorItemValue.val_min.__le__(nb), CorItemValue.val_max.__ge__(nb))).first()
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="__get_id_qualif_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))
        return qualif.TItems.attribute_id

    def __repr__(self):
        items = []
        items.append(self.humid_hab.__str__())
        items.append(self.flora.__str__())
        items.append(self.vertebrates.__str__())
        items.append(self.invertebrates.__str__())
        return items


class EcoCat:
    eco_cat: Item
    note: Integer


class HydroCat:
    protection: Item
    epuration: Item
    soutien: Item
    note: Integer


class SocioCat:
    loisirs: Item
    production: Item
    note: Integer


class StatusCat:
    status: Item
    management: Item
    note: Integer


class FctStateCat:
    hydro: Item
    bio: Item
    note: Integer


class ThreadCat:
    thread: Item
    note: Integer


class Volet1:

    def __init__(self, id_zh, rb_id):
        self.id_zh = id_zh
        self.rb_id = rb_id
        self.cat1_sdage = Cat(self.rb_id, self.id_zh, SdageCat)
        self.cat2_heritage = Cat(self.rb_id, self.id_zh, HeritageCat)
        # self.eco_cat: EcoCat
        # self.hydro_cat: HydroCat
        # self.soc_cat: SocioCat
        # self.note = self.__get_note()
        # self.denom = self.__get_denom()

    def __str__(self):
        return {
            "cat1_sdage": self.cat1_sdage.__str__(),
            "cat2_heritage": self.cat2_heritage.__str__()
        }


class Volet2:
    status_cat: SdageCat
    fct_state_cat: FctStateCat
    thread: ThreadCat
    note: Integer
    denom: Integer


class Hierarchy(ZH):

    def __init__(self, id_zh):
        self.id_zh = id_zh
        self.rb_id = self.__get_rb()
        self.volet1 = Volet1(self.id_zh, self.rb_id)
        # self.volet2: Volet2(self.id_zh, self.rb_id)
        # self.global_note: Integer
        # self.final_note: Integer

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

    def __str__(self):
        return {
            "river_basin": DB.session.query(TRiverBasin).filter(TRiverBasin.id_rb == self.rb_id).one().name,
            "volet1": self.volet1.__str__()
            # "volet2": self.volet2.__str__(),
            # "note totale": self.global_note,
            # "note globale": self.final_note
        }
