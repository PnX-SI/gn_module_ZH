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


    def test_add_zh(self, users, zh_data):
        set_logged_user(self.client, users["self_user"])
        response = self.client.get(url_for("pr_zh.get_zh"))
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["items"]["features"]) > 0