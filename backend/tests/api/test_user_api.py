"""???? API ??"""

import pytest
from app import create_app

class TestUserAPI:
    def setup_method(self):
        """??????"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_get_profile_unauthorized(self):
        """???????????"""
        response = self.client.get("/user/profile")
        assert response.status_code == 401
    
    def test_update_profile_unauthorized(self):
        """???????????"""
        response = self.client.put("/user/profile", json={})
        assert response.status_code == 401
    
    def test_update_avatar_unauthorized(self):
        """?????????"""
        response = self.client.post("/user/avatar")
        assert response.status_code == 401
    
    def test_reset_password_unauthorized(self):
        """?????????"""
        response = self.client.post("/user/reset-password", json={})
        assert response.status_code == 401
    
    def test_delete_account_unauthorized(self):
        """?????????"""
        response = self.client.delete("/user/account", json={})
        assert response.status_code == 401
