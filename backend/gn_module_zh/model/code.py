import sys

from geonature.utils.env import DB
from sqlalchemy.sql import func, select

from ..api_error import ZHApiError
from .zh import ZH
from .zh_schema import TZH, BibOrganismes, CorZhArea


class Code(ZH):
    def __init__(self, id_zh, id_org, zh_geom):
        self.id_zh = id_zh
        self.id_org = id_org
        self.zh_geom = zh_geom

    def get_departments(self):
        try:
            departments = CorZhArea.get_departments(self.id_zh)
            area = 0
            local_srid = DB.session.execute(func.Find_SRID("ref_geo", "l_areas", "geom")).scalar()
            my_geom = DB.session.execute(
                select(func.ST_Transform(func.ST_SetSRID(TZH.geom, 4326), local_srid)).where(
                    TZH.id_zh == self.id_zh
                )
            ).scalar_one()
            main_dep = None
            for dep in departments:
                dep_area = DB.session.scalar(
                    select(dep.LAreas.geom.ST_Intersection(my_geom).ST_Area())
                )
                if dep_area > area:
                    area = dep_area
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
        q_codes = DB.session.scalars(select(TZH).where(TZH.code.contains(base_code))).all()
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
