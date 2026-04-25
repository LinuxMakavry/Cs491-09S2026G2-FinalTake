"""
Test suite for /api/reviews endpoints.
Methodology: Integration Testing (Flask test client + in-memory SQLite)
Member: Ric Escalante (RickWithNoK) — Dev A, API Integration Tests

Test IDs map directly to the Sprint 3 test case table:
  TC-RE-01  POST /api/reviews — create review (happy path)
  TC-RE-02  GET  /api/reviews — list reviews for a media item
  TC-RE-03  DELETE /api/reviews/<id> — owner can delete their review
  TC-RE-04  POST /api/reviews — upsert: second POST updates existing review
  TC-RE-05  POST /api/reviews — unauthenticated request rejected (401)
  TC-RE-06  GET  /api/reviews/mine — returns only the authenticated user's reviews
  TC-RE-07  GET  /api/reviews/check — returns existing review for current user
  TC-RE-08  POST /api/reviews — rating out of range returns 400 (boundary test)
  TC-RE-09  GET  /api/favorites — favorites endpoint unaffected by reviews blueprint (regression)
  TC-RE-10  GET  /api/search — search endpoint unaffected by reviews blueprint (regression)

REFERENCES:
  - pytest docs: https://docs.pytest.org/
  - Flask testing docs: https://flask.palletsprojects.com/en/stable/testing/
  - SQLAlchemy in-memory DB for tests: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html
"""

import pytest
from unittest.mock import patch
from app import create_app
from app.models import db as _db
from app.models.user import User


# ── Fixtures ────────────────────────────────────────────────────────────────

TEST_CONFIG = {
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}


@pytest.fixture
def app():
    """Create a fresh app instance with in-memory SQLite for each test."""
    application = create_app(test_config=TEST_CONFIG)
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def user(app):
    """Create a test user and return the User object."""
    with app.app_context():
        u = User(username="ric_test", email="ric@test.com")
        u.set_password("testpass")
        _db.session.add(u)
        _db.session.commit()
        # Re-query to get a bound instance with an id
        u = User.query.filter_by(email="ric@test.com").first()
        return u


@pytest.fixture
def auth_headers(user):
    """Return X-User-Id header for the test user."""
    return {"X-User-Id": str(user.id)}


def _post_review(client, user_id, media_id="42", media_type="movie",
                  rating=4, body="Great film", title="Test Movie"):
    """Helper: POST a review and return the response."""
    return client.post(
        "/api/reviews",
        json={
            "media_id": media_id,
            "media_type": media_type,
            "rating": rating,
            "body": body,
            "title": title,
        },
        headers={"X-User-Id": str(user_id)},
    )


# ── TC-RE-01: Create review (happy path) ────────────────────────────────────

class TestCreateReview:
    """TC-RE-01 — POST /api/reviews creates a review with correct fields."""

    def test_create_review_returns_201(self, client, user):
        res = _post_review(client, user.id)
        assert res.status_code == 201

    def test_create_review_returns_review_data(self, client, user):
        res = _post_review(client, user.id, rating=5, body="Excellent")
        data = res.get_json()
        assert "review" in data
        assert data["review"]["rating"] == 5
        assert data["review"]["body"] == "Excellent"
        assert data["review"]["media_type"] == "movie"

    def test_create_review_message_is_review_created(self, client, user):
        res = _post_review(client, user.id)
        assert res.get_json()["message"] == "Review created"


# ── TC-RE-02: List reviews for a media item ─────────────────────────────────

class TestGetReviews:
    """TC-RE-02 — GET /api/reviews returns all reviews for a media item."""

    def test_get_reviews_returns_200(self, client, user):
        _post_review(client, user.id, media_id="99", media_type="game")
        res = client.get("/api/reviews?media_type=game&media_id=99")
        assert res.status_code == 200

    def test_get_reviews_returns_list(self, client, user):
        _post_review(client, user.id, media_id="77", media_type="book")
        res = client.get("/api/reviews?media_type=book&media_id=77")
        data = res.get_json()
        assert isinstance(data["reviews"], list)
        assert len(data["reviews"]) == 1

    def test_get_reviews_missing_params_returns_400(self, client):
        res = client.get("/api/reviews")
        assert res.status_code == 400

    def test_get_reviews_includes_username(self, client, user):
        _post_review(client, user.id, media_id="55", media_type="movie")
        res = client.get("/api/reviews?media_type=movie&media_id=55")
        review = res.get_json()["reviews"][0]
        assert "username" in review


