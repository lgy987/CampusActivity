"""Database tests for auth service"""

import pytest
import time
from werkzeug.security import generate_password_hash
from app.services.auth_service import AuthService
from app.common.errors import BusinessError
from app.common.database import db_session
from models import User, Organizer, Admin


class TestDBAuth:
    
    def test_register_user_success(self, app):
        """Test user registration success"""
        with app.app_context():
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                data = {
                    "student_id": f"2024{unique}",
                    "email": f"db_test_{unique}@example.com",
                    "username": "dbtest",
                    "password": "Test123456",
                    "confirm_password": "Test123456",
                    "gender": "M",
                    "college": "CS",
                    "major": "CS",
                    "grade": "2024"
                }
                result = AuthService.register_user(data)
                assert result["role"] == "user"
                assert "token" in result
    
    def test_register_user_duplicate_student_id(self, app):
        """Test duplicate student id registration"""
        with app.app_context():
            # Create first user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                student_id = f"2024{unique}"
                data1 = {
                    "student_id": student_id,
                    "email": f"first_{unique}@example.com",
                    "username": "firstuser",
                    "password": "Test123456",
                    "confirm_password": "Test123456",
                    "gender": "M",
                    "college": "CS",
                    "major": "CS",
                    "grade": "2024"
                }
                AuthService.register_user(data1)
            
            # Try to register with same student_id
            with db_session() as session:
                data2 = {
                    "student_id": student_id,
                    "email": f"second_{unique}@example.com",
                    "username": "seconduser",
                    "password": "Test123456",
                    "confirm_password": "Test123456",
                    "gender": "M",
                    "college": "CS",
                    "major": "CS",
                    "grade": "2024"
                }
                with pytest.raises(BusinessError) as exc:
                    AuthService.register_user(data2)
                assert exc.value.code == 400
    
    def test_login_success(self, app):
        """Test login success"""
        with app.app_context():
            # Create user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                student_id = f"2024{unique}"
                data = {
                    "student_id": student_id,
                    "email": f"login_{unique}@example.com",
                    "username": "logintest",
                    "password": "Test123456",
                    "confirm_password": "Test123456",
                    "gender": "M",
                    "college": "CS",
                    "major": "CS",
                    "grade": "2024"
                }
                AuthService.register_user(data)
            
            # Test login
            with db_session() as session:
                result = AuthService.login("user", student_id, "Test123456")
                assert result["role"] == "user"
                assert "token" in result
    
    def test_login_wrong_password(self, app):
        """Test login with wrong password"""
        with app.app_context():
            # Create user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                student_id = f"2024{unique}"
                data = {
                    "student_id": student_id,
                    "email": f"wrongpwd_{unique}@example.com",
                    "username": "wrongtest",
                    "password": "Test123456",
                    "confirm_password": "Test123456",
                    "gender": "M",
                    "college": "CS",
                    "major": "CS",
                    "grade": "2024"
                }
                AuthService.register_user(data)
            
            # Test wrong password
            with db_session() as session:
                with pytest.raises(BusinessError) as exc:
                    AuthService.login("user", student_id, "WrongPassword")
                assert exc.value.code == 401
    
    def test_login_nonexistent_user(self, app):
        """Test login with nonexistent user"""
        with app.app_context():
            with pytest.raises(BusinessError) as exc:
                AuthService.login("user", "9999999999", "password")
            assert exc.value.code == 401
    
    def test_register_organizer_success(self, app):
        """Test organizer registration success"""
        with app.app_context():
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                data = {
                    "email": f"new_org_{unique}@example.com",
                    "org_name": "New Org",
                    "password": "Test123456",
                    "confirm_password": "Test123456",
                    "org_proof_text": "Proof text"
                }
                result = AuthService.register_organizer(data)
                assert result["role"] == "organizer"
                assert "token" in result
    
    def test_register_organizer_duplicate_email(self, app):
        """Test organizer registration with duplicate email"""
        with app.app_context():
            # Create first organizer
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                email = f"dup_org_{unique}@example.com"
                data1 = {
                    "email": email,
                    "org_name": "First Org",
                    "password": "Test123456",
                    "confirm_password": "Test123456",
                    "org_proof_text": "Proof text"
                }
                AuthService.register_organizer(data1)
            
            # Try to register with same email
            with db_session() as session:
                data2 = {
                    "email": email,
                    "org_name": "Duplicate Org",
                    "password": "Test123456",
                    "confirm_password": "Test123456",
                    "org_proof_text": "Proof text"
                }
                with pytest.raises(BusinessError) as exc:
                    AuthService.register_organizer(data2)
                assert exc.value.code == 400
    
    def test_organizer_login_success(self, app):
        """Test organizer login success"""
        with app.app_context():
            # Create organizer
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                email = f"org_login_{unique}@example.com"
                data = {
                    "email": email,
                    "org_name": "Login Org",
                    "password": "Test123456",
                    "confirm_password": "Test123456",
                    "org_proof_text": "Proof text"
                }
                AuthService.register_organizer(data)
            
            # Test login
            with db_session() as session:
                result = AuthService.login("organizer", email, "Test123456")
                assert result["role"] == "organizer"
                assert "token" in result
    
    def test_admin_login_success(self, app):
        """Test admin login success"""
        with app.app_context():
            # Create admin
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                admin_no = unique
                admin = Admin(
                    admin_no=admin_no,
                    email=f"admin_{unique}@example.com",
                    password=generate_password_hash("admin123"),
                    username="testadmin",
                    role="admin",
                    status="active"
                )
                session.add(admin)
                session.flush()
            
            # Test login
            with db_session() as session:
                result = AuthService.login("admin", admin_no, "admin123")
                assert result["role"] == "admin"
                assert "token" in result
    
    def test_register_deleted_organizer_reactivate(self, app):
        """Test reactivate deleted organizer"""
        with app.app_context():
            # Create organizer
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                email = f"deleted_org_{unique}@example.com"
                organizer = Organizer(
                    email=email,
                    org_name="To Be Deleted",
                    password=generate_password_hash("oldpassword"),
                    org_proof_text="Proof",
                    status="approved"
                )
                session.add(organizer)
                session.flush()
                
                # Delete organizer
                organizer.status = "deleted"
                session.flush()
            
            # Reactivate
            with db_session() as session:
                data = {
                    "email": email,
                    "org_name": "Reactivated Org",
                    "password": "NewPassword123",
                    "confirm_password": "NewPassword123",
                    "org_proof_text": "New proof text"
                }
                result = AuthService.register_organizer(data)
                assert result["role"] == "organizer"
                assert "token" in result
            
            # Verify reactivation
            with db_session() as session:
                updated_organizer = session.query(Organizer).filter(Organizer.email == email).first()
                assert updated_organizer.status == "pending"
                assert updated_organizer.org_name == "Reactivated Org"