import pytest
from flask import session

def test_login(client, app):
    rv = client.get("oauth/login")
    # test that viewing the page renders without errors
    assert rv.status_code == 200
    # test that page renders correct html 
    assert b'Sign In' in rv.data