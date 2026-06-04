"""??????? API ??"""

import pytest
from app import create_app

class TestNotificationsAPI:
    def setup_method(self):
        """??????"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_list_notifications_unauthorized(self):
        """???????????"""
        response = self.client.get("/notifications")
        assert response.status_code == 401
    
    def test_mark_notification_read_unauthorized(self):
        """???????????"""
        response = self.client.put("/notifications/1/read")
        assert response.status_code == 401
    
    def test_create_announcement_unauthorized(self):
        """?????????"""
        response = self.client.post("/admin/announcements", json={})
        assert response.status_code == 401
    
    def test_list_announcements_public(self):
        """????????????????"""
        response = self.client.get("/announcements")
        assert response.status_code == 200
    
    def test_delete_announcement_unauthorized(self):
        """?????????"""
        response = self.client.delete("/admin/announcements/1")
        assert response.status_code == 401