# ── TC-RE-03: Delete review (owner only) ────────────────────────────────────

class TestDeleteReview:
    """TC-RE-03 — DELETE /api/reviews/<id> removes the review."""

    def test_owner_can_delete_review(self, client, user):
        create_res = _post_review(client, user.id, media_id="10")
        review_id = create_res.get_json()["review"]["id"]

        del_res = client.delete(
            f"/api/reviews/{review_id}",
            headers={"X-User-Id": str(user.id)},
        )
        assert del_res.status_code == 200

    def test_deleted_review_no_longer_returned(self, client, user):
        create_res = _post_review(client, user.id, media_id="11")
        review_id = create_res.get_json()["review"]["id"]
        client.delete(f"/api/reviews/{review_id}", headers={"X-User-Id": str(user.id)})

        list_res = client.get("/api/reviews?media_type=movie&media_id=11")
        assert len(list_res.get_json()["reviews"]) == 0

    def test_delete_nonexistent_review_returns_404(self, client, user):
        res = client.delete("/api/reviews/99999", headers={"X-User-Id": str(user.id)})
        assert res.status_code == 404

    def test_other_user_cannot_delete_review(self, client, app, user):
        """TC-RE-11 (Bug #3): user B must not be able to delete user A's review — expect 403."""
        with app.app_context():
            other = User(username="attacker", email="attacker@test.com")
            other.set_password("pass")
            _db.session.add(other)
            _db.session.commit()
            other = User.query.filter_by(email="attacker@test.com").first()
            other_id = other.id

        create_res = _post_review(client, user.id, media_id="60")
        review_id = create_res.get_json()["review"]["id"]

        del_res = client.delete(
            f"/api/reviews/{review_id}",
            headers={"X-User-Id": str(other_id)},
        )
        assert del_res.status_code == 403


# ── TC-RE-04: Upsert — second POST updates existing review ──────────────────

class TestUpsertReview:
    """TC-RE-04 — second POST for same user+media updates the existing review."""

    def test_second_post_returns_200_not_201(self, client, user):
        _post_review(client, user.id, media_id="20", rating=3)
        res = _post_review(client, user.id, media_id="20", rating=5)
        assert res.status_code == 200

    def test_second_post_updates_rating(self, client, user):
        _post_review(client, user.id, media_id="21", rating=2)
        _post_review(client, user.id, media_id="21", rating=5)

        list_res = client.get("/api/reviews?media_type=movie&media_id=21")
        reviews = list_res.get_json()["reviews"]
        assert len(reviews) == 1
        assert reviews[0]["rating"] == 5

    def test_second_post_message_is_review_updated(self, client, user):
        _post_review(client, user.id, media_id="22", rating=1)
        res = _post_review(client, user.id, media_id="22", rating=4)
        assert res.get_json()["message"] == "Review updated"


# ── TC-RE-05: Unauthenticated requests rejected ──────────────────────────────

class TestUnauthenticated:
    """TC-RE-05 — requests without X-User-Id return 401."""

    def test_post_without_auth_returns_401(self, client):
        res = client.post(
            "/api/reviews",
            json={"media_id": "1", "media_type": "movie", "rating": 3, "title": "X"},
        )
        assert res.status_code == 401

    def test_mine_without_auth_returns_401(self, client):
        res = client.get("/api/reviews/mine")
        assert res.status_code == 401

    def test_check_without_auth_returns_401(self, client):
        res = client.get("/api/reviews/check/movie/1")
        assert res.status_code == 401

    def test_delete_without_auth_returns_401(self, client):
        res = client.delete("/api/reviews/1")
        assert res.status_code == 401


# ── TC-RE-06: /mine returns only the current user's reviews ─────────────────

