"""Category API route tests"""

import pytest
from app import create_app


class TestCategoriesAPI:
    def setup_method(self):
        """Create test app"""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
    
    def test_get_categories(self):
        """Test get categories list"""
        response = self.client.get("/categories")
        assert response.status_code == 200
        data = response.get_json()
        assert data["code"] == 200
        assert "data" in data
