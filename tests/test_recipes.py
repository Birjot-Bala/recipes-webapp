import pytest
from flask import session, url_for, request

def test_nologin_index(client, app):
    rv = client.get('/')
    # test that viewing the page redirects
    assert rv.status_code == 302
    # test redirect location
    assert rv.headers['Location'] == 'http://localhost/oauth/login'

def test_user_index(client, app):
    with client:
        with client.session_transaction() as sess: # session for test
            sess["user"] = {"name": "test_user"}

        rv = client.get('/')
        # test that viewing the page renders without errors
        assert rv.status_code == 200
        # test content
        assert b'Welcome test_user' in rv.data 