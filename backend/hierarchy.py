#from abc import get_cache_token
import sys

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

    def __init__(self, rule_id, rb_id, id_qualif, knowledge, cor_rule_id):
        self.rule_id = rule_id
        self.rb_id = rb_id
        self.active = self.__is_rb_rule()
        self.cor_rule_id = cor_rule_id
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
            attribute_id_list = [getattr(item, 'attribute_id') for item in DB.session.query(
                TItems).filter(TItems.cor_rule_id == self.cor_rule_id).all()]
            if id_qualif not in attribute_id_list:
                raise ZHApiError(
                    message='wrong_qualif', details='zh qualif provided is not part of the qualif list defined in the river basin hierarchy rules', status_code=400)
            return id_qualif

    def __get_note(self):
        if self.active:
            type = self.__get_note_type()
            if type == 'single':
                return getattr(DB.session.query(TItems).filter(and_(TItems.attribute_id == self.id_qualif, TItems.cor_rule_id == self.cor_rule_id)).one(), 'note')
            else:
                return getattr(DB.session.query(TItems).filter(and_(TItems.attribute_id == self.id_qualif, TItems.cor_rule_id == self.cor_rule_id, TItems.note_type_id == self.knowledge)).one(), 'note')

    def __get_note_type(self):
        note_type_list = [getattr(item, 'note_type_id') for item in DB.session.query(
            TItems).filter(TItems.cor_rule_id == self.cor_rule_id).all()]
        if note_type_list[0] == 1:
            return 'single'
        else:
            return 'double'

    def __get_denominator(self):
        return max(getattr(val, 'note') for val in DB.session.query(TItems).filter(TItems.cor_rule_id == self.cor_rule_id).all())

    def __get_rule_name(self):
        try:
            DB.session.query(TRules, BibHierSubcategories).join(TRules).filter(
                TRules.rule_id == self.rule_id).one().BibHierSubcategories.label
        except NoResultFound:
            pass
        name = DB.session.query(TRules, BibHierCategories).join(TRules).filter(
            TRules.rule_id == self.rule_id).one().BibHierCategories.label
        return name

    def __str__(self):
        return {
            "active": self.active,
            "qualification": getattr(DB.session.query(TNomenclatures).filter(TNomenclatures.id_nomenclature == self.id_qualif).one(), 'label_default'),
            # "connaissance": self.knowledge,
            "nom sous-rubrique": self.__get_rule_name(),
            "note sous-rubrique": self.note,
            "denominateur sous-rubrique": self.denominator
        }


class Cat:

    def __init__(self, rb_id, abb_cat):
        self.rb_id: int = rb_id
        self.abb: str = abb_cat
        self.rule_ids: list[int] = self.__get_rules()
        self.items: list[Item]
        self.denominator: int
        self.note: int
        # self.active = Hierarchy.set_active(cat_id, type='cat')

    @property
    def items(self):
        return self.__items

    @property
    def denominator(self):
        return self.__denominator

    @items.setter
    def items(self, value):
        item_list = []
        for item in value:
            cor_rule_id = Cat.get_cor_rule_id(self.rb_id, item['rule_id'])
            item_list.append(
                Item(
                    rule_id=item['rule_id'],
                    rb_id=self.rb_id,
                    id_qualif=item['qualif_id'],
                    knowledge=item['id_knowledge'],
                    cor_rule_id=cor_rule_id
                ))
        self.__items = item_list

    @denominator.setter
    def denominator(self, value):
        self.__denominator = Hierarchy.get_denom(self.rb_id, value)

    def __get_rules(self):
        rule_ids = [getattr(item.TRules, 'rule_id') for item in DB.session.query(
            TRules, BibHierCategories).join(TRules).filter(BibHierCategories.abbreviation == self.abb).all()]
        return rule_ids

    def __get_name(self):
        # todo : return full name from abb
        return self.abb
        # self.__name = DB.session.query(TRules, BibHierCategories).join(
        #    TRules).filter(TRules.rule_id == value).one().BibHierCategories.label

    @staticmethod
    def get_note(value):
        return sum([getattr(item, 'note') for item in value])

    @staticmethod
    def get_cor_rule_id(rb_id, rule_id):
        return getattr(DB.session.query(CorRbRules).filter(and_(CorRbRules.rb_id == rb_id, CorRbRules.rule_id == rule_id)).one(), 'cor_rule_id')

    def __str__(self):
        return {
            "items": [item.__str__() for item in self.items],
            "note rubrique": self.note,
            "denominateur rubrique": self.denominator,
            "nom rubrique": self.__get_name()
        }


class Heritage:

    def __init__(self):
        hab: Item
        flora: Item
        vertebrates: Item
        invertebrates: Integer


class EcoCat:
    eco_cat: Item
    note: Integer


