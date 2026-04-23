"""
Test suite for auth routes (register and login endpoints).
Methodology: Integration testing with Flask test client and in-memory SQLite.
"""
import pytest
from app import create_app
from app.models import db as _db


@pytest.fixture
def client():
    # Pass test_config INTO create_app so the in-memory DB is used
    # before db.init_app(app) and db.create_all() run inside the factory.
    app = create_app(test_config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    with app.app_context():
        with app.test_client() as c:
            yield c
        _db.session.remove()
        _db.drop_all()


class TestRegister:
    """Auth registration endpoint tests"""

    def test_register_success(self, client):
        """Valid registration returns 201"""
        res = client.post("/auth/register", json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "password123"
        })
        assert res.status_code == 201
        assert "user" in res.get_json()

    def test_register_missing_fields(self, client):
        """Missing fields returns 400"""
        res = client.post("/auth/register", json={
            "email": "test@example.com"
        })
        assert res.status_code == 400

    def test_register_duplicate_email(self, client):
        """Duplicate email is rejected (400 or 409 depending on blueprint)"""
        client.post("/auth/register", json={
            "email": "dup@example.com",
            "username": "user1",
            "password": "password123"
        })
        res = client.post("/auth/register", json={
            "email": "dup@example.com",
            "username": "user2",
            "password": "password123"
        })
        # Accept either status — both indicate duplicate email rejection.
        # This keeps the test stable across issue #30 blueprint decision.
        assert res.status_code in (400, 409)


class TestLogin:
    """Auth login endpoint tests"""

    def test_login_success(self, client):
        """Valid login returns 200"""
        client.post("/auth/register", json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "password123"
        })
        res = client.post("/auth/login", json={
            "email": "login@example.com",
            "password": "password123"
        })
        assert res.status_code == 200
        assert res.get_json()["message"] == "Login successful"

    def test_login_wrong_password(self, client):
        """Wrong password returns 401"""
        client.post("/auth/register", json={
            "email": "wrong@example.com",
            "username": "wronguser",
            "password": "password123"
        })
        res = client.post("/auth/login", json={
            "email": "wrong@example.com",
            "password": "badpassword"
        })
        assert res.status_code == 401

    def test_login_missing_fields(self, client):
        """Missing fields returns 400"""
        res = client.post("/auth/login", json={
            "email": "test@example.com"
        })
        assert res.status_code == 400


"""
SOURCES:
- pytest fixtures: https://docs.pytest.org/en/stable/how-to/fixtures.html
- Flask test client: https://flask.palletsprojects.com/en/3.0.x/testing/
- Existing test_api.py pattern in this project
"""