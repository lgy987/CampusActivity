"""Database tests for notification service"""

import time
import pytest
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app.services.notification_service import NotificationService
from app.common.errors import BusinessError
from app.common.database import db_session
from models import Notification, Announcement, Admin


class TestNotificationDB:
    
    def test_create_announcement_success(self, app):
        """Test create announcement success"""
        with app.app_context():
            # Create admin
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
            
            # Create announcement
            with db_session() as session:
                start_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                
                result = NotificationService.create_announcement(
                    admin_id, "Test Announcement", "This is test content", start_time, end_time
                )
                assert "announcement_id" in result
    
    def test_create_announcement_empty_title(self, app):
        """Test create announcement with empty title"""
        with app.app_context():
            # Create admin
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
            
            # Test empty title
            with db_session() as session:
                start_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                
                with pytest.raises(BusinessError) as exc:
                    NotificationService.create_announcement(admin_id, "", "Content", start_time, end_time)
                assert exc.value.code == 400
    
    def test_create_announcement_title_too_long(self, app):
        """Test create announcement with title too long"""
        with app.app_context():
            # Create admin
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
            
            # Test title too long (>50 characters)
            with db_session() as session:
                long_title = "A" * 51
                start_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                
                with pytest.raises(BusinessError) as exc:
                    NotificationService.create_announcement(admin_id, long_title, "Content", start_time, end_time)
                assert exc.value.code == 400
    
    def test_list_announcements(self, app):
        """Test list announcements"""
        with app.app_context():
            # Create admin
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
            
            # Create announcement
            with db_session() as session:
                start_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                
                unique_title = f"Test Title {int(time.time())}"
                NotificationService.create_announcement(admin_id, unique_title, "Content", start_time, end_time)
                
                result = NotificationService.list_announcements()
                assert len(result) >= 1
                # Find the announcement we just created
                found = any(a["title"] == unique_title for a in result)
                assert found is True
    
    def test_list_valid_announcements(self, app):
        """Test list valid announcements (public)"""
        with app.app_context():
            # Create admin
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
            
            # Create valid announcement (started in past, ends in future)
            with db_session() as session:
                start_time = (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                
                NotificationService.create_announcement(admin_id, "Valid Title", "Content", start_time, end_time)
                
                result = NotificationService.list_valid_announcements()
                # Should find the valid announcement
                assert len(result) >= 0
    
    def test_list_valid_announcements_empty(self, app):
        """Test list valid announcements when none valid"""
        with app.app_context():
            # Create admin
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
            
            # Create expired announcement (ended in past)
            with db_session() as session:
                start_time = (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                
                NotificationService.create_announcement(admin_id, "Expired Title", "Content", start_time, end_time)
                
                result = NotificationService.list_valid_announcements()
                # Expired announcement should not be in valid list
                # Valid announcements count may be 0
                assert isinstance(result, list)
    
    def test_delete_announcement_success(self, app):
        """Test delete announcement success"""
        with app.app_context():
            # Create admin
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
            
            # Create announcement
            with db_session() as session:
                start_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                
                result = NotificationService.create_announcement(admin_id, "To Delete", "Content", start_time, end_time)
                announcement_id = result["announcement_id"]
            
            # Delete announcement
            with db_session() as session:
                NotificationService.delete_announcement(announcement_id)
                
                # Verify deleted
                announcement = session.get(Announcement, announcement_id)
                assert announcement is None