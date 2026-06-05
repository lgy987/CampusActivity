"""Statistics API route tests"""

import pytest
from app import create_app


class TestStatisticsAPI:
    def setup_method(self):
        """Create test app"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_admin_statistics_unauthorized(self):
        """Test admin statistics without authentication"""
        response = self.client.get("/admin/statistics")
        assert response.status_code == 401
    
    def test_leaderboard_public(self):
        """Test leaderboard without authentication (public)"""
        response = self.client.get("/leaderboard")
        assert response.status_code == 200
