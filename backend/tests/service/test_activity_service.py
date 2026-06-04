"""Database tests for activity service"""

import pytest
import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from app.services.activity_service import ActivityService
from app.common.errors import BusinessError
from app.common.database import db_session
from models import Activity, Organizer, Category


class TestActivityDB:
    
    def test_create_activity_success(self, app):
        """Test create activity success"""
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
                category_id = category.id
            
            # Create activity
            with db_session() as session:
                start_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() + timedelta(days=7, hours=2)).strftime("%Y-%m-%d %H:%M:%S")
                deadline = (datetime.utcnow() + timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S")
                
                data = {
                    "name": "Test Activity",
                    "category_id": category_id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "campus": "Liangxiang",
                    "location": "Building A101",
                    "max_participants": 50,
                    "registration_deadline": deadline,
                    "cancel_deadline": deadline,
                    "description": "Test description"
                }
                
                result = ActivityService.create_activity(organizer_id, data)
                assert result["status"] == "draft"
                assert result["activity_id"] is not None
    
    def test_submit_activity_success(self, app):
        """Test submit activity success"""
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
            
            # Create activity
            with db_session() as session:
                start_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() + timedelta(days=7, hours=2)).strftime("%Y-%m-%d %H:%M:%S")
                deadline = (datetime.utcnow() + timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S")
                
                data = {
                    "name": "Test Activity",
                    "category_id": category_id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "campus": "Liangxiang",
                    "location": "Building A101",
                    "max_participants": 50,
                    "registration_deadline": deadline,
                    "cancel_deadline": deadline,
                    "description": "Test description"
                }
                
                result = ActivityService.create_activity(organizer_id, data)
                activity_id = result["activity_id"]
            
            # Submit activity
            with db_session() as session:
                result = ActivityService.submit_activity(organizer_id, activity_id)
                assert result["status"] == "pending"
    
    def test_get_activity_detail(self, app):
        """Test get activity detail"""
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
            
            # Create activity
            with db_session() as session:
                start_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() + timedelta(days=7, hours=2)).strftime("%Y-%m-%d %H:%M:%S")
                deadline = (datetime.utcnow() + timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S")
                
                data = {
                    "name": "Test Activity",
                    "category_id": category_id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "campus": "Liangxiang",
                    "location": "Building A101",
                    "max_participants": 50,
                    "registration_deadline": deadline,
                    "cancel_deadline": deadline,
                    "description": "Test description"
                }
                
                result = ActivityService.create_activity(organizer_id, data)
                activity_id = result["activity_id"]
                activity_name = data["name"]
            
            # Get detail
            with db_session() as session:
                result = ActivityService.get_detail(activity_id, None, None)
                assert result["activity_id"] == activity_id
                assert result["name"] == activity_name
    
    def test_update_activity_draft(self, app):
        """Test update draft activity"""
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
            
            # Create activity
            with db_session() as session:
                start_time = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                end_time = (datetime.utcnow() + timedelta(days=7, hours=2)).strftime("%Y-%m-%d %H:%M:%S")
                deadline = (datetime.utcnow() + timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S")
                
                data = {
                    "name": "Test Activity",
                    "category_id": category_id,
                    "start_time": start_time,
                    "end_time": end_time,
                    "campus": "Liangxiang",
                    "location": "Building A101",
                    "max_participants": 50,
                    "registration_deadline": deadline,
                    "cancel_deadline": deadline,
                    "description": "Test description"
                }
                
                result = ActivityService.create_activity(organizer_id, data)
                activity_id = result["activity_id"]
            
            # Update activity
            with db_session() as session:
                new_start_time = (datetime.utcnow() + timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")
                new_end_time = (datetime.utcnow() + timedelta(days=8, hours=2)).strftime("%Y-%m-%d %H:%M:%S")
                new_deadline = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
                
                update_data = {
                    "name": "Updated Activity",
                    "category_id": category_id,
                    "start_time": new_start_time,
                    "end_time": new_end_time,
                    "campus": "Zhongguancun",
                    "location": "Building B201",
                    "max_participants": 100,
                    "registration_deadline": new_deadline,
                    "cancel_deadline": new_deadline,
                    "description": "Updated description"
                }
                
                result = ActivityService.update_activity(organizer_id, activity_id, update_data)
                assert result["status"] == "draft"
            
            # Verify update
            with db_session() as session:
                detail = ActivityService.get_detail(activity_id, None, None)
                assert detail["name"] == "Updated Activity"
                assert detail["campus"] == "Zhongguancun"