class HydroCat:

    def __init__(self):
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
        self.cat1_sdage = self.__set_sdage()
        self.cat2_heritage = self.__set_heritage()
        self.cat3_eco = self.__set_eco()
        # self.hydro_cat: HydroCat
        # self.soc_cat: SocioCat
        # self.note = self.__get_note()
        # self.denom = self.__get_denom()

    def __set_sdage(self):
        cat1 = Cat(self.rb_id, 'cat1')
        items = []
        for id in cat1.rule_ids:
            items = [
                {
                    "rule_id": id,
                    "qualif_id": self.__get_qualif(id),
                    "id_knowledge": self.__get_knowledge(id)
                }
            ]
        cat1.items = items
        #cat1.items = Sdage
        cat1.denominator = 'rub_sdage'
        cat1.note = cat1.get_note(cat1.items)
        cat1.name = 'cat1'  # todo : get full name from abb
        return cat1

    def __set_heritage(self):
        cat2 = Cat(self.rb_id, 'cat2')
        items = []
        for id in cat2.rule_ids:
            items.append(
                {
                    "rule_id": id,
                    "qualif_id": self.__get_qualif(id),
                    "id_knowledge": self.__get_knowledge(id)
                }
            )
        cat2.items = items
        cat2.denominator = 'rub_interet_pat'
        cat2.note = cat2.get_note(cat2.items)
        cat2.name = 'cat2'
        return cat2

    def __set_eco(self):
        cat3 = Cat(self.rb_id, 'cat3')
        items = []
        for id in cat3.rule_ids:
            items = [
                {
                    "rule_id": id,
                    "qualif_id": self.__get_qualif(id),
                    "id_knowledge": self.__get_knowledge(id)
                }
            ]
        cat3.items = items
        #cat1.items = Sdage
        cat3.denominator = 'rub_eco'
        cat3.note = cat3.get_note(cat3.items)
        cat3.name = 'cat3'  # todo : get full name from abb
        return cat3

    def __get_qualif(self, rule_id):
        if rule_id == 1:
            return getattr(TZH.get_tzh_by_id(self.id_zh), 'id_sdage')
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
        if rule_id == 6:
            # get nomenclature id of bio functions 61 and 62
            bio_type_id = getattr(DB.session.query(BibNomenclaturesTypes).filter(
                BibNomenclaturesTypes.mnemonique == 'FONCTIONS_BIO').one(), 'id_type')
            cd_nomenclature_list = ['61', '62']
            q_bio = DB.session.query(TFunctions, TNomenclatures).join(TNomenclatures, TNomenclatures.id_nomenclature == TFunctions.id_function).filter(
                TFunctions.id_zh == self.id_zh).filter(and_(TNomenclatures.id_type == bio_type_id, TNomenclatures.cd_nomenclature.in_(cd_nomenclature_list))).all()
            if not q_bio:
                raise ZHApiError(
                    message='no_eco_function', details='eco function evaluation not possible for this zh', status_code=400)
            hier_type_id = getattr(DB.session.query(BibNomenclaturesTypes).filter(
                BibNomenclaturesTypes.mnemonique == 'HIERARCHY').one(), 'id_type')
            if len(q_bio) == 1:
                # if 61 or 62 : continum ('reseau')
                return getattr(DB.session.query(TNomenclatures).filter(and_(TNomenclatures.id_type == hier_type_id, TNomenclatures.cd_nomenclature == 'res')).one(), 'id_nomenclature')
            elif len(q_bio) == 2:
                # if 61 and 62 : isolated
                return getattr(DB.session.query(TNomenclatures).filter(and_(TNomenclatures.id_type == hier_type_id, TNomenclatures.cd_nomenclature == 'iso')).one(), 'id_nomenclature')
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

    # def __get_rule_ids(self, cat_id):
    #    # todo: get list of subcat_ids from cat_id
    #    subcat_ids = []
    #    return subcat_ids

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

    def __str__(self):
        return {
            "cat1_sdage": self.cat1_sdage.__str__(),
            "cat2_heritage": self.cat2_heritage.__str__(),
            "cat3_eco": self.cat3_eco.__str__()
        }


"""
class Volet2:
    status_cat: SdageCat
    fct_state_cat: FctStateCat
    thread: ThreadCat
    note: Integer
    denom: Integer
"""


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

    @staticmethod
    def get_denom(rb_id, col_name):
        rb_name = DB.session.query(TRiverBasin).filter(
            TRiverBasin.id_rb == rb_id).one().name
        return getattr(DB.session.query(RbNotesSummary).filter(RbNotesSummary.bassin_versant == rb_name).one(), col_name)

    def __str__(self):
        return {
            "river_basin": DB.session.query(TRiverBasin).filter(TRiverBasin.id_rb == self.rb_id).one().name,
            "volet1": self.volet1.__str__()
            # "volet2": self.volet2.__str__(),
            # "note totale": self.global_note,
            # "note globale": self.final_note
        }
