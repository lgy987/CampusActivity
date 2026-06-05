"""Checkin API route tests"""

import pytest
from app import create_app


class TestCheckinAPI:
    def setup_method(self):
        """Create test app"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_get_checkin_code_unauthorized(self):
        """Test get checkin code without authentication"""
        response = self.client.get("/organizer/activities/1/checkin-code")
        assert response.status_code == 401
    
    def test_checkin_unauthorized(self):
        """Test checkin without authentication"""
        response = self.client.post("/activities/1/checkin", json={})
        assert response.status_code == 401
    
    def test_manual_checkin_unauthorized(self):
        """Test manual checkin without authentication"""
        response = self.client.post("/organizer/activities/1/manual-checkin", json={})
        assert response.status_code == 401
    
    def test_get_my_checkins_unauthorized(self):
        """Test get my checkins without authentication"""
        response = self.client.get("/user/checkins")
        assert response.status_code == 401
    
    def test_get_checkin_stats_unauthorized(self):
        """Test get checkin stats without authentication"""
        response = self.client.get("/organizer/activities/1/checkins")
        assert response.status_code == 401
