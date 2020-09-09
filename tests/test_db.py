import sqlite3

import pytest
from recipes_webapp.db import get_db, modified_date_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """Test that init-db command is called correctly."""
    class Recorder(object):
        called = False
    
    def fake_init_db():
        Recorder.called = True
    
    monkeypatch.setattr('recipes_webapp.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called


def test_modified_date_db(app):
    """Test that modified_date_db has no errors."""
    with app.app_context():
        assert isinstance(modified_date_db(), str)