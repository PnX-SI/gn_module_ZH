from pypnusershub.tests.utils import set_logged_user

from flask import url_for

from geonature.tests.fixtures import *
from .fixtures import *


@pytest.mark.usefixtures("client_class")
class TestFilters:
    def test_get_zh_with_filter(self, users, zh_data, ref_geo_data):
        set_logged_user(self.client, users["admin_user"])

        response = self.client.post(
            url_for("pr_zh.get_zh"),
            json={
                "territories": {
                    "ZNIEFF2": [
                        {"code": "930012713", "name": "Clue de vergons - barre de pinadoux"}
                    ]
                }
            },
        )
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["items"]["features"]) == 1
