"""????????? API ??"""

import pytest
from app import create_app

class TestAdminUsersAPI:
    def setup_method(self):
        """??????"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_list_users_unauthorized(self):
        """???????????"""
        response = self.client.get("/admin/users")
        assert response.status_code == 401
    
    def test_list_organizers_unauthorized(self):
        """????????????"""
        response = self.client.get("/admin/organizers")
        assert response.status_code == 401
    
    def test_list_admins_unauthorized(self):
        """????????????"""
        response = self.client.get("/admin/admins")
        assert response.status_code == 401
