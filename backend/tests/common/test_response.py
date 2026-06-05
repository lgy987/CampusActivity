"""Success response tests"""

from app.common.response import success
from flask import Flask


class TestSuccessResponse:
    def setup_method(self):
        """Create Flask app context"""
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.ctx = self.app.app_context()
        self.ctx.push()
    
    def teardown_method(self):
        """Pop Flask app context"""
        self.ctx.pop()
    
    def test_success_with_data(self):
        response, status = success({"user_id": 1})
        assert status == 200
        data = response.get_json()
        assert data["code"] == 200
        assert data["data"] == {"user_id": 1}
    
    def test_success_with_message(self):
        response, status = success(message="Custom message")
        data = response.get_json()
        assert data["message"] == "Custom message"
    
    def test_success_defaults(self):
        response, status = success()
        data = response.get_json()
        assert data["code"] == 200
        assert data["message"] == "success"
        assert data["data"] is None
