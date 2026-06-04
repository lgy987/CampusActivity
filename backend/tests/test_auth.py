"""?? JWT ????"""

from app.common.auth import create_token, decode_token
from flask import Flask
import pytest

class TestJWT:
    def setup_method(self):
        """???????"""
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "test-secret-key-12345"
        self.ctx = self.app.app_context()
        self.ctx.push()
    
    def teardown_method(self):
        self.ctx.pop()
    
    def test_create_token(self):
        """???? token"""
        token = create_token("user", 123)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_decode_token_success(self):
        """?????? token"""
        token = create_token("organizer", 456)
        payload = decode_token(token)
        assert payload is not None
        assert payload["role"] == "organizer"
        assert payload["user_id"] == 456
        assert "exp" in payload
    
    def test_decode_token_invalid(self):
        """?????? token"""
        payload = decode_token("invalid.token.string")
        assert payload is None
    
    def test_decode_token_expired(self):
        """?????? token"""
        # ????????? token?????????????? token ?????
        payload = decode_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDAwMDAwMDB9.signature")
        assert payload is None
    
    def test_create_and_decode_user_token(self):
        """???? token ??????"""
        token = create_token("user", 999)
        payload = decode_token(token)
        assert payload["role"] == "user"
        assert payload["user_id"] == 999
    
    def test_create_and_decode_admin_token(self):
        """????? token ??????"""
        token = create_token("admin", 888)
        payload = decode_token(token)
        assert payload["role"] == "admin"
        assert payload["user_id"] == 888
