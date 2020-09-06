import pytest
from flask import session

def test_login(client, app):
    # test that viewing the page renders without errors
    assert client.get("oauth/login").status_code == 200




