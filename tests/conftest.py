import os

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
    app = create_app({"TESTING": True, "SESSION_TYPE": "filesystem"})

    yield app


@pytest.fixture
def client(app):
    "A test client for the app."
    return app.test_client()
            

@pytest.fixture
def mock_requests(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)