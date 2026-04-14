from pypnusershub.tests.utils import set_logged_user

from flask import url_for

from geonature.tests.fixtures import *
from .fixtures import *


@pytest.mark.usefixtures("client_class")
class TestBdd:
    def test_no_zh(self, users):
        set_logged_user(self.client, users["self_user"])
        response = self.client.get(url_for("pr_zh.get_zh"))
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["items"]["features"]) == 0

    def test_get_zh(self, users, zh_data):
        set_logged_user(self.client, users["self_user"])
        response = self.client.get(url_for("pr_zh.get_zh"))
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["items"]["features"]) > 0

    def test_get_zh_by_id(self, users, zh_data):
        set_logged_user(self.client, users["self_user"])
        response = self.client.get(url_for("pr_zh.get_zh_by_id", id_zh=zh_data.get("zh1").id_zh))
        assert response.status_code == 200
        data = response.get_json()
        assert data["properties"]["id_zh"] == zh_data.get("zh1").id_zh
        assert data["properties"]["main_name"] == zh_data.get("zh1").main_name

    def test_get_zh_by_id_not_found(self, users):
        set_logged_user(self.client, users["self_user"])
        response = self.client.get(url_for("pr_zh.get_zh_by_id", id_zh=999999))
        # TODO: renvoie une 500 si la zone de protection n'existe pas ce serait préférable une 404
        assert response.status_code == 500

    def test_get_zh_by_id_no_auth(self, users, zh_data):
        set_logged_user(self.client, users["noright_user"])
        response = self.client.get(url_for("pr_zh.get_zh_by_id", id_zh=zh_data.get("zh1").id_zh))
        assert response.status_code == 403
        data = response.get_json()
        assert data["code"] == 403
        assert (
            data["description"]
            == f"User {users['noright_user'].get_id()} has no permissions to R in ZONES_HUMIDES"
        )
