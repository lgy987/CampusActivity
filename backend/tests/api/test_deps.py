"""?? API ????"""

import pytest
from app.api.deps import get_json_data, get_current_user, require_auth, require_role
from app.common.errors import BusinessError


class TestGetJsonData:
    def test_get_json_data_empty(self, app):
        """??? JSON ??"""
        with app.test_request_context(json={}):
            with pytest.raises(BusinessError) as exc:
                get_json_data()
            assert exc.value.code == 400
    
    def test_get_json_data_valid(self, app):
        """???? JSON ??"""
        with app.test_request_context(json={"key": "value"}):
            data = get_json_data()
            assert data == {"key": "value"}


class TestGetCurrentUser:
    def test_no_auth_header(self, app):
        """??????"""
        with app.test_request_context():
            role, user_id = get_current_user()
            assert role is None
            assert user_id is None
    
    def test_invalid_auth_header(self, app):
        """???????"""
        with app.test_request_context(headers={"Authorization": "Invalid"}):
            role, user_id = get_current_user()
            assert role is None
            assert user_id is None


class TestRequireAuth:
    def test_require_auth_without_token(self, app):
        """???????"""
        with app.test_request_context():
            @require_auth()
            def test_func():
                return "success"
            
            with pytest.raises(BusinessError) as exc:
                test_func()
            assert exc.value.code == 401
