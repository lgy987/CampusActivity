"""??????? - ???????"""

import pytest
from sqlalchemy import text


class TestDatabaseConnection:
    def test_db_session_works(self, app):
        """???????????"""
        from app.common.database import db_session
        
        with app.app_context():
            with db_session() as session:
                # ??????
                result = session.execute(text("SELECT 1"))
                assert result.fetchone()[0] == 1
    
    def test_create_and_query_user(self, app):
        """?????????"""
        from app.common.database import db_session
        from models import User
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            with db_session() as session:
                # ????
                user = User(
                    student_id="2024099901",
                    email="dbtest@example.com",
                    username="?????",
                    password=generate_password_hash("test123"),
                    gender="?",
                    college="????",
                    major="????",
                    grade="2024?",
                    status="active"
                )
                session.add(user)
                session.flush()
                user_id = user.id
                
                # ????
                found = session.get(User, user_id)
                assert found is not None
                assert found.email == "dbtest@example.com"
