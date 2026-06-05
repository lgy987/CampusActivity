"""Database connection tests - in-memory database"""

import pytest
from sqlalchemy import text


class TestDatabaseConnection:
    def test_db_session_works(self, app):
        """Test database session works"""
        from app.common.database import db_session
        
        with app.app_context():
            with db_session() as session:
                result = session.execute(text("SELECT 1"))
                assert result.fetchone()[0] == 1
    
    def test_create_and_query_user(self, app):
        """Test create and query user"""
        from app.common.database import db_session
        from models import User
        from werkzeug.security import generate_password_hash
        import time
        
        with app.app_context():
            with db_session() as session:
                # Use unique data to avoid conflicts
                unique_suffix = str(int(time.time() * 1000))[-6:]
                
                user = User(
                    student_id=f"2024{unique_suffix}",
                    email=f"dbtest_{unique_suffix}@example.com",
                    username="dbtest",
                    password=generate_password_hash("test123"),
                    gender="M",
                    college="Test College",
                    major="Test Major",
                    grade="2024",
                    status="active"
                )
                session.add(user)
                session.flush()
                user_id = user.id
                
                # Query the user
                found = session.get(User, user_id)
                assert found is not None
                assert found.email == f"dbtest_{unique_suffix}@example.com"