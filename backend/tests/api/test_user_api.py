"""User API route tests"""

import pytest
from app import create_app


class TestUserAPI:
    def setup_method(self):
        """Create test app"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_get_profile_unauthorized(self):
        """Test get profile without authentication"""
        response = self.client.get("/user/profile")
        assert response.status_code == 401
    
    def test_update_profile_unauthorized(self):
        """Test update profile without authentication"""
        response = self.client.put("/user/profile", json={})
        assert response.status_code == 401
    
    def test_update_avatar_unauthorized(self):
        """Test update avatar without authentication"""
        response = self.client.post("/user/avatar")
        assert response.status_code == 401
    
    def test_reset_password_unauthorized(self):
        """Test reset password without authentication"""
        response = self.client.post("/user/reset-password", json={})
        assert response.status_code == 401
    
    def test_delete_account_unauthorized(self):
        """Test delete account without authentication"""
        response = self.client.delete("/user/account", json={})
        assert response.status_code == 401
