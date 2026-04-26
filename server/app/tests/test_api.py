"""
Test suite for api_routes.py
Methodology: Unit + Integration (Flask test client — no real API calls)
All external services (TMDB, RAWG, Google Books) are mocked so tests
run offline and never consume API quota.
"""
import pytest
from unittest.mock import patch
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Health check ────────────────────────────────────────────
class TestHealthCheck:
    """TC-S01: Smoke — verify API is reachable"""

    def test_health_returns_200(self, client):
        res = client.get("/api/health")
        assert res.status_code == 200

    def test_health_returns_ok_status(self, client):
        data = client.get("/api/health").get_json()
        assert data["status"] == "ok"


# ── Search endpoint ─────────────────────────────────────────
class TestSearch:
    """TC-I01 through TC-I05: Integration — search route validation"""

    def test_search_missing_query_returns_400(self, client):
        """TC-I01: no query param → 400"""
        res = client.get("/api/search")
        assert res.status_code == 400
        assert "error" in res.get_json()

    def test_search_invalid_type_returns_400(self, client):
        """TC-I02: bad type param → 400"""
        res = client.get("/api/search?query=test&type=podcast")
        assert res.status_code == 400

    @patch("app.api_routes.tmdb")
    @patch("app.api_routes.gbooks")
    def test_search_all_returns_200(self, mock_gbooks, mock_tmdb, client):
        """TC-I03: type=all with mocked services → 200"""
        mock_tmdb.search_media.return_value = {"results": [{"id": 1, "title": "Matrix"}]}
        mock_gbooks.search_books.return_value = {"results": []}
        res = client.get("/api/search?query=matrix&type=all")
        assert res.status_code == 200
        assert "results" in res.get_json()

    @patch("app.api_routes.rawg")
    def test_search_game_returns_200(self, mock_rawg, client):
        """TC-I04: type=game with mocked RAWG → 200"""
        mock_rawg.search_games.return_value = {"results": [{"id": 99, "name": "Doom"}]}
        res = client.get("/api/search?query=doom&type=game")
        assert res.status_code == 200

    @patch("app.api_routes.rawg")
    def test_search_game_service_failure_returns_500(self, mock_rawg, client):
        """TC-I05: RAWG returns None (API down) → 500"""
        mock_rawg.search_games.return_value = None
        res = client.get("/api/search?query=doom&type=game")
        assert res.status_code == 500


# ── Movie detail endpoint ───────────────────────────────────
class TestMovieDetail:
    """TC-I06 through TC-I08: Integration — movie detail route"""

    @patch("app.api_routes.tmdb")
    def test_get_movie_success(self, mock_tmdb, client):
        """TC-I06: valid movie id → 200 with data"""
        mock_tmdb.get_movie.return_value = {"id": 603, "title": "The Matrix"}
        res = client.get("/api/movie/603")
        assert res.status_code == 200
        assert res.get_json()["title"] == "The Matrix"

    @patch("app.api_routes.tmdb")
    def test_get_movie_not_found(self, mock_tmdb, client):
        """TC-I07: TMDB says movie not found → 404"""
        mock_tmdb.get_movie.return_value = {"success": False}
        res = client.get("/api/movie/999999")
        assert res.status_code == 404

    @patch("app.api_routes.tmdb")
    def test_get_movie_service_failure(self, mock_tmdb, client):
        """TC-I08: TMDB returns None → 500"""
        mock_tmdb.get_movie.return_value = None
        res = client.get("/api/movie/603")
        assert res.status_code == 500


# ── Trending endpoint ───────────────────────────────────────
class TestTrending:
    """TC-I09 through TC-I11: Integration — trending route"""

    @patch("app.api_routes.tmdb")
    def test_trending_movie_returns_200(self, mock_tmdb, client):
        """TC-I09: type=movie → 200"""
        mock_tmdb.get_trending.return_value = {"results": []}
        res = client.get("/api/trending?type=movie")
        assert res.status_code == 200

    def test_trending_invalid_type_returns_400(self, client):
        """TC-I10: bad type → 400"""
        res = client.get("/api/trending?type=podcast")
        assert res.status_code == 400

    @patch("app.api_routes.tmdb")
    def test_trending_invalid_window_returns_400(self, mock_tmdb, client):
        """TC-I11: bad time window → 400"""
        res = client.get("/api/trending?type=movie&window=year")
        assert res.status_code == 400


# ── Media details endpoint ──────────────────────────────────
class TestMediaDetails:
    """TC-I12 through TC-I13: Integration — generic media detail route"""

    @patch("app.api_routes.tmdb")
    def test_get_media_detail_movie(self, mock_tmdb, client):
        """TC-I12: media_type=movie → calls tmdb.get_movie"""
        mock_tmdb.get_movie.return_value = {"id": 1, "title": "Inception"}
        res = client.get("/api/media/movie/1")
        assert res.status_code == 200
        mock_tmdb.get_movie.assert_called_once_with(1)

    def test_get_media_detail_invalid_type(self, client):
        """TC-I13: unknown media_type → 400"""
        res = client.get("/api/media/anime/1")
        assert res.status_code == 400

"""
SOURCES / REFERENCES:
- pytest documentation: fixtures, test classes, conftest patterns
  https://docs.pytest.org/en/stable/
- Flask testing documentation: app.test_client(), TESTING config flag
  https://flask.palletsprojects.com/en/3.0.x/testing/
- unittest.mock documentation: patch decorator, MagicMock, return_value
  https://docs.python.org/3/library/unittest.mock.html
- Flask Blueprint testing pattern: registering blueprints in test app via create_app factory
  https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
- Test case IDs (TC-I01 etc.) linked to test plan methodology in Sprint 2 doc
"""