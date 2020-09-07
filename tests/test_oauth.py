import pytest
from flask import session, url_for, request

def test_login(client, app):
    rv = client.get('oauth/login')
    # test that viewing the page renders without errors
    assert rv.status_code == 200
    # test that page renders correct html 
    assert b'Sign In' in rv.data


def test_authorized_noop(client, app):
    rv = client.get('oauth' + app.config['REDIRECT_PATH'])
    # test for redirect
    assert rv.status_code == 302
    # test that the redirect is to the index url with no-op
    assert rv.headers['Location'] == 'http://localhost/'
    

def test_authorized_error(client, app):
    with client:
        with client.session_transaction() as sess: # session for test
            sess['state'] = 'test'

        rv = client.get(
            'oauth' + app.config['REDIRECT_PATH'] + '?error=error&state=test'
        )
        # 
        assert rv.status_code == 200
        # test for correct args
        assert request.args['error'] == 'error'
        # test that error page is displayed
        assert b'Login Failure' in rv.data


def test_authorized_acquire_token(client, app, mock_msal):
    with client:
        with client.session_transaction() as sess: # session for test
            sess['state'] = 'test'

        rv = client.get(
            'oauth' + app.config['REDIRECT_PATH'] + '?code=test&state=test'
        )
        # test that code has been ran by checking if session has been updated
        assert session["user"] == 'mock_claim'
        # test for redirect back to index
        assert rv.status_code == 302
        assert rv.headers['Location'] == 'http://localhost/'
 


    
