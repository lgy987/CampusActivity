"""Admin activity API route tests"""

import pytest
from app import create_app


class TestAdminActivitiesAPI:
    def setup_method(self):
        """Create test app"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_list_review_activities_unauthorized(self):
        """Test list review activities without authentication"""
        response = self.client.get("/admin/activities")
        assert response.status_code == 401
    
    def test_get_admin_activity_detail_unauthorized(self):
        """Test get admin activity detail without authentication"""
        response = self.client.get("/admin/activities/1")
        assert response.status_code == 401
    
    def test_review_activity_unauthorized(self):
        """Test review activity without authentication"""
        response = self.client.put("/admin/activities/1/review", json={})
        assert response.status_code == 401
    
    def test_remove_activity_unauthorized(self):
        """Test remove activity without authentication"""
        response = self.client.put("/admin/activities/1/remove", json={})
        assert response.status_code == 401
