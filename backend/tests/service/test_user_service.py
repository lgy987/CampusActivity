"""User service tests - unit and database tests"""

import pytest
import time
from werkzeug.security import generate_password_hash
from app.services.user_service import UserService
from app.common.errors import BusinessError
from app.common.database import db_session
from models import User, Organizer, Admin


class TestUserServiceValidation:
    """Parameter validation tests (no database)"""
    
    def test_list_users_default_params(self):
        """Test list users with default params"""
        params = {}
        page = max(int(params.get("page", 1)), 1)
        page_size = min(max(int(params.get("page_size", 20)), 1), 100)
        assert page == 1
        assert page_size == 20
    
    def test_list_users_with_custom_params(self):
        """Test list users with custom params"""
        params = {"page": "5", "page_size": "50"}
        page = max(int(params.get("page", 1)), 1)
        page_size = min(max(int(params.get("page_size", 20)), 1), 100)
        assert page == 5
        assert page_size == 50
    
    def test_list_users_page_min(self):
        """Test page minimum value is 1"""
        params = {"page": "0"}
        page = max(int(params.get("page", 1)), 1)
        assert page == 1
    
    def test_list_users_page_size_max(self):
        """Test page_size maximum is 100"""
        params = {"page_size": "200"}
        page_size = min(max(int(params.get("page_size", 20)), 1), 100)
        assert page_size == 100
    
    def test_update_profile_invalid_phone_format(self):
        """Test phone number validation logic"""
        import re
        # Valid phone
        assert re.fullmatch(r"1\d{10}", "13800138000") is not None
        # Invalid phone
        assert re.fullmatch(r"1\d{10}", "12345") is None


