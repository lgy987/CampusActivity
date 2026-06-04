"""pytest ????"""

import os
import sys

# ?? backend ??? Python ??
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

os.environ["FLASK_ENV"] = "testing"
os.environ["DISABLE_SCHEDULER"] = "1"


@pytest.fixture
def app():
    """??????"""
    from app import create_app
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """?????"""
    return app.test_client()
