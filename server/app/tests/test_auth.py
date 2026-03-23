"""
Test suite for User model
Methodology: Unit testing the User model directly
with an in-memory SQLite database.
"""
import pytest
from flask import Flask
from app.models import db as _db
from app.models.user import User


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    _db.init_app(app)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


def test_create_user(app):
    """User can be created and saved to database"""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('mypassword')
        _db.session.add(user)
        _db.session.commit()
        assert user.id is not None
        assert user.username == 'testuser'


def test_password_is_hashed(app):
    """Password is stored as hash not plaintext"""
    with app.app_context():
        user = User(username='hashuser', email='hash@example.com')
        user.set_password('mypassword')
        assert user.password_hash != 'mypassword'
        assert len(user.password_hash) > 50


def test_check_password_correct(app):
    """check_password returns True for correct password"""
    with app.app_context():
        user = User(username='checkuser', email='check@example.com')
        user.set_password('mypassword')
        assert user.check_password('mypassword') is True


def test_check_password_wrong(app):
    """check_password returns False for wrong password"""
    with app.app_context():
        user = User(username='wronguser', email='wrong@example.com')
        user.set_password('mypassword')
        assert user.check_password('badpassword') is False


def test_to_dict_no_password(app):
    """to_dict never exposes password data"""
    with app.app_context():
        user = User(username='dictuser', email='dict@example.com')
        user.set_password('mypassword')
        _db.session.add(user)
        _db.session.commit()
        data = user.to_dict()
        assert 'password' not in data
        assert 'password_hash' not in data
        assert data['username'] == 'dictuser'


def test_duplicate_email_rejected(app):
    """Database rejects duplicate emails"""
    with app.app_context():
        user1 = User(username='user1', email='same@example.com')
        user1.set_password('pass1')
        _db.session.add(user1)
        _db.session.commit()

        user2 = User(username='user2', email='same@example.com')
        user2.set_password('pass2')
        _db.session.add(user2)
        with pytest.raises(Exception):
            _db.session.commit()
