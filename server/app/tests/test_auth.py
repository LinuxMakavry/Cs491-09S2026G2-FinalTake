"""
Test suite for /auth routes (register + login)
TC-A01 through TC-A10
"""
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app(test_config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        with app.test_client() as client:
            yield client


# ── Register ────────────────────────────────────────────────
class TestRegister:

    def test_register_success(self, client):
        """TC-A01: Valid data → 201 and user object returned"""
        res = client.post("/auth/register", json={
            "username": "alice", "email": "alice@test.com", "password": "secret123"
        })
        assert res.status_code == 201
        data = res.get_json()
        assert data["user"]["username"] == "alice"
        assert data["user"]["email"] == "alice@test.com"
        assert "password" not in data["user"]
        assert "password_hash" not in data["user"]

    def test_register_missing_fields_returns_400(self, client):
        """TC-A02: Missing password → 400"""
        res = client.post("/auth/register", json={
            "username": "bob", "email": "bob@test.com"
        })
        assert res.status_code == 400
        assert "error" in res.get_json()

    def test_register_duplicate_email_returns_409(self, client):
        """TC-A03: Same email twice → 409 conflict"""
        client.post("/auth/register", json={
            "username": "alice", "email": "alice@test.com", "password": "secret123"
        })
        res = client.post("/auth/register", json={
            "username": "alice2", "email": "alice@test.com", "password": "other"
        })
        assert res.status_code == 409
        assert "error" in res.get_json()

    def test_register_duplicate_username_returns_409(self, client):
        """TC-A04: Same username twice → 409 conflict"""
        client.post("/auth/register", json={
            "username": "alice", "email": "alice@test.com", "password": "secret123"
        })
        res = client.post("/auth/register", json={
            "username": "alice", "email": "different@test.com", "password": "other"
        })
        assert res.status_code == 409

    def test_register_password_not_exposed(self, client):
        """TC-A05: Password hash must never appear in response"""
        res = client.post("/auth/register", json={
            "username": "charlie", "email": "charlie@test.com", "password": "pass"
        })
        body = res.get_json()
        assert "password_hash" not in str(body)
        assert "password" not in body["user"]


# ── Login ───────────────────────────────────────────────────
class TestLogin:

    def _register(self, client):
        client.post("/auth/register", json={
            "username": "testuser", "email": "test@test.com", "password": "password123"
        })

    def test_login_success(self, client):
        """TC-A06: Correct credentials → 200 and user object"""
        self._register(client)
        res = client.post("/auth/login", json={
            "email": "test@test.com", "password": "password123"
        })
        assert res.status_code == 200
        data = res.get_json()
        assert data["message"] == "Login successful"
        assert data["user"]["email"] == "test@test.com"

    def test_login_wrong_password_returns_401(self, client):
        """TC-A07: Wrong password → 401"""
        self._register(client)
        res = client.post("/auth/login", json={
            "email": "test@test.com", "password": "wrongpassword"
        })
        assert res.status_code == 401
        assert "error" in res.get_json()

    def test_login_unknown_email_returns_401(self, client):
        """TC-A08: Email not in DB → 401"""
        res = client.post("/auth/login", json={
            "email": "nobody@test.com", "password": "password123"
        })
        assert res.status_code == 401

    def test_login_missing_fields_returns_400(self, client):
        """TC-A09: Missing email → 400"""
        res = client.post("/auth/login", json={"password": "password123"})
        assert res.status_code == 400

    def test_login_empty_body_returns_400(self, client):
        """TC-A10: Empty JSON body → 400"""
        res = client.post("/auth/login", json={})
        assert res.status_code == 400
