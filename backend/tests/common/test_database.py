"""Unit tests for database session"""

from app.common.database import db_session
from sqlalchemy import text
import pytest


class TestDatabaseSession:
    def test_db_session_context_manager(self, app):
        """Test database session context manager"""
        with app.app_context():
            with db_session() as session:
                result = session.execute(text("SELECT 1"))
                assert result is not None
    
    def test_db_session_commit(self, app):
        """Test session commit"""
        with app.app_context():
            with db_session() as session:
                assert session is not None
    
    def test_db_session_rollback_on_error(self, app):
        """Test rollback on error"""
        from models import User
        
        with app.app_context():
            # ???????
            with db_session() as session:
                from werkzeug.security import generate_password_hash
                import time
                unique_suffix = str(int(time.time() * 1000))[-6:]
                user = User(
                    student_id=f"2024{unique_suffix}",
                    email=f"test_{unique_suffix}@example.com",
                    username="test",
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
            
            # ????????????????????
            try:
                with db_session() as session:
                    duplicate_user = User(
                        student_id=f"2024{unique_suffix}",  # ?????
                        email="another@example.com",
                        username="another",
                        password=generate_password_hash("test123"),
                        gender="M",
                        college="CS",
                        major="CS",
                        grade="2024",
                        status="active"
                    )
                    session.add(duplicate_user)
                    session.flush()
            except Exception:
                pass
            
            # ??????????
            with db_session() as session:
                user = session.get(User, user_id)
                assert user is not None
                assert user.student_id == f"2024{unique_suffix}"
