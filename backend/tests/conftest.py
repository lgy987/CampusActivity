"""pytest ????"""

import os
import pytest

# ??????
os.environ["FLASK_ENV"] = "testing"
os.environ["DISABLE_SCHEDULER"] = "1"

from app import create_app


@pytest.fixture
def app():
    """??????"""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """?????"""
    return app.test_client()
