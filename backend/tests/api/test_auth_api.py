"""Auth API route tests"""

import pytest
from app import create_app


class TestAuthAPI:
    def setup_method(self):
        """Create test app"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_register_user_missing_fields(self):
        """Test register with empty body"""
        response = self.client.post("/auth/register/user", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert data["code"] == 400
    
    def test_register_user_invalid_student_id(self):
        """Test register with invalid student id"""
        data = {
            "student_id": "12345",
            "email": "test@example.com",
            "username": "testuser",
            "password": "Test123456",
            "confirm_password": "Test123456",
            "gender": "M",
            "college": "CS",
            "major": "CS",
            "grade": "2024"
        }
        response = self.client.post("/auth/register/user", json=data)
        assert response.status_code == 400
        data = response.get_json()
        assert data["code"] == 400
    
    def test_register_user_password_mismatch(self):
        """Test register with password mismatch"""
        data = {
            "student_id": "2024000001",
            "email": "test@example.com",
            "username": "testuser",
            "password": "Test123456",
            "confirm_password": "Different123",
            "gender": "M",
            "college": "CS",
            "major": "CS",
            "grade": "2024"
        }
        response = self.client.post("/auth/register/user", json=data)
        assert response.status_code == 400
        data = response.get_json()
        assert data["code"] == 400
    
    def test_login_missing_fields(self):
        """Test login with empty body"""
        response = self.client.post("/auth/login", json={})
        assert response.status_code == 400
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            "role": "user",
            "account": "nonexistent",
            "password": "wrong"
        }
        response = self.client.post("/auth/login", json=data)
        assert response.status_code == 401
    
    def test_logout(self):
        """Test logout"""
        response = self.client.post("/auth/logout")
        assert response.status_code == 200
        data = response.get_json()
        assert data["code"] == 200 or data["message"] == "success"
