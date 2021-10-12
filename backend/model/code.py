from sqlalchemy.sql import func

from geonature.utils.env import DB

from .zh_schema import *

from .zh import ZH


class Code(ZH):

    def __init__(self, id_zh, id_org, zh_geom):
        self.id_zh = id_zh
        self.id_org = id_org
        self.zh_geom = zh_geom

    def get_departments(self):
        departments = CorZhArea.get_departments(self.id_zh)
        area = 0
        my_geom = DB.session.query(func.ST_Transform(func.ST_SetSRID(
            TZH.geom, 4326), 2154)).filter(TZH.id_zh == self.id_zh).one()[0]
        for dep in departments:
            if DB.session.scalar(dep.LAreas.geom.ST_Intersection(my_geom).ST_Area()) > area:
                area = DB.session.scalar(
                    dep.LAreas.geom.ST_Intersection(my_geom).ST_Area())
                main_dep = dep.LAreas.area_code
        return main_dep

    def get_organism(self):
        return BibOrganismes.get_abbrevation(self.id_org)

    def get_number(self):
        number = DB.session.query(CorZhArea).join(LAreas, LAreas.id_area == CorZhArea.id_area).join(
            TZH, TZH.id_zh == CorZhArea.id_zh).filter(TZH.id_org == self.id_org, LAreas.area_code == self.get_departments()).count()
        if number > 9999:
            raise ValueError("code error : zh_number_greater_than_9999")
        return number+1

    def __repr__(self):
        return f'{self.get_departments()}-{self.get_organism()}-{self.get_number()}'
