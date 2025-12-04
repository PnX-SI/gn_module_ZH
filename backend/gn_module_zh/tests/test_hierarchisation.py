from pypnusershub.tests.utils import set_logged_user

from flask import url_for

from geonature.tests.fixtures import *
from .fixtures import *


def printobj(obj):
    print("\n\n\nObj => ")
    for key, value in obj.__dict__.items():
        # if not key.startswith('_'):  # Ignore les attributs privés
        print(f"{key}: {value}")
    print("\n\n\n")


@pytest.mark.usefixtures("client_class")
class TestHierarchisation:
    def test_hierarchisation(self, users, zh_data):

        from gn_module_zh.model.zh import ZH

        set_logged_user(self.client, users["self_user"])
        zh = ZH(zh_data.get("zh1").id_zh)
        printobj(zh_data.get("zh1"))

        db.session.execute("REFRESH MATERIALIZED VIEW pr_zh.rb_notes_summary;")

        response = self.client.get(url_for("pr_zh.get_hierarchy", id_zh=zh_data.get("zh1").id_zh))
        data = response.get_json()
        print("data:", data)
        assert response.status_code == 200
        # assert len(data["items"]["features"]) > 0

        # assert response.status_code == 200
        # data = response.get_json()
        # assert len(data["items"]["features"]) == 0
