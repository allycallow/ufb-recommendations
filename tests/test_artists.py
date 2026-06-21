from unittest.mock import patch

ARTIST_ID = "artist123"
BASE_URL = f"/artists/{ARTIST_ID}"
TRENDING_URL = "/artists/trending"
TOP_PICKS_URL = f"{BASE_URL}/top-picks"


def test_missing_api_key_returns_403(client):
    response = client.get(f"{BASE_URL}/related-artists")
    assert response.status_code == 403


def test_invalid_api_key_returns_401(client):
    response = client.get(
        f"{BASE_URL}/related-artists", headers={"X-API-Key": "wrong-key"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_related_artists_empty(client, auth_headers):
    with patch("app.db.get_artist_related_artists", return_value=[]) as mock_db:
        response = client.get(f"{BASE_URL}/related-artists", headers=auth_headers)
        mock_db.assert_called_once_with(ARTIST_ID)
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_related_artists_with_data(client, auth_headers):
    mock_data = [{"id": "artist:abc"}, {"id": "artist:xyz"}]
    with patch("app.db.get_artist_related_artists", return_value=mock_data) as mock_db:
        response = client.get(f"{BASE_URL}/related-artists", headers=auth_headers)
        mock_db.assert_called_once_with(ARTIST_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == ["artist:abc", "artist:xyz"]


def test_trending_artists_missing_api_key_returns_403(client):
    response = client.get(TRENDING_URL)
    assert response.status_code == 403


def test_trending_artists_invalid_api_key_returns_401(client):
    response = client.get(TRENDING_URL, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_trending_artists_empty(client, auth_headers):
    with patch("app.db.get_trending_artists", return_value=[]) as mock_db:
        response = client.get(TRENDING_URL, headers=auth_headers)
        mock_db.assert_called_once()
    assert response.status_code == 200
    assert response.json() == {"success": True, "items": []}


def test_trending_artists_with_data(client, auth_headers):
    artist_ids = [
        "a4517d13-8371-4e28-b07f-8f47c56b561c",
        "41e5a14a-40ce-482d-8b2c-84f013b40f1e",
    ]
    with patch("app.db.get_trending_artists", return_value=artist_ids) as mock_db:
        response = client.get(TRENDING_URL, headers=auth_headers)
        mock_db.assert_called_once()
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == artist_ids


def test_top_picks_missing_api_key_returns_403(client):
    response = client.get(TOP_PICKS_URL)
    assert response.status_code == 403


def test_top_picks_invalid_api_key_returns_401(client):
    response = client.get(TOP_PICKS_URL, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["statusCode"] == 401


def test_top_picks_empty(client, auth_headers):
    with patch("app.db.get_artist_top_picks", return_value=[]) as mock_db:
        response = client.get(TOP_PICKS_URL, headers=auth_headers)
        mock_db.assert_called_once_with(ARTIST_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == []
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total"] == 0


def test_top_picks_with_data(client, auth_headers):
    mock_items = ["track1", "track2", "track3"]
    with patch("app.db.get_artist_top_picks", return_value=mock_items) as mock_db:
        response = client.get(TOP_PICKS_URL, headers=auth_headers)
        mock_db.assert_called_once_with(ARTIST_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["items"] == mock_items
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total"] == 3


def test_top_picks_pagination(client, auth_headers):
    mock_items = [f"track{i}" for i in range(5)]
    with patch("app.db.get_artist_top_picks", return_value=mock_items) as mock_db:
        response = client.get(
            TOP_PICKS_URL, params={"page": 2, "page_size": 2}, headers=auth_headers
        )
        mock_db.assert_called_once_with(ARTIST_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == ["track2", "track3"]
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert data["total"] == 5


def test_top_picks_page_beyond_data(client, auth_headers):
    mock_items = ["track1", "track2"]
    with patch("app.db.get_artist_top_picks", return_value=mock_items) as mock_db:
        response = client.get(
            TOP_PICKS_URL, params={"page": 5, "page_size": 10}, headers=auth_headers
        )
        mock_db.assert_called_once_with(ARTIST_ID)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 2
