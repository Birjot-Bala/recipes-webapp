import os
import tempfile

import pytest
import requests
import msal

from recipes_webapp import create_app
from recipes_webapp.db import get_db, init_db

class MockResponse:

    @staticmethod
    def json():
        return {"mock_key": "mock_response"}

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        "TESTING": True, 
        "SESSION_TYPE": "filesystem", 
        "DATABASE": db_path,
        "REDIRECT_PATH": "/getAToken",
        "SCOPE": ["User.ReadBasic.All", "Notes.Read"],
        "CLIENT_ID": "test",
        "CLIENT_SECRET": "secret",
        "AUTHORITY": "https://login.microsoftonline.com/common",
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # clean up
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
            

@pytest.fixture
def runner(app):
    """A test runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def mock_requests(monkeypatch):
    """Monkeypatch for requests with mock response."""
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

@pytest.fixture
def mock_msal(monkeypatch):
    """Monkeypatch for MSAL library."""
    def mock_acquire_token(*args, **kwargs):
        return {'access_token': 'mock_token', 'id_token_claims': 'mock_user'}
    
    monkeypatch.setattr(
        msal.ClientApplication, 'acquire_token_by_authorization_code', 
        mock_acquire_token
    )