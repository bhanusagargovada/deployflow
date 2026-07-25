import pytest
from app import create_app
from config import TestingConfig
from database import db as _db


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_login_logout(client):
    # register (use password >=6 chars)
    rv = client.post('/auth/register', data={'username': 'testuser', 'email': 'test@example.com', 'password': 'password', 'confirm': 'password'}, follow_redirects=True)
    assert b'Account created' in rv.data
    # login
    rv = client.post('/auth/login', data={'email': 'test@example.com', 'password': 'password'}, follow_redirects=True)
    assert b'Logged in successfully' in rv.data
    # logout
    rv = client.get('/auth/logout', follow_redirects=True)
    assert b'You have been logged out' in rv.data
