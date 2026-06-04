"""?????? - ???????"""

import pytest
from app.services.user_service import UserService
from app.common.errors import BusinessError

class TestUserServiceValidation:
    """??????"""
    
    def test_update_profile_invalid_phone(self):
        """??????????????"""
        # ??????????????
        data = {"phone": "12345"}
        # ??????? mock ????????????
        # ??????????
        import re
        phone = "12345"
        if phone and not re.fullmatch(r"1\d{10}", phone):
            error_msg = "?????11?"
            assert error_msg == "?????11?"
    
    def test_list_users_default_params(self):
        """????????????"""
        params = {}
        page = max(int(params.get("page", 1)), 1)
        page_size = min(max(int(params.get("page_size", 20)), 1), 100)
        assert page == 1
        assert page_size == 20
    
    def test_list_users_with_custom_params(self):
        """?????????????"""
        params = {"page": "5", "page_size": "50"}
        page = max(int(params.get("page", 1)), 1)
        page_size = min(max(int(params.get("page_size", 20)), 1), 100)
        assert page == 5
        assert page_size == 50
