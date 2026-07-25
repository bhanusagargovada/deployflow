import pytest
from app import create_app
from config import TestingConfig
from database import db as _db
from models.user import User, Role


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


def create_user(app, username, email, password, role):
    with app.app_context():
        u = User(username=username, email=email, role=role)
        u.set_password(password)
        _db.session.add(u)
        _db.session.commit()
        return u


def login(client, email, password):
    return client.post('/auth/login', data={'email': email, 'password': password}, follow_redirects=False)


def test_member_cannot_create_project(app, client):
    create_user(app, 'member', 'member@example.com', 'password', Role.MEMBER)
    login(client, 'member@example.com', 'password')
    rv = client.get('/projects/create')
    # should redirect to dashboard
    assert rv.status_code in (302, 303)


def test_pm_can_create_project(app, client):
    create_user(app, 'pm', 'pm@example.com', 'password', Role.PM)
    login(client, 'pm@example.com', 'password')
    rv = client.get('/projects/create')
    assert rv.status_code == 200
