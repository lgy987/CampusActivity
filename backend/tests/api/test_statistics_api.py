"""???? API ??"""

import pytest
from app import create_app

class TestStatisticsAPI:
    def setup_method(self):
        """??????"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_admin_statistics_unauthorized(self):
        """?????????????"""
        response = self.client.get("/admin/statistics")
        assert response.status_code == 401
    
    def test_leaderboard_public(self):
        """??????????????"""
        response = self.client.get("/leaderboard")
        assert response.status_code == 200
