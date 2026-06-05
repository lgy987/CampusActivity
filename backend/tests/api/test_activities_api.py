"""Activity API route tests"""

import pytest
from app import create_app


class TestActivitiesAPI:
    def setup_method(self):
        """Create test app"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_list_activities_public(self):
        """Test public activity list endpoint"""
        response = self.client.get("/activities")
        assert response.status_code == 200
    
    def test_get_activity_detail_not_found(self):
        """Test get non-existent activity returns 404"""
        response = self.client.get("/activities/99999")
        assert response.status_code == 404
    
    def test_create_activity_unauthorized(self):
        """Test create activity without authentication"""
        response = self.client.post("/organizer/activities", json={})
        assert response.status_code == 401
    
    def test_submit_activity_unauthorized(self):
        """Test submit activity without authentication"""
        response = self.client.post("/organizer/activities/1/submit")
        assert response.status_code == 401
    
    def test_update_activity_unauthorized(self):
        """Test update activity without authentication"""
        response = self.client.put("/organizer/activities/1", json={})
        assert response.status_code == 401
    
    def test_delete_activity_unauthorized(self):
        """Test delete activity without authentication"""
        response = self.client.delete("/organizer/activities/1")
        assert response.status_code == 401
    
    def test_get_my_activities_unauthorized(self):
        """Test get my activities without authentication"""
        response = self.client.get("/organizer/activities")
        assert response.status_code == 401
