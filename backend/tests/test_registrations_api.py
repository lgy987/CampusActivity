"""???? API ??"""

import pytest
from app import create_app

class TestRegistrationsAPI:
    def setup_method(self):
        """??????"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_register_activity_unauthorized(self):
        """?????????"""
        response = self.client.post("/activities/1/register", json={})
        assert response.status_code == 401
    
    def test_cancel_registration_unauthorized(self):
        """?????????"""
        response = self.client.delete("/activities/1/register")
        assert response.status_code == 401
    
    def test_get_my_registrations_unauthorized(self):
        """?????????????"""
        response = self.client.get("/user/registrations")
        assert response.status_code == 401
    
    def test_get_activity_registrations_unauthorized(self):
        """???????????????"""
        response = self.client.get("/organizer/activities/1/registrations")
        assert response.status_code == 401
    
    def test_reject_registration_unauthorized(self):
        """?????????"""
        response = self.client.post("/organizer/registrations/1/reject", json={})
        assert response.status_code == 401
    
    def test_get_registration_stats_unauthorized(self):
        """?????????????"""
        response = self.client.get("/activities/1/registration-stats")
        assert response.status_code == 401
