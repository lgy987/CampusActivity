from app.common.errors import BusinessError
from flask import Flask

class TestBusinessError:
    def setup_method(self):
        """????????????"""
        self.app = Flask(__name__)
        self.ctx = self.app.app_context()
        self.ctx.push()
    
    def teardown_method(self):
        """??????????"""
        self.ctx.pop()
    
    def test_error_with_defaults(self):
        error = BusinessError("????")
        response, status = error.to_response()
        assert status == 400
        data = response.get_json()
        assert data["code"] == 400
        assert data["message"] == "????"
    
    def test_error_with_custom_code(self):
        error = BusinessError("???", code=404, status_code=404)
        response, status = error.to_response()
        assert status == 404
        data = response.get_json()
        assert data["code"] == 404
    
    def test_error_with_401(self):
        error = BusinessError("???", code=401, status_code=401)
        response, status = error.to_response()
        assert status == 401
        data = response.get_json()
        assert data["code"] == 401
