"""Database tests for registration service"""

import pytest
import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app.services.registration_service import RegistrationService
from app.services.activity_service import ActivityService
from app.common.errors import BusinessError
from app.common.database import db_session
from models import Activity, Organizer, Category, User, Registration


class TestRegistrationDB:
    
    def test_register_activity_success(self, app):
        """Test register activity success"""
        with app.app_context():
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
            
            # Test register
            with db_session() as session:
                result = RegistrationService.register(user_id, activity_id)
                assert result["status"] == "registered"
                assert result["registration_id"] is not None
    
    def test_register_duplicate(self, app):
        """Test duplicate registration"""
        with app.app_context():
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
            
            # First registration
            with db_session() as session:
                RegistrationService.register(user_id, activity_id)
            
            # Duplicate registration should fail
            with db_session() as session:
                with pytest.raises(BusinessError) as exc:
                    RegistrationService.register(user_id, activity_id)
                assert exc.value.code == 400
    
    def test_cancel_registration(self, app):
        """Test cancel registration"""
        with app.app_context():
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
            
            # Register
            with db_session() as session:
                RegistrationService.register(user_id, activity_id)
            
            # Cancel
            with db_session() as session:
                result = RegistrationService.cancel(user_id, activity_id)
                assert "release_time" in result
    
    def test_get_my_registrations(self, app):
        """Test get my registrations"""
        with app.app_context():
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
            
            # Register
            with db_session() as session:
                RegistrationService.register(user_id, activity_id)
            
            # Get my registrations
            with db_session() as session:
                params = {"page": "1", "page_size": "20"}
                result = RegistrationService.get_my_registrations(user_id, params)
                assert result["total"] >= 1
                assert len(result["list"]) >= 1