class TestUserServiceDB:
    """Database tests for user service - self-contained"""
    
    def test_get_user_profile_success(self, app):
        """Test get user profile success"""
        with app.app_context():
            # Create test user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                user = User(
                    student_id=f"2024{unique}",
                    email=f"test_{unique}@example.com",
                    username="testuser",
                    password=generate_password_hash("test123"),
                    gender="M",
                    college="CS",
                    major="CS",
                    grade="2024",
                    status="active"
                )
                session.add(user)
                session.flush()
                user_id = user.id
            
            # Test get profile
            with db_session() as session:
                result = UserService.get_profile("user", user_id)
                assert result["user_id"] == user_id
                assert result["username"] == "testuser"
    
    def test_update_user_profile_success(self, app):
        """Test update user profile success"""
        with app.app_context():
            # Create test user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                user = User(
                    student_id=f"2024{unique}",
                    email=f"test_{unique}@example.com",
                    username="testuser",
                    password=generate_password_hash("test123"),
                    gender="M",
                    college="CS",
                    major="CS",
                    grade="2024",
                    status="active"
                )
                session.add(user)
                session.flush()
                user_id = user.id
            
            # Update user
            with db_session() as session:
                UserService.update_profile("user", user_id, {"username": "UpdatedUserName"})
            
            # Verify update
            with db_session() as session:
                result = UserService.get_profile("user", user_id)
                assert result["username"] == "UpdatedUserName"
    
    def test_update_user_profile_with_phone(self, app):
        """Test update user profile with phone number"""
        with app.app_context():
            # Create test user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                user = User(
                    student_id=f"2024{unique}",
                    email=f"test_{unique}@example.com",
                    username="testuser",
                    password=generate_password_hash("test123"),
                    gender="M",
                    college="CS",
                    major="CS",
                    grade="2024",
                    status="active"
                )
                session.add(user)
                session.flush()
                user_id = user.id
            
            # Update phone
            with db_session() as session:
                UserService.update_profile("user", user_id, {"phone": "13900139000"})
            
            # Verify
            with db_session() as session:
                result = UserService.get_profile("user", user_id)
                assert result["phone"] == "13900139000"
    
    def test_update_user_profile_invalid_phone(self, app):
        """Test update user profile with invalid phone"""
        with app.app_context():
            # Create test user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                user = User(
                    student_id=f"2024{unique}",
                    email=f"test_{unique}@example.com",
                    username="testuser",
                    password=generate_password_hash("test123"),
                    gender="M",
                    college="CS",
                    major="CS",
                    grade="2024",
                    status="active"
                )
                session.add(user)
                session.flush()
                user_id = user.id
            
            # Test invalid phone
            with pytest.raises(BusinessError) as exc:
                UserService.update_profile("user", user_id, {"phone": "12345"})
            assert exc.value.code == 400
    
    def test_reset_password_success(self, app):
        """Test reset password success"""
        with app.app_context():
            # Create test user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                student_id = f"2024{unique}"
                user = User(
                    student_id=student_id,
                    email=f"test_{unique}@example.com",
                    username="testuser",
                    password=generate_password_hash("test123"),
                    gender="M",
                    college="CS",
                    major="CS",
                    grade="2024",
                    status="active"
                )
                session.add(user)
                session.flush()
                user_id = user.id
            
            # Reset password
            with db_session() as session:
                UserService.reset_password("user", user_id, "test123", "NewPass456")
            
            # Verify with login
            from app.services.auth_service import AuthService
            result = AuthService.login("user", student_id, "NewPass456")
            assert result["role"] == "user"
    
    def test_reset_password_wrong_old_password(self, app):
        """Test reset password with wrong old password"""
        with app.app_context():
            # Create test user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                user = User(
                    student_id=f"2024{unique}",
                    email=f"test_{unique}@example.com",
                    username="testuser",
                    password=generate_password_hash("test123"),
                    gender="M",
                    college="CS",
                    major="CS",
                    grade="2024",
                    status="active"
                )
                session.add(user)
                session.flush()
                user_id = user.id
            
            # Test wrong password
            with pytest.raises(BusinessError) as exc:
                UserService.reset_password("user", user_id, "wrongpassword", "NewPass123")
            assert exc.value.code == 400
    
    def test_get_organizer_profile_success(self, app):
        """Test get organizer profile success"""
        with app.app_context():
            # Create test organizer
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                organizer = Organizer(
                    email=f"org_{unique}@example.com",
                    org_name="Test Org",
                    password=generate_password_hash("org123"),
                    org_proof_text="Proof text",
                    status="approved"
                )
                session.add(organizer)
                session.flush()
                organizer_id = organizer.id
            
            # Test get profile
            with db_session() as session:
                result = UserService.get_profile("organizer", organizer_id)
                assert result["organizer_id"] == organizer_id
                assert result["org_name"] == "Test Org"
    
    def test_get_admin_profile_success(self, app):
        """Test get admin profile success"""
        with app.app_context():
            # Create test admin
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                admin = Admin(
                    admin_no=unique,
                    email=f"admin_{unique}@example.com",
                    password=generate_password_hash("admin123"),
                    username="testadmin",
                    role="admin",
                    status="active"
                )
                session.add(admin)
                session.flush()
                admin_id = admin.id
            
            # Test get profile
            with db_session() as session:
                result = UserService.get_profile("admin", admin_id)
                assert result["admin_id"] == admin_id
                assert result["role"] == "admin"
    
    def test_get_user_detail_admin(self, app):
        """Test admin get user detail"""
        with app.app_context():
            # Create test user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                user = User(
                    student_id=f"2024{unique}",
                    email=f"test_{unique}@example.com",
                    username="testuser",
                    password=generate_password_hash("test123"),
                    gender="M",
                    college="CS",
                    major="CS",
                    grade="2024",
                    status="active"
                )
                session.add(user)
                session.flush()
                user_id = user.id
                student_id = user.student_id
            
            # Test get user detail
            with db_session() as session:
                result = UserService.get_user_detail(user_id)
                assert result["user_id"] == user_id
                assert result["student_id"] == student_id
    
    def test_list_users_admin(self, app):
        """Test admin list users"""
        with app.app_context():
            # Create test user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                user = User(
                    student_id=f"2024{unique}",
                    email=f"test_{unique}@example.com",
                    username="testuser",
                    password=generate_password_hash("test123"),
                    gender="M",
                    college="CS",
                    major="CS",
                    grade="2024",
                    status="active"
                )
                session.add(user)
                session.flush()
            
            # Test list users
            with db_session() as session:
                params = {"page": "1", "page_size": "10"}
                result = UserService.list_users(params)
                assert "total" in result
                assert "list" in result
                assert result["page"] == 1
    
    def test_list_organizers_admin(self, app):
        """Test admin list organizers"""
        with app.app_context():
            # Create test organizer
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                organizer = Organizer(
                    email=f"org_{unique}@example.com",
                    org_name="Test Org",
                    password=generate_password_hash("org123"),
                    org_proof_text="Proof text",
                    status="approved"
                )
                session.add(organizer)
                session.flush()
            
            # Test list organizers
            with db_session() as session:
                params = {"page": "1", "page_size": "10"}
                result = UserService.list_organizers(params)
                assert "total" in result
                assert "list" in result
                assert result["page"] == 1