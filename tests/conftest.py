import os
import tempfile

import pytest
import requests

from recipes_webapp import create_app

class MockResponse:

    @staticmethod
    def json():
        return {"mock_key": "mock_response"}

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

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
            

@pytest.fixture
def mock_requests(monkeypatch):
    """Monkeypatch for requests with mock response."""
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)