class TestMyReviews:
    """TC-RE-06 — GET /api/reviews/mine returns only the authenticated user's reviews."""

    def test_mine_returns_only_current_users_reviews(self, client, app, user):
        # Create a second user
        with app.app_context():
            other = User(username="other_user", email="other@test.com")
            other.set_password("pass")
            _db.session.add(other)
            _db.session.commit()
            other = User.query.filter_by(email="other@test.com").first()
            other_id = other.id

        _post_review(client, user.id, media_id="30", media_type="movie")
        _post_review(client, user.id, media_id="31", media_type="movie")
        _post_review(client, other_id, media_id="32", media_type="movie")

        res = client.get("/api/reviews/mine", headers={"X-User-Id": str(user.id)})
        data = res.get_json()
        assert res.status_code == 200
        assert len(data["reviews"]) == 2
        for r in data["reviews"]:
            assert r["user_id"] == user.id


# ── TC-RE-07: /check returns the user's existing review ─────────────────────

class TestCheckReview:
    """TC-RE-07 — GET /api/reviews/check returns review when one exists."""

    def test_check_returns_review_when_exists(self, client, user):
        _post_review(client, user.id, media_id="40", media_type="movie", rating=4)
        res = client.get(
            "/api/reviews/check/movie/40",
            headers={"X-User-Id": str(user.id)},
        )
        data = res.get_json()
        assert res.status_code == 200
        assert data["review"] is not None
        assert data["review"]["rating"] == 4

    def test_check_returns_none_when_no_review(self, client, user):
        res = client.get(
            "/api/reviews/check/movie/99999",
            headers={"X-User-Id": str(user.id)},
        )
        data = res.get_json()
        assert res.status_code == 200
        assert data["review"] is None


# ── TC-RE-08: Rating boundary value testing ──────────────────────────────────

class TestRatingBoundary:
    """TC-RE-08 — rating must be an integer between 1 and 5 inclusive."""

    def test_rating_zero_returns_400(self, client, user):
        res = client.post(
            "/api/reviews",
            json={"media_id": "50", "media_type": "movie", "rating": 0, "title": "X"},
            headers={"X-User-Id": str(user.id)},
        )
        assert res.status_code == 400

    def test_rating_six_returns_400(self, client, user):
        res = client.post(
            "/api/reviews",
            json={"media_id": "51", "media_type": "movie", "rating": 6, "title": "X"},
            headers={"X-User-Id": str(user.id)},
        )
        assert res.status_code == 400

    def test_rating_one_is_valid(self, client, user):
        res = client.post(
            "/api/reviews",
            json={"media_id": "52", "media_type": "movie", "rating": 1, "title": "X"},
            headers={"X-User-Id": str(user.id)},
        )
        assert res.status_code == 201

    def test_rating_five_is_valid(self, client, user):
        res = client.post(
            "/api/reviews",
            json={"media_id": "53", "media_type": "movie", "rating": 5, "title": "X"},
            headers={"X-User-Id": str(user.id)},
        )
        assert res.status_code == 201

    def test_rating_as_string_returns_400(self, client, user):
        res = client.post(
            "/api/reviews",
            json={"media_id": "54", "media_type": "movie", "rating": "four", "title": "X"},
            headers={"X-User-Id": str(user.id)},
        )
        assert res.status_code == 400


# ── TC-RE-09: Favorites endpoint regression ──────────────────────────────────

class TestFavoritesRegression:
    """TC-RE-09 — /api/favorites still works after reviews blueprint registered."""

    def test_favorites_list_returns_200(self, client, user):
        res = client.get("/api/favorites", headers={"X-User-Id": str(user.id)})
        assert res.status_code == 200
        assert "favorites" in res.get_json()


# ── TC-RE-10: Search endpoint regression ─────────────────────────────────────

class TestSearchRegression:
    """TC-RE-10 — /api/search still works after reviews blueprint registered."""

    @patch("app.api_routes.tmdb")
    @patch("app.api_routes.gbooks")
    def test_search_all_returns_200(self, mock_gbooks, mock_tmdb, client):
        mock_tmdb.search_media.return_value = {"results": []}
        mock_gbooks.search_books.return_value = {"results": []}
        res = client.get("/api/search?query=batman&type=all")
        assert res.status_code == 200
