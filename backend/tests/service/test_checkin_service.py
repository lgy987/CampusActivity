"""Database tests for checkin service"""

import pytest
import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app.services.checkin_service import CheckinService
from app.services.registration_service import RegistrationService
from app.common.errors import BusinessError
from app.common.database import db_session
from models import Activity, Organizer, Category, User, Registration


class TestCheckinDB:
    
    def test_get_checkin_code_success(self, app):
        """Test get checkin code success"""
        with app.app_context():
            # Create organizer
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                organizer = Organizer(
                    email=f"org_{unique}@example.com",
                    org_name="Test Org",
                    password=generate_password_hash("org123"),
                    org_proof_text="Proof",
                    status="approved"
                )
                session.add(organizer)
                session.flush()
                organizer_id = organizer.id
            
            # Create category
            with db_session() as session:
                category_id = int(str(int(time.time() * 1000))[-5:]) + 100
                category = Category(
                    id=category_id,
                    name="Lecture",
                    parent_id=1,
                    level=2,
                    sort_order=1
                )
                session.add(category)
                session.flush()
            
            # Create activity (draft)
            with db_session() as session:
                start_time = datetime.utcnow() + timedelta(days=7)
                end_time = start_time + timedelta(hours=2)
                deadline = start_time - timedelta(days=1)
                
                activity = Activity(
                    organizer_id=organizer_id,
                    category_id=category_id,
                    name="Test Activity",
                    start_time=start_time,
                    end_time=end_time,
                    campus="Liangxiang",
                    location="Building A",
                    max_participants=50,
                    current_participants=0,
                    registration_deadline=deadline,
                    cancel_deadline=deadline,
                    description="Test description",
                    status="draft"
                )
                session.add(activity)
                session.flush()
                activity_id = activity.id
            
            # Test get checkin code
            with db_session() as session:
                result = CheckinService.get_checkin_code(organizer_id, activity_id)
                assert "checkin_code" in result
                assert len(result["checkin_code"]) == 6
    
    def test_manual_checkin_success(self, app):
        """Test manual checkin success"""
        with app.app_context():
            # Create organizer
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                organizer = Organizer(
                    email=f"org_{unique}@example.com",
                    org_name="Test Org",
                    password=generate_password_hash("org123"),
                    org_proof_text="Proof",
                    status="approved"
                )
                session.add(organizer)
                session.flush()
                organizer_id = organizer.id
                organizer_email = organizer.email
            
            # Create category
            with db_session() as session:
                category_id = int(str(int(time.time() * 1000))[-5:]) + 100
                category = Category(
                    id=category_id,
                    name="Lecture",
                    parent_id=1,
                    level=2,
                    sort_order=1
                )
                session.add(category)
                session.flush()
            
            # Create open activity
            with db_session() as session:
                start_time = datetime.utcnow() + timedelta(days=7)
                end_time = start_time + timedelta(hours=2)
                deadline = start_time - timedelta(days=1)
                
                activity = Activity(
                    organizer_id=organizer_id,
                    category_id=category_id,
                    name="Open Activity",
                    start_time=start_time,
                    end_time=end_time,
                    campus="Liangxiang",
                    location="Building B",
                    max_participants=50,
                    current_participants=5,
                    registration_deadline=deadline,
                    cancel_deadline=deadline,
                    description="Open for registration",
                    status="open"
                )
                session.add(activity)
                session.flush()
                activity_id = activity.id
            
            # Create user
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                student_id = f"2024{unique}"
                user = User(
                    student_id=student_id,
                    email=f"user_{unique}@example.com",
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
            
            # Register user for activity
            with db_session() as session:
                reg_result = RegistrationService.register(user_id, activity_id)
                assert reg_result["status"] == "registered"
            
            # Manual checkin
            with db_session() as session:
                result = CheckinService.manual_checkin(organizer_id, activity_id, student_id)
                assert result["user_id"] == user_id
                assert "checkin_time" in result
    
    def test_get_checkin_stats(self, app):
        """Test get checkin statistics"""
        with app.app_context():
            # Create organizer
            with db_session() as session:
                unique = str(int(time.time() * 1000))[-6:]
                organizer = Organizer(
                    email=f"org_{unique}@example.com",
                    org_name="Test Org",
                    password=generate_password_hash("org123"),
                    org_proof_text="Proof",
                    status="approved"
                )
                session.add(organizer)
                session.flush()
                organizer_id = organizer.id
            
            # Create category
            with db_session() as session:
                category_id = int(str(int(time.time() * 1000))[-5:]) + 100
                category = Category(
                    id=category_id,
                    name="Lecture",
                    parent_id=1,
                    level=2,
                    sort_order=1
                )
                session.add(category)
                session.flush()
            
            # Create open activity
            with db_session() as session:
                start_time = datetime.utcnow() + timedelta(days=7)
                end_time = start_time + timedelta(hours=2)
                deadline = start_time - timedelta(days=1)
                
                activity = Activity(
                    organizer_id=organizer_id,
                    category_id=category_id,
                    name="Open Activity",
                    start_time=start_time,
                    end_time=end_time,
                    campus="Liangxiang",
                    location="Building B",
                    max_participants=50,
                    current_participants=5,
                    registration_deadline=deadline,
                    cancel_deadline=deadline,
                    description="Open for registration",
                    status="open"
                )
                session.add(activity)
                session.flush()
                activity_id = activity.id
            
            # Test get checkin stats
            with db_session() as session:
                result = CheckinService.get_checkin_stats(organizer_id, activity_id)
                assert "total_registered" in result
                assert "checked_in" in result
                assert "checkin_rate" in result