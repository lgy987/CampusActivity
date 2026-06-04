from app.common.response import success
from flask import Flask

class TestSuccessResponse:
    def setup_method(self):
        """????????????"""
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.ctx = self.app.app_context()
        self.ctx.push()
    
    def teardown_method(self):
        """??????????"""
        self.ctx.pop()
    
    def test_success_with_data(self):
        response, status = success({"user_id": 1})
        assert status == 200
        # ?? get_json() ?? JSON ??
        data = response.get_json()
        assert data["code"] == 200
        assert data["data"] == {"user_id": 1}
    
    def test_success_with_message(self):
        response, status = success(message="?????")
        data = response.get_json()
        assert data["message"] == "?????"
    
    def test_success_defaults(self):
        response, status = success()
        data = response.get_json()
        assert data["code"] == 200
        assert data["message"] == "success"
        assert data["data"] is None
