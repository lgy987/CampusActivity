"""pytest config with database support"""

import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["FLASK_ENV"] = "testing"
os.environ["DISABLE_SCHEDULER"] = "1"

from app import create_app
from app.common.database import db_session
from models import Base, User, Organizer, Admin, Category, Activity


@pytest.fixture(scope="session")
def app():
    """Create test app with in-memory database"""
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    
    import app.common.database as database
    database.engine = test_engine
    database.SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=test_engine))
    
    Base.metadata.create_all(bind=test_engine)
    
    app = create_app()
    app.config["TESTING"] = True
    
    yield app
    
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session_fixture(app):
    with app.app_context():
        with db_session() as session:
            yield session


@pytest.fixture
def test_user(db_session_fixture):
    import time
    unique_suffix = str(int(time.time() * 1000))[-6:]
    user = User(
        student_id=f"2024{unique_suffix}",
        email=f"test_{unique_suffix}@example.com",
        username="testuser",
        password=generate_password_hash("test123"),
        gender="男",
        college="计算机学院",
        major="CS",
        grade="2024",
        status="active"
    )
    db_session_fixture.add(user)
    db_session_fixture.flush()
    # Refresh to keep object attached to session
    db_session_fixture.refresh(user)
    return user


@pytest.fixture
def test_organizer(db_session_fixture):
    import time
    unique_suffix = str(int(time.time() * 1000))[-6:]
    organizer = Organizer(
        email=f"org_{unique_suffix}@example.com",
        org_name="Test Org",
        password=generate_password_hash("org123"),
        org_proof_text="Proof",
        status="approved"
    )
    db_session_fixture.add(organizer)
    db_session_fixture.flush()
    db_session_fixture.refresh(organizer)
    return organizer


@pytest.fixture
def test_admin(db_session_fixture):
    import time
    unique_suffix = str(int(time.time() * 1000))[-6:]
    admin = Admin(
        admin_no=f"{unique_suffix}",
        email=f"admin_{unique_suffix}@example.com",
        password=generate_password_hash("admin123"),
        username="admin",
        role="admin",
        status="active"
    )
    db_session_fixture.add(admin)
    db_session_fixture.flush()
    db_session_fixture.refresh(admin)
    return admin


@pytest.fixture
def test_category(db_session_fixture):
    import time
    category_id = int(str(int(time.time() * 1000))[-5:]) + 100
    category = Category(
        id=category_id,
        name="Lecture",
        parent_id=1,
        level=2,
        sort_order=1
    )
    db_session_fixture.add(category)
    db_session_fixture.flush()
    db_session_fixture.refresh(category)
    return category


@pytest.fixture
def test_activity(db_session_fixture, test_organizer, test_category):
    from datetime import datetime, timedelta
    start_time = datetime.utcnow() + timedelta(days=7)
    end_time = start_time + timedelta(hours=2)
    deadline = start_time - timedelta(days=1)
    
    activity = Activity(
        organizer_id=test_organizer.id,
        category_id=test_category.id,
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
    db_session_fixture.add(activity)
    db_session_fixture.flush()
    db_session_fixture.refresh(activity)
    return activity


@pytest.fixture
def test_open_activity(db_session_fixture, test_organizer, test_category):
    from datetime import datetime, timedelta
    start_time = datetime.utcnow() + timedelta(days=7)
    end_time = start_time + timedelta(hours=2)
    deadline = start_time - timedelta(days=1)
    
    activity = Activity(
        organizer_id=test_organizer.id,
        category_id=test_category.id,
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
    db_session_fixture.add(activity)
    db_session_fixture.flush()
    db_session_fixture.refresh(activity)
    return activity


@pytest.fixture
def auth_headers_user(client, test_user):
    response = client.post("/auth/login", json={
        "role": "user",
        "account": test_user.student_id,
        "password": "test123"
    })
    token = response.get_json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_organizer(client, test_organizer):
    response = client.post("/auth/login", json={
        "role": "organizer",
        "account": test_organizer.email,
        "password": "org123"
    })
    token = response.get_json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_admin(client, test_admin):
    response = client.post("/auth/login", json={
        "role": "admin",
        "account": test_admin.admin_no,
        "password": "admin123"
    })
    token = response.get_json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}
