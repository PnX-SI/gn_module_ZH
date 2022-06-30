import sys

from geonature.utils.env import DB
from sqlalchemy.sql import func

from ..api_error import ZHApiError
from .zh import ZH
from .zh_schema import *


class Code(ZH):
    def __init__(self, id_zh, id_org, zh_geom):
        self.id_zh = id_zh
        self.id_org = id_org
        self.zh_geom = zh_geom

    def get_departments(self):
        try:
            departments = CorZhArea.get_departments(self.id_zh)
            area = 0
            my_geom = (
                DB.session.query(func.ST_Transform(func.ST_SetSRID(TZH.geom, 4326), 2154))
                .filter(TZH.id_zh == self.id_zh)
                .one()[0]
            )
            main_dep = None
            for dep in departments:
                if DB.session.scalar(dep.LAreas.geom.ST_Intersection(my_geom).ST_Area()) > area:
                    area = DB.session.scalar(dep.LAreas.geom.ST_Intersection(my_geom).ST_Area())
                    main_dep = dep.LAreas.area_code
            if main_dep is None:
                raise ZHApiError(message="no_department", details="main_dep value is none")
            return main_dep
        except ZHApiError:
            raise
        except Exception as e:
            exc_type, value, tb = sys.exc_info()
            raise ZHApiError(
                message="set_geom_error", details=str(exc_type) + ": " + str(e.with_traceback(tb))
            )

    def get_organism(self):
        return BibOrganismes.get_abbrevation(self.id_org)

    def get_number(self):
        base_code = self.get_departments() + self.get_organism()
        q_codes = DB.session.query(TZH).filter(TZH.code.contains(base_code)).all()
        if q_codes:
            code_numbers = [int(zh.code.split(self.get_organism())[1]) for zh in q_codes]
            max_code = max(code_numbers)
        else:
            max_code = 0
        if max_code > 9999:
            raise ValueError("code error : zh_number_greater_than_9999")
        return max_code + 1

    def __repr__(self):
        return f"{self.get_departments()}{self.get_organism()}{self.get_number():04d